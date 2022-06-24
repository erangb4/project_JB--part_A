import pytest
from facades.AnonymousFacade import AnonymousFacade
from classes.Flight import Flight
from classes.Country import Country
from classes.AirlineCompany import AirlineCompany
from datetime import datetime
from classes.User import User
from Db_Repo_Pool import DbRepoPool
from exceptions.WrongData import WrongDataError


@pytest.fixture(scope='session')
def dao_connection_singleton():
    print('Setting up same DAO for all tests.')
    repool = DbRepoPool.get_instance()
    repo = repool.get_connection()
    return AnonymousFacade(repo)


@pytest.fixture(autouse=True)
def reset_db(dao_connection_singleton):
    dao_connection_singleton.repo.reset_test_db()
    return


def test_facade_base_get_all_flights(dao_connection_singleton):
    actual = dao_connection_singleton.get_all_flights()
    assert actual == [Flight(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                             departure_time=datetime(2022, 3, 15, 6, 0, 0),
                             landing_time=datetime(2022, 3, 15, 10, 0, 0), remaining_tickets=200),
                      Flight(airline_company_id=2, origin_country_id=1, destination_country_id=2,
                             departure_time=datetime(2022, 2, 20, 6, 0, 0),
                             landing_time=datetime(2022, 2, 20, 10, 0, 0), remaining_tickets=0)]


@pytest.mark.parametrize('id_, expected', [(1, Flight(id=1, airline_company_id=1, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0),
                             remaining_tickets=200)), (2, Flight(id=2, airline_company_id=2, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0),
                        landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=0))])
def test_facade_base_get_flight_by_id(dao_connection_singleton, id_, expected):
    actual = dao_connection_singleton.get_flight_by_id(id_)
    assert actual == [expected]


@pytest.mark.parametrize('ocountry_id, dcountry_id, date_, expected', [
                                                                       (1, 2, datetime(2022, 1, 30), [Flight(id=1, airline_company_id=1, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0),
                             remaining_tickets=200), Flight(id=2, airline_company_id=2, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0),
                        landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=0)]),
                                                                       (1, 1, datetime(2022, 1, 30), [])])
def test_facade_base_get_flights_by_parameters(dao_connection_singleton, ocountry_id, dcountry_id, date_, expected):
    actual = dao_connection_singleton.get_flights_by_parameters(ocountry_id, dcountry_id, date_)
    assert actual == expected


@pytest.mark.parametrize('ocountry_id, dcountry_id, date_', [('f', 3, datetime(2022, 1, 30)),
                                                             (3, 'r', datetime(2022, 1, 30)),
                                                             (0, 4, datetime(2022, 1, 30)),
                                                             (1, 2, 4)])
def test_facade_base_get_flights_by_parameters_raise_notvaliddataerror(dao_connection_singleton, ocountry_id, dcountry_id, date_):
    with pytest.raises(WrongDataError):
        dao_connection_singleton.get_flights_by_parameters(ocountry_id, dcountry_id, date_)


def test_facade_base_get_all_airlines(dao_connection_singleton):
    actual = dao_connection_singleton.get_all_airlines()
    assert actual == [AirlineCompany(id=1, name='miri', country_id=1, user_id=3),
                      AirlineCompany(id=2, name='gidi', country_id=2, user_id=4)]


@pytest.mark.parametrize('id_, expected', [(3, []), (1, [AirlineCompany(id=1, name='miri', country_id=1, user_id=3)]),
                                           (2, [AirlineCompany(id=2, name='gidi', country_id=2, user_id=4)])])
def test_facade_base_get_airline_by_id(dao_connection_singleton, id_, expected):
    actual = dao_connection_singleton.get_airline_by_id(id_)
    assert actual == expected


@pytest.mark.parametrize('country_id', [('h'), (0)])
def test_facade_base_get_airline_by_id_raise_notvaliddataerror(dao_connection_singleton, country_id):
    with pytest.raises(WrongDataError):
        dao_connection_singleton.get_airline_by_id(country_id)


def test_facade_base_get_all_countries(dao_connection_singleton):
    actual = dao_connection_singleton.get_all_countries()
    assert actual == [Country(id=1, name='Israel'), Country(id=2, name='usa')]


@pytest.mark.parametrize('id_, expected', [(3, []), (1, [Country(id=1, name='Israel')]), (2, [Country(id=2, name='usa')])])
def test_facade_base_get_country_by_id(dao_connection_singleton, id_, expected):
    actual = dao_connection_singleton.get_country_by_id(id_)
    assert actual == expected


@pytest.mark.parametrize('country_id', [('6'), (0)])
def test_facade_base_get_country_by_id_raise_notvaliddataerror(dao_connection_singleton, country_id):
    with pytest.raises(WrongDataError):
        dao_connection_singleton.get_country_by_id(country_id)


@pytest.mark.parametrize('user, expected', [(User(username='Eranos', password='123', email='erano@gmail.coom', user_role=2), True)])
def test_facade_base_create_user(dao_connection_singleton, user, expected):
    actual = dao_connection_singleton.create_user(user)
    assert actual == expected


@pytest.mark.parametrize('user', [('notuser'),
                                  (User(username='eran', password='123', email='eranos@gmail.com', user_role=1)),
                                  User(username='Eranos', password='123', email='eran@gmail.com', user_role=2),
                                  User(username='Eranos', password='123', email='eranos@gmail.com', user_role=5)])
def test_facade_base_create_user_raise_notvaliddataerror(dao_connection_singleton, user):
    with pytest.raises(WrongDataError):
        dao_connection_singleton.create_user(user)


@pytest.mark.parametrize('airline_id, expected', [(1, [Flight(id=1, airline_company_id=1, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=200)])])
def test_airline_facade_get_flights_by_airline_id(dao_connection_singleton, airline_id, expected):
    actual = dao_connection_singleton.get_flights_by_airline_id(airline_id)
    assert actual == expected


@pytest.mark.parametrize('airline_id', ['not int', 0, 7])
def test_facade_base_get_flights_by_airline_id_raise_notvaliddataerror(dao_connection_singleton, airline_id):
    with pytest.raises(WrongDataError):
        dao_connection_singleton.get_flights_by_airline_id(airline_id)
