# -*- coding: utf-8 -*-
import logging
import daiquiri
import json
import uuid
import math
import time
from tqdm import tqdm

from ..exceptions import *
from .resultset import ResultSet
from ..util import Uri

daiquiri.setup(level=logging.INFO)

logger = daiquiri.getLogger(__name__)


class HierarchyHelper:
    def _collect_ancestors(self):
        """Collects ancestors for this instance, 
        starting with the root of the tree (Pio) and
        ending with the instance itself.
        """

        ancestors = [self]
        parent = self._parent
        while parent is not None:
            ancestors.append(parent)
            parent = parent._parent
        return ancestors[::-1]

    @property
    def root(self):
        return self._collect_ancestors()[0]  # the root must always be pio

    def block_until_completion(self, transaction_uuid, timeout=None):
        processed = 0
        started_at = time.time()
        pbar = tqdm(total=100, desc="Processing")

        while True:
            if timeout is not None and time.time() > started_at + timeout:
                print("timeout reached, breaking loop")
                break

            result_json, status_code = self.root._dispatch_request(
                caller=self,
                operation="TRANSACTION_STATUS",
                path=f"transaction_status/{transaction_uuid}",
            )

            if status_code == 200:
                if result_json["STATUS"] == "FINISHED":
                    pbar.update(100 - processed)
                    # TODO: Refresh ancestors

                    pbar.close()
                    return True

                elif result_json["STATUS"] == "RECEIVING":
                    pass

                elif result_json["STATUS"] == "PROCESSING":
                    percentage = int(
                        float(result_json["OPS_DONE"])
                        / float(result_json["OPS_TOTAL"])
                        * 100
                    )
                    pbar.update(percentage - processed)
                    processed = percentage

            else:
                pbar.close()
                return False

            time.sleep(0.5)


class BaseResource(HierarchyHelper):
    def __init__(self, parent, **kwargs):
        self._parent = parent
        self._ancestors = self._collect_ancestors()

        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def uri(self):
        return self.PATH.format(**{self.__class__.__name__.lower(): self.uid})

    @classmethod
    def is_allowed(cls, operation):
        return True

    def delete(self):
        """
        Deletes this resource
        
        ```python
        resource = collection.filter(key__exact="mykey").first
        resource.delete()
        ```
        """
        result_json = self.root._dispatch_request(
            caller=self, operation="DELETE", path=self.uri
        )

    def update(self):
        """
        Updates this resource
        
        ```python
        resource = collection.filter(key__exact="mykey").first
        resource.key = "anotherkey"
        resource.update()
        ```
        """
        self.root._push_operation(
            caller=self,
            operation="UPDATE",
            path=self.uri,
            params=None,
            data=None,
            headers=None,
        )


class Resource(BaseResource):
    def __init__(self, parent, uid, **kwargs):
        super().__init__(parent=parent, **kwargs)
        self.uid = uid

        for key, value in kwargs.items():
            setattr(self, key, value)

    def _refresh(self):
        # Ignore relations so as to avoid overriding pyprimed relations
        excluded = ["experiments", "abvariants", "signals", "targets", "campaigns"]

        result_json = self.root._dispatch_request(
            caller=self, operation="GET", path=self.uri
        )

        for key, value in result_json.items():
            if key not in excluded:
                setattr(self, key, value)


class Relationship(BaseResource):
    def __init__(self, parent, from_uid, to_uid, **kwargs):
        super().__init__(parent=parent, **kwargs)
        self.from_uid = from_uid
        self.to_uid = to_uid

        for key, value in kwargs.items():
            setattr(self, key, value)


class Collection(HierarchyHelper):
    """Provides the Collection class, designed to
    hold various Resource types and offers 
    methods to modify the collection.
    """

    def __init__(self, parent, path, operations):
        self._parent = parent
        self._path = path
        self._operations = operations

    @property
    def allowed_operations(self):
        return self._operations

    def is_allowed(self, operation):
        if operation not in self.allowed_operations:
            return False
        return True

    @property
    def path(self):
        raise NotImplementedError

    def create(self, **attrs):
        """
        Adds an object to collection

        ```python
        collection.create(name="mymodel")
        ```
        
        # Arguments
        attrs (dict): Attributes of object to be added.

        # Raises
        AlreadyExistsException: If resource by that primary key already exists.
        """

        parent_class = self._parent.__class__.__name__.lower()
        if parent_class != "pio":
            attrs[parent_class] = {"uid": self._parent.uid}

        result_json = self.root._dispatch_request(
            caller=self, operation="CREATE", path=self.path, data=dict(attrs)
        )

        return self._RESOURCE(parent=self, **result_json)

    def get_or_create(self, **attrs):
        parent_class = self._parent.__class__.__name__.lower()
        if parent_class != "pio":
            attrs[parent_class] = {"uid": self._parent.uid}

        result_json = self.root._dispatch_request(
            caller=self, operation="GET_OR_CREATE", path=self.path, data=dict(attrs)
        )

        return self._RESOURCE(parent=self, **result_json)

    def get(self, **pk):
        """
        Gets a single object by primary key from collection

        ```python
        collection.get(key="my_unique_key")
        ```
        
        # Arguments
        pk (**dict): resource primary key
        """

        result_json = self.root._dispatch_request(
            caller=self,
            operation="GET",
            path=self.path,
            params={"filter": json.dumps(Uri.filter_default_setter(pk))},
        )

        return self._RESOURCE(parent=self, **result_json)

    def all(self, sort=None, range=None):
        """
        Retrieves all resources from collection

        ```python
        collection.all()
        ```
        
        # Arguments
        sort (???): sort argument
        range (???): range argument
        """
        request = {
            "caller": self,
            "operation": "ALL",
            "path": self.path,
            "params": {
                "sort": json.dumps(sort or self._DEFAULT_SORTING),
                "range": json.dumps(range or self._DEFAULT_RANGE),
            },
        }

        return ResultSet(self, request)

    def filter(self, sort=None, range=None, **filter):
        """
        Retrieve a subset of resources from collection

        ```python
        collection.filter(key__exact="mykey")
        ```
    
        # Arguments
        filter (**dict): filter conditions used to retrieve 
        subset: `collection.filter(name__contains="myvalue")`
        sort (???): sort argument
        range (???): range argument
        """
        request = {
            "caller": self,
            "operation": "FILTER",
            "path": self.path,
            "params": {
                "filter": json.dumps(Uri.filter_default_setter(filter)),
                "sort": json.dumps(sort or self._DEFAULT_SORTING),
                "range": json.dumps(range or self._DEFAULT_RANGE),
            },
        }

        return ResultSet(self, request)

    def upsert(self, resources, chunk_size=1000):
        """
        Upsert resources to the collection

        An upsert operation updates resources that exist both in
        the remote set, and the local set. Objects that only
        exist in the local set are created in the remote.

        # Arguments
        resources (list): Resources that will be uploaded to the server
        chunk_size (int): Size for chunks in number of elements, defaults to 1000
        """

        def chunks(resources, chunk_size):
            """Yields successive n-sized chunks from resources."""
            for i in range(0, len(resources), chunk_size):
                yield resources[i : i + chunk_size]

        def throttle(timeout_ms, fill_ratio):
            if fill_ratio >= 0.8:
                return float((timeout_ms + 0.1) * 2)
            elif fill_ratio < 0.2:
                return float(timeout_ms / 2)
            else:
                return timeout_ms

        if not self.is_allowed("UPSERT"):
            raise MethodNotAllowedExpection()

        timeout_ms = 0.0
        start_transaction_ts = None
        transaction_uuid = str(uuid.uuid4())
        num_chunks = math.ceil(len(resources) / chunk_size)

        headers = {
            "Content-Type": "application/json",
            "X-TX-LENGTH": str(num_chunks),
            "X-TX-SIZE": str(len(resources)),
            "X-TX-UUID": str(transaction_uuid),
        }

        for chunk in tqdm(
            chunks(resources, chunk_size), total=num_chunks, desc="Upserting"
        ):
            result_json, status_code = self.root._dispatch_request(
                caller=self,
                operation="UPSERT",
                path=self.path,
                data=list(chunk),
                headers=headers,
            )

            if status_code >= 200 and status_code <= 202:
                timeout_ms = throttle(timeout_ms, result_json["fillratio"])
                start_transaction_ts = start_transaction_ts or result_json["started_at"]
                time.sleep(float(timeout_ms / 1000))

            elif status_code == 204:
                # Upsertion performed successfully, but no body data is returned
                time.sleep(float(timeout_ms / 1000))

            elif status_code == 429:
                logger.error("API overloaded, try again later")
                return None

            else:
                logger.error(result_json)
                return None

        self.block_until_completion(transaction_uuid)
        return transaction_uuid, start_transaction_ts

    def delsert(self, resources, chunk_size=1000):
        """
        Delserts resources to the collection

        A delsert operation updates resources that exist both in 
        the remote set, and the local set. Objects that only 
        exist in the local set are created in the remote. 
        Objects that only exist in the remote set are removed
        from the remote set.

        ```python
        collection.delsert(resources)
        ```
        
        # Arguments
        resources (list): resources to be delserted
        """
        transaction_uuid, start_transaction_ts = self.upsert(
            resources, chunk_size=chunk_size
        )

        filter = {
            "transaction_uuid__ne": transaction_uuid,
            "created_at__lt": start_transaction_ts,
        }

        result_json = self.root._dispatch_request(
            caller=self,
            operation="DELETE",
            path=self.path,
            params={"filter": json.dumps(Uri.filter_default_setter(filter))},
        )

        self.block_until_completion(result_json["transaction_uuid"])

    def delete(self, force=False, **filter):
        """Deletes a subset of resources from the collection

        ```python
        collection.delete(key__exact="mykey")
        ```
    
        # Arguments
        force (boolean): forces execution despite not specifying
        filters (essentially deleting everything in the 
        collection)
        filter (**dict): filter conditions used to retrieve 
        subset: `collection.delete(name__contains="myvalue")`
        """

        result_json = self.root._dispatch_request(
            caller=self,
            operation="DELETE",
            path=self.path,
            params={"filter": json.dumps(Uri.filter_default_setter(filter))},
            headers={"X-FORCE-DELETE": str(force).upper()},
        )

        if "transaction_uuid" in result_json:
            transaction_uuid = result_json["transaction_uuid"]
            self.block_until_completion(transaction_uuid)


class SimpleCollection(Collection):
    """Provides a simple collection of resources"""

    def __init__(self, parent, path, operations):
        super().__init__(parent, path, operations)

    @property
    def path(self):
        interpolate = {}
        for a in self._collect_ancestors()[1:-1]:
            if hasattr(a, "uid") and a.uid is not None:
                interpolate[a.__class__.__name__.lower()] = a.uid
        return self._path.format(**interpolate)


class RelationshipCollection(Collection):
    """Provides a the RelationshipCollection 
    that allows for interacting with collections
    consisting of relationships."""

    def __init__(self, parent, path, operations):
        super().__init__(parent, path, operations)
        self._left = None
        self._right = None

    @property
    def path(self):
        if self._left is None or self._right is None:
            raise Exception("did you forget to call the `on()` method?")

        return self._path.format(
            **{
                self.__class__._LEFT.__name__.lower(): self._left.uid,
                self.__class__._RIGHT.__name__.lower(): self._right.uid,
            }
        )

    def on(self, **kwargs):
        self._left = kwargs[self.__class__._LEFT.__name__.lower()]
        self._right = kwargs[self.__class__._RIGHT.__name__.lower()]
        return self


class UsingRelationshipCollection(RelationshipCollection):
    """Provides a special class of RelationshipCollections 
    that allows for performing an additional intermediate 
    operation on one of it's 'parents'.

    e.g. upload targets before uploading predictions:
    ```python
    pio\
        .predictions\
        .on(model=model, universe=universe)\
        .using(*targets)\
        .upsert(*predictions)
    ```

    The class is WIP and flawed in many ways. It does,
    however provide the desired API for the predictions
    resources in `pyprimed`, as was intended.
    """

    def __init__(self, parent, path, operations):
        super().__init__(parent, path, operations)

    def _bind_using_left(self, member, method):
        self._bound = "left"
        self._left_member = member
        self._left_method = method
        # self._usingproxy = getattr(getattr(self._left, member), method)

    def _bind_using_right(self, member, method):
        self._bound = "right"
        self._right_member = member
        self._right_method = method
        # self._usingproxy = getattr(getattr(self._right, member), method)

    def using(self, *args, **kwargs):
        if self._left is None or self._right is None:
            raise Exception("did you forget to call the `on()` method?")

        if self._bound == "left":
            _usingproxy = getattr(
                getattr(self._left, self._left_member), self._left_method
            )
            _usingproxy(*args, **kwargs)
        else:
            _usingproxy = getattr(
                getattr(self._right, self._right_member), self._right_method
            )
            _usingproxy(*args, **kwargs)

        return self
