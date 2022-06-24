import pytest
from classes.Customer import Customer
from classes.Ticket import Ticket
from facades.AnonymousFacade import AnonymousFacade
from exceptions.RemainingTickets import RemainingTicketsError
from exceptions.WrongData import WrongDataError
from Db_Repo_Pool import DbRepoPool


@pytest.fixture(scope='session')
def customer_facade_object():
    print('Setting up same DAO for all tests.')
    repool = DbRepoPool.get_instance()
    repo = repool.get_connection()
    anonfacade = AnonymousFacade(repo)
    return anonfacade.login('bibi', '1234')


@pytest.fixture(autouse=True)
def reset_db(customer_facade_object):
    customer_facade_object.repo.reset_test_db()
    return


@pytest.mark.parametrize('customer, expected', [(Customer(first_name='bela', last_name='sho', address='bar 1',
                                                          phone_no='0545847650', credit_card_no='9999', user_id=2), True)])
def test_customer_facade_update_customer(customer_facade_object, customer, expected):
    actual = customer_facade_object.update_customer(customer)
    assert actual == expected


@pytest.mark.parametrize('customer', ['not customer',
                                                (Customer(first_name='eran', last_name='gabay', address='hashaked 11',
                          phone_no='0547650267', credit_card_no='0022', user_id=2)),
                                                (Customer(first_name='eran', last_name='gabay', address='hashaked 11',
                          phone_no='0547650260', credit_card_no='0000', user_id=2))])
def test_customer_facade_update_customer_raise_notvaliddataerror(customer_facade_object, customer):
    with pytest.raises(WrongDataError):
        customer_facade_object.update_customer(customer)


@pytest.mark.parametrize('ticket, expected', [(Ticket(flight_id=2, customer_id=2), True)])
def test_customer_facade_remove_ticket(customer_facade_object, ticket, expected):
    actual = customer_facade_object.remove_ticket(ticket)
    assert actual == expected


@pytest.mark.parametrize('ticket', ['not ticket', Ticket(flight_id=3, customer_id=3), Ticket(flight_id=1, customer_id=1)])
def test_customer_facade_remove_ticket_raise_notvaliddataerror(customer_facade_object, ticket):
    with pytest.raises(WrongDataError):
        customer_facade_object.remove_ticket(ticket)


def test_customer_facade_get_tickets_by_customer(customer_facade_object):
    actual = customer_facade_object.get_tickets_by_customer()
    assert actual == [Ticket(id=2, flight_id=2, customer_id=2)]


def test_customer_facade_add_ticket_raise_noremainingticketserror(customer_facade_object):
    with pytest.raises(RemainingTicketsError):
        customer_facade_object.add_ticket(Ticket(flight_id=2, customer_id=1))


@pytest.mark.parametrize('ticket, expected', [(Ticket(flight_id=1), True)])
def test_customer_facade_add_ticket(customer_facade_object, ticket, expected):
    actual = customer_facade_object.add_ticket(ticket)
    assert actual == expected


@pytest.mark.parametrize('ticket', ['not ticket', Ticket(flight_id=4)])
def test_customer_facade_add_ticket_raise_notvaliddataerror(customer_facade_object, ticket):
    with pytest.raises(WrongDataError):
        customer_facade_object.add_ticket(ticket)
