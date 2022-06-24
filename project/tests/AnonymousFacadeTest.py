import pytest
from facades.AnonymousFacade import AnonymousFacade
from facades.CustomerFacade import CustomerFacade
from facades.AirlineFacade import AirlineFacade
from facades.AdministratorFacade import AdministratorFacade
from exceptions.WrongUserRole import WrongUserRoleError
from exceptions.WrongData import WrongDataError
from Db_Repo_Pool import DbRepoPool


@pytest.fixture(scope='session')
def anonymous_facade_object():
    print('Setting up same DAO for all tests.')
    repool = DbRepoPool.get_instance()
    repo = repool.get_connection()
    return AnonymousFacade(repo)


@pytest.fixture(autouse=True)
def reset_db(anonymous_facade_object):
    anonymous_facade_object.repo.reset_test_db()
    return


@pytest.mark.parametrize('username, password, expected', [('bibi', '1234', CustomerFacade),
                                                          ('miri', '1234', AirlineFacade),
                                                          ('itay', '1234', AdministratorFacade)])
def test_anonymous_facade_log_in(anonymous_facade_object, username, password, expected):
    actual = anonymous_facade_object.login(username, password)
    if expected is None:
        assert actual == expected
    else:
        assert isinstance(actual, expected)


def test_anonymous_facade_log_in_raise_wronglogindataerror(anonymous_facade_object):
    with pytest.raises(WrongDataError):
        anonymous_facade_object.login('hh', '123')


def test_anonymous_facade_log_in_raise_userroletableerror(anonymous_facade_object):
    with pytest.raises(WrongUserRoleError):
        anonymous_facade_object.login('not legal', '123')