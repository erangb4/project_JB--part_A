import pytest
from facades.AnonymousFacade import AnonymousFacade
from classes.User import User
from classes.Administrator import Administrator
from classes.Customer import Customer
from classes.AirlineCompany import AirlineCompany
from exceptions.WrongData import WrongDataError
from Db_Repo_Pool import DbRepoPool


@pytest.fixture(scope='session')
def administrator_facade_object():
    print('Setting up same DAO for all tests.')
    repool = DbRepoPool.get_instance()
    repo = repool.get_connection()
    anonfacade = AnonymousFacade(repo)
    return anonfacade.login('yochi', '1234567')


@pytest.fixture(autouse=True)
def reset_db(administrator_facade_object):
    administrator_facade_object.repo.reset_test_db()
    return


@pytest.mark.parametrize('administrator, expected', [Administrator(first_name='roni', last_name='rani', user_id=8), True])
def test_administrator_facade_add_administrator(administrator_facade_object, administrator, expected):
    actual = administrator_facade_object.add_administrator(administrator)
    assert actual == expected


@pytest.mark.parametrize('user, administrator', [('not user', 2),
                                                 (User(username='bar', password='123', email='bar@gmail.com', user_role=9), 2),
                                                 (User(username='bar', password='123', email='bar@gmail.com', user_role=3), 2),
                                                 (User(username='bari', password='123', email='bari@gmail.com', user_role=3), 'par')])
def test_administrator_facade_add_administrator_raise_notvaliddataerror(administrator_facade_object, user, administrator):
    with pytest.raises(WrongDataError):
        administrator_facade_object.add_administrator(administrator)

'''
def test_administrator_facade_get_all_customers(administrator_facade_object):
    actual = administrator_facade_object.get_all_customers()
    expected = [Customer(id=1, first_name='ron', last_name='bar', address='herzel 14', phone_no='0546655443', credit_card_no='4580', user_id=1),
                Customer(id=2, first_name='bor', last_name='tor', address='gori 4', phone_no='0543321444', credit_card_no='4567', user_id=2)]
    assert actual == expected


@pytest.mark.parametrize('admin_id, expected', [(1, True)])
def test_administrator_facade_remove_administrator(administrator_facade_object, admin_id, expected):
    actual = administrator_facade_object.remove_administrator(admin_id)
    assert actual == expected


@pytest.mark.parametrize('admin_id', ['not int', -1, 3])
def test_administrator_facade_remove_administrator_raise_notvaliddataerror(administrator_facade_object, admin_id):
    with pytest.raises(WrongDataError):
        administrator_facade_object.remove_administrator(admin_id)


@pytest.mark.parametrize('customer_id, expected', [(1, True), (2, True)])
def test_administrator_facade_remove_customer(administrator_facade_object, customer_id, expected):
    actual = administrator_facade_object.remove_customer(customer_id)
    assert actual == expected


@pytest.mark.parametrize('customer_id', ['f', 0, 3])
def test_administrator_facade_remove_customer_raise_notvaliddataerror(administrator_facade_object, customer_id):
    with pytest.raises(WrongDataError):
        administrator_facade_object.remove_customer(customer_id)


@pytest.mark.parametrize('airline_id, expected', [(1, True)])
def test_administrator_facade_remove_airline(administrator_facade_object, airline_id, expected):
    actual = administrator_facade_object.remove_airline(airline_id)
    assert actual == expected


@pytest.mark.parametrize('airline_id', ['f', -1, 4])
def test_administrator_facade_remove_airline_raise_notvaliddataerror(administrator_facade_object, airline_id):
    with pytest.raises(WrongDataError):
        administrator_facade_object.remove_airline(airline_id)


@pytest.mark.parametrize('user, customer, expected', [
                                                      (User(username='rabi', password='123', email='rabi@gmail.com', user_role=1),
                                                      Customer(first_name='so', last_name='os', address='mor 18', phone_no='0987654321', credit_card_no='6543', user_id=8) , True)])
def test_administrator_facade_add_customer(administrator_facade_object, user, customer, expected):
    actual = administrator_facade_object.add_customer(user, customer)
    assert actual == expected


@pytest.mark.parametrize('user, customer', [(1, 1),
                                            (User(username='bab', password='123', email='bab@gmail.com', user_role=2),
                                            Customer(first_name='rew', last_name='wer', address='rosh 1', phone_no='0543765432', credit_card_no='0099', user_id=1)),
                                            (User(username='dad', password='123', email='dad@gmail.coom', user_role=2),
                                            Customer(first_name='rew', last_name='wer', address='rosh 1', phone_no='0543765432', credit_card_no='0099', user_id=1)),
                                            (User(username='bab', password='123', email='bab@gmail.com', user_role=1),
                                            Customer(first_name='rew', last_name='wer', address='rosh 1', phone_no='0543765432', credit_card_no='0099', user_id=1)),
                                            (User(username='dad', password='123', email='dad@gmail.coom', user_role=2), 'tre'),
                                            (User(username='dad', password='123', email='dad@gmail.com', user_role=1),
                                            Customer(first_name='rew', last_name='wer', address='rosh 1', phone_no='0543765432', credit_card_no='0099', user_id=1)),
                                            (User(username='dad', password='123', email='dadi@gmail.com', user_role=1),
                                             Customer(first_name='rew', last_name='wer', address='rosh 1', phone_no='0543765432', credit_card_no='0099', user_id=1))])
def test_administrator_facade_add_customer_raise_notvaliddataerror(administrator_facade_object, user, customer):
    with pytest.raises(WrongDataError):
        administrator_facade_object.add_customer(user, customer)


@pytest.mark.parametrize('user, airline, expected', [
                                                     (User(username='ronen', password='123', email='ronen@gmail.com', user_role=2),
                                                      AirlineCompany(name='usd', country_id=1, user_id=8), True)])
def test_administrator_facade_add_airline(administrator_facade_object, user, airline, expected):
    actual = administrator_facade_object.add_airline(user, airline)
    assert actual == expected


@pytest.mark.parametrize('user, airline', [(1, 1),
                                           (User(username='roi', password='123', email='roi@gmail.com', user_role=1), 1),
                                           (User(username='roki', password='123', email='roi@gmail.com', user_role=2), 1),
                                           (User(username='roi', password='123', email='roi@gmail.com', user_role=2),
                                           AirlineCompany(name='mok', country_id=1, user_id=3)),
                                           (User(username='roi', password='123', email='roi@gmail.com', user_role=2),
                                           AirlineCompany(name='usd', country_id=3, user_id=3))])
def test_administrator_facade_add_airline_raise_notvaliddataerror(administrator_facade_object, user, airline):
    with pytest.raises(WrongDataError):
        administrator_facade_object.add_customer(user, airline)
'''

