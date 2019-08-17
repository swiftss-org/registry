from app import restful
from registry.dao import Dao

entities_to_test = ['UserType',
                    'User',
                    'Patient',
                    'Hospital',
                    'Operation',
                    'Surgery']


def test_daos(database_session):
    for entity_name in entities_to_test:
        dao = Dao.find_dao(database_session, entity_name)
        all = dao.find_all()
        assert len(all) > 0
        for item in all:
            assert item == dao.find_id(item.id)

            new_item = dao.new(entity_name)
            new_item.from_dict(restful.json_loads(restful.json_dumps(item.as_dict())))
            assert new_item.as_dict() == item.as_dict()