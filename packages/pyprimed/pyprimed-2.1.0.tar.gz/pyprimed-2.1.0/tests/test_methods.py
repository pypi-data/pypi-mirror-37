# -*- coding: utf-8 -*-
"""
TestMethods
"""
import json
import pytest
import pyprimed

@pytest.mark.unit
class TestResourceRequest:
    def test_delete(self, monkeypatch, pio):

        def mockrequest(*args, **kwargs):
            assert kwargs["operation"] == "DELETE"
            assert kwargs["path"] == "models/xyz"
            assert kwargs["params"] == None
            assert kwargs["data"] == None
            assert kwargs["headers"] == None

        monkeypatch.setattr(pio, '_push_operation', mockrequest)

        model = pyprimed.models.model.Model(parent=pio, uid="xyz")
        model.delete

@pytest.mark.unit
class TestCollectionRequest:

    def test_create(self, monkeypatch, pio):

        def mockrequest(*args, **kwargs):
            assert kwargs["operation"] == "CREATE"
            assert kwargs["path"] == "models"
            assert kwargs["data"] == {"name": "mymodel"}
            return pyprimed.util.Dictionary.merge(kwargs["data"], {"uid": 1234})

        monkeypatch.setattr(pio, '_dispatch_request', mockrequest)

        pio.models.create(name="mymodel")

    def test_get(self, monkeypatch, pio):

        def mockrequest(*args, **kwargs):
            assert kwargs["operation"] == "GET"
            assert kwargs["path"] == "models"
            assert kwargs["params"] == {'filter': '{"name__exact": "mymodel"}'}
            return {"name": "mymodel", "uid": 1234}

        monkeypatch.setattr(pio, '_dispatch_request', mockrequest)

        pio.models.get(name="mymodel")

    def test_all(self, monkeypatch, pio):
        def mockrequest(*args, **kwargs):
            assert kwargs["operation"] == "ALL"
            assert kwargs["path"] == "models"
            return ({}, '')

        monkeypatch.setattr(pio, '_dispatch_request', mockrequest)

        pio.models.all()

    def test_filter(self, monkeypatch, pio):
        def mockrequest(*args, **kwargs):
            assert kwargs["operation"] == "FILTER"
            assert kwargs["path"] == "models"
            assert kwargs["params"] == {'filter': '{"name__exact": "mymodel"}', 'range': '[0, 100]', 'sort': '["name", "ASC"]'}
            return ({}, '')

        monkeypatch.setattr(pio, '_dispatch_request', mockrequest)

        pio.models.filter(name="mymodel")

    def test_upsert(self, monkeypatch, pio):
        def mockrequest(*args, **kwargs):
            assert (kwargs['operation'] == 'UPSERT' or kwargs['operation'] == 'TRANSACTION_STATUS')

            if kwargs['operation'] == 'UPSERT':
                assert kwargs['path'] == 'signals?model.uid=xyz'
                assert len(kwargs['data']) == 100

                assert kwargs['headers']['Content-Type'] == 'application/json'
                assert kwargs['headers']['X-TX-LENGTH'] == str(10)
                assert kwargs['headers']['X-TX-SIZE'] == str(1000)
                assert kwargs['headers']['X-TX-UUID'] is not None

                return ({'fillratio': 0.3, 'started_at': 27}, 200)
            else:
                return {'STATUS': 'FINISHED'}, 200

        monkeypatch.setattr(pio, '_dispatch_request', mockrequest)

        model = pyprimed.models.model.Model(parent=pio, uid='xyz')
        signals = [{'key': f'signal-{i}'} for i in range(1000)]
        transaction_uuid, start_transaction_ts = model.signals.upsert(signals, chunk_size=100)

        assert transaction_uuid is not None
        assert start_transaction_ts == 27

    def test_delsert(self, monkeypatch, pio):
        def mock_upsert(path, data, headers):
            assert path == "signals?model.uid=xyz"
            assert data == [
                {"key": "mysignal"}, {"key": "anothersignal"}]
            return ({"transaction_uuid": "abc", "started_at": 27, "fillratio": 0.3}, 200)

        def mock_delete(path, params, headers):
            assert path == "signals?model.uid=xyz"

            filter = json.loads(params["filter"])
            assert filter["created_at__lt"]
            assert filter["transaction_uuid__ne"]

            return {'transaction_uuid': '123'}

        def mock_transaction_status(path):
            return {'STATUS': 'FINISHED'}, 200

        monkeypatch.setattr(pio._client, 'upsert', mock_upsert)
        monkeypatch.setattr(pio._client, 'delete', mock_delete)
        monkeypatch.setattr(pio._client, 'transaction_status', mock_transaction_status)

        model = pyprimed.models.model.Model(parent=pio, uid='xyz')
        model.signals.delsert([{"key": "mysignal"}, {"key": "anothersignal"}])

    def test_delete(self, monkeypatch, pio):

        def mockrequest(*args, **kwargs):
            assert (kwargs["operation"] == "DELETE" or kwargs['operation'] == 'TRANSACTION_STATUS')

            if kwargs["operation"] == "DELETE":
                assert kwargs["path"] == "models"
                assert kwargs["params"] == {'filter': '{"name__exact": "mymodel"}'}
                assert kwargs["headers"] == {"X-FORCE-DELETE": "FALSE"}
                return {'transaction_uuid': '123'}
            else:
                return {'STATUS': 'FINISHED'}, 200

        monkeypatch.setattr(pio, '_dispatch_request', mockrequest)

        pio.models.delete(name="mymodel")

    def test_processing(self, monkeypatch, pio):
        self.ops_done = 0

        def mockrequest(*args, **kwargs):
            assert (kwargs['operation'] == 'UPSERT' or kwargs['operation'] == 'TRANSACTION_STATUS')

            if kwargs['operation'] == 'UPSERT':
                return ({'fillratio': 0.3, 'started_at': 27}, 200)
            if kwargs['operation'] == 'TRANSACTION_STATUS':
                self.ops_done += 1
                if self.ops_done < 10:
                    return {'STATUS': 'PROCESSING', 'OPS_TOTAL': 10, 'OPS_DONE': self.ops_done}, 200
                else:
                    return {'STATUS': 'FINISHED'}, 200

        monkeypatch.setattr(pio, '_dispatch_request', mockrequest)

        model = pyprimed.models.model.Model(parent=pio, uid='xyz')
        signals = [{'key': f'signal-{i}'} for i in range(1000)]
        transaction_uuid, start_transaction_ts = model.signals.upsert(signals, chunk_size=100)


@pytest.mark.unit
class TestRelationshipCollectionRequest:

    def test_create(self, monkeypatch, pio):

        def mockrequest(*args, **kwargs):
            assert kwargs["operation"] == "CREATE"
            assert kwargs["path"] == "predictions?model.uid=xyz&universe.uid=123"
            assert kwargs["data"] == {
                "sk": "A", "tk": "1", "score": 0.75}
            return pyprimed.util.Dictionary.merge(kwargs["data"], {"from_uid": 1234, "to_uid": 5678})

        monkeypatch.setattr(pio, '_dispatch_request', mockrequest)

        model = pyprimed.models.model.Model(parent=pio, uid="xyz")
        universe = pyprimed.models.universe.Universe(parent=pio, uid="123")

        pio\
            .predictions\
            .on(model=model, universe=universe)\
            .create(sk="A", tk="1", score=0.75)

    def test_all(self, monkeypatch, pio):
        def mockrequest(*args, **kwargs):
            assert kwargs["operation"] == "ALL"
            assert kwargs["path"] == "predictions?model.uid=xyz&universe.uid=123"
            return ({}, '')

        monkeypatch.setattr(pio, '_dispatch_request', mockrequest)

        model = pyprimed.models.model.Model(parent=pio, uid="xyz")
        universe = pyprimed.models.universe.Universe(parent=pio, uid="123")

        pio\
            .predictions\
            .on(model=model, universe=universe)\
            .all()

    def test_filter(self, monkeypatch, pio):
        def mockrequest(*args, **kwargs):
            assert kwargs["operation"] == "FILTER"
            assert kwargs["path"] == "predictions?model.uid=xyz&universe.uid=123"
            assert kwargs["params"] == {'filter': '{"sk__exact": "A"}', 'range': '[0, 100]', 'sort': '["score", "DESC"]'}
            return ({}, '')

        monkeypatch.setattr(pio, '_dispatch_request', mockrequest)

        model = pyprimed.models.model.Model(parent=pio, uid="xyz")
        universe = pyprimed.models.universe.Universe(parent=pio, uid="123")

        pio\
            .predictions\
            .on(model=model, universe=universe)\
            .filter(sk="A")

    def test_upsert(self, monkeypatch, pio):
        def mockrequest(*args, **kwargs):
            assert (kwargs["operation"] == "UPSERT" or kwargs['operation'] == 'TRANSACTION_STATUS')

            if kwargs["operation"] == "UPSERT":
                assert kwargs["path"] == "predictions?model.uid=xyz&universe.uid=123"
                assert kwargs["data"] == [{"sk": "A", "tk": "1", "score": 0.75}, {
                    "sk": "B", "tk": "1", "score": 0.1}]

                return ({'fillratio': 0.3, 'started_at': 27}, 200)
            else:
                return {'STATUS': 'FINISHED'}, 200

        monkeypatch.setattr(pio, '_dispatch_request', mockrequest)

        model = pyprimed.models.model.Model(parent=pio, uid="xyz")
        universe = pyprimed.models.universe.Universe(parent=pio, uid="123")

        pio\
            .predictions\
            .on(model=model, universe=universe)\
            .upsert([{"sk": "A", "tk": "1", "score": 0.75}, {"sk": "B", "tk": "1", "score": 0.1}])

    def test_delsert(self, monkeypatch, pio):
        def mock_upsert(path, data, headers):
            assert path == "predictions?model.uid=xyz&universe.uid=123"
            assert data == [{"sk": "A", "tk": "1", "score": 0.75}, {
                "sk": "B", "tk": "1", "score": 0.1}]
            return ({"transaction_uuid": "abc", "started_at": 27, "fillratio": 0.3}, 200)

        def mock_delete(path, params, headers):
            assert path == "predictions?model.uid=xyz&universe.uid=123"

            filter = json.loads(params["filter"])
            assert filter["created_at__lt"]
            assert filter["transaction_uuid__ne"]

            return {'transaction_uuid': '123'}

        def mock_transaction_status(path):
            return {'STATUS': 'FINISHED'}, 200

        monkeypatch.setattr(pio._client, 'upsert', mock_upsert)
        monkeypatch.setattr(pio._client, 'delete', mock_delete)
        monkeypatch.setattr(pio._client, 'transaction_status', mock_transaction_status)

        model = pyprimed.models.model.Model(parent=pio, uid="xyz")
        universe = pyprimed.models.universe.Universe(parent=pio, uid="123")

        pio\
            .predictions\
            .on(model=model, universe=universe)\
            .delsert([{"sk": "A", "tk": "1", "score": 0.75}, {"sk": "B", "tk": "1", "score": 0.1}])

    def test_delete(self, monkeypatch, pio):

        def mockrequest(*args, **kwargs):
            assert (kwargs["operation"] == "DELETE" or kwargs['operation'] == 'TRANSACTION_STATUS')

            if kwargs["operation"] == "DELETE":
                assert kwargs["path"] == "predictions?model.uid=xyz&universe.uid=123"
                assert kwargs["params"] == {'filter': '{"sk__exact": "A"}'}
                assert kwargs["headers"] == {"X-FORCE-DELETE": "FALSE"}
                return {'transaction_uuid': '123'}
            else:
                return {'STATUS': 'FINISHED'}, 200

        monkeypatch.setattr(pio, '_dispatch_request', mockrequest)

        model = pyprimed.models.model.Model(parent=pio, uid="xyz")
        universe = pyprimed.models.universe.Universe(parent=pio, uid="123")

        pio\
            .predictions\
            .on(model=model, universe=universe)\
            .delete(sk="A")
