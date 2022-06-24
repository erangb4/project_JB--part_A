from flask import Flask, request
import json
from Db_Repo import DbRepo
from Db_Config import local_session
from classes.Customer import Customer
from classes.User import User

repo = DbRepo(local_session)
app = Flask(__name__)


def convert_to_json(_list):
    json_list = []
    for i in _list:
        _dict = i.__dict__
        _dict.pop('_sa_instance_state', None)
        json_list.append(_dict)
    return json_list


@app.route("/")
def home():
    # print('hi')
    return '''
        <html>
            Customers!
            Countries!
            Administrators!
            Airline Companies!
            Users!
            User-Roles!
            Flights!
            Tickets!
        </html>
    '''


@app.route('/users', methods=['GET', 'POST'])
def get_or_post_user():
    if request.method == 'GET':
        return json.dumps(convert_to_json(repo.get_all(User)))
    if request.method == 'POST':
        new_user = request.get_json()
        repo.add(User(username=new_user['username'],
                      password=new_user['password'],
                      email=new_user['email'],
                      user_role=1))
        return '{"status": "success"}'


@app.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE', 'PATCH'])
def get_user_by_id(id):
    if request.method == 'GET':
        for c in convert_to_json(repo.get_all(User)):
            if c["id"] == id:
                return json.dumps(c)
        return '{}'
    if request.method == 'PUT':
        updated_new_user = request.get_json()
        users_json = convert_to_json(repo.get_all(User))
        for c in users_json:
            if c["id"] == id:
                c["password"] = updated_new_user["password"] if "password" in updated_new_user.keys() else None
                c["email"] = updated_new_user["email"] if "email" in updated_new_user.keys() else None
                repo.update_by_id(User, User.id, id, c)
                return json.dumps(updated_new_user)
            repo.add(User(id=updated_new_user['user_id'],
                          username=updated_new_user['username'],
                          password=updated_new_user['password'],
                          email=updated_new_user['email'],
                          user_role=1))
            return '{"status": "success"}'
        return '{"status": "not found"}'
    if request.method == 'PATCH':
        updated_user = request.get_json()
        users_json = convert_to_json(repo.get_all(User))
        for c in users_json:
            if c["id"] == id:
                c["password"] = updated_user["password"] if "password" in updated_user.keys() else None
                c["email"] = updated_user["email"] if "email" in updated_user.keys() else None
                repo.update_by_id(User, User.id, id, c)
                return '{"status": "success"}'
        return '{"status": "not found"}'
    if request.method == 'DELETE':
        deleted_user = request.get_json()
        users_json = convert_to_json(repo.get_all(User))
        for c in users_json:
            if c["id"] == id:
                repo.delete_by_id(User, User.id, id)
                repo.delete_by_id(User, User.id, c["user_id"])
        return f'{json.dumps(deleted_user)} deleted'
    return '{"status": "not found"}'


@app.route('/customers', methods=['GET', 'POST'])
def get_or_post_customer():
    if request.method == 'GET':
        return json.dumps(convert_to_json(repo.get_all(Customer)))
    if request.method == 'POST':
        new_customer = request.get_json()
        repo.add(Customer(first_name=new_customer['first_name'],
                          last_name=new_customer['last_name'],
                          address=new_customer['address'],
                          phone_number=new_customer['phone_number'],
                          credit_card_number=new_customer['credit_card_number'],
                          user_id=new_customer['user_id']))
        return '{"status": "success"}'


@app.route('/customers/<int:id>', methods=['GET', 'PUT', 'DELETE', 'PATCH'])
def get_customer_by_id(id):
    if request.method == 'GET':
        for c in convert_to_json(repo.get_all(Customer)):
            if c["id"] == id:
                return json.dumps(c)
        return '{}'
    if request.method == 'PUT':
        updated_new_customer = request.get_json()
        customers_json = convert_to_json(repo.get_all(Customer))
        for c in customers_json:
            if c["id"] == id:
                c["first_name"] = updated_new_customer["first_name"] if "first_name" in updated_new_customer.keys() else None
                c["last_name"] = updated_new_customer["last_name"] if "last_name" in updated_new_customer.keys() else None
                c["address"] = updated_new_customer["address"] if "address" in updated_new_customer.keys() else None
                c["phone_number"] = updated_new_customer["phone_number"] if "phone_number" in updated_new_customer.keys() else None
                c["credit_card_number"] = updated_new_customer["credit_card_number"] if "credit_card_number" in updated_new_customer.keys() else None
                repo.update_by_id(Customer, Customer.id, id, c)
                return json.dumps(updated_new_customer)
            repo.add(Customer(first_name=updated_new_customer['first_name'],
                              last_name=updated_new_customer['last_name'],
                              address=updated_new_customer['address'],
                              phone_number=updated_new_customer['phone_number'],
                              credit_card_number=updated_new_customer['credit_card_number'],
                              user_id=updated_new_customer['user_id']))
            return '{"status": "success"}'
        return '{"status": "not found"}'
    if request.method == 'PATCH':
        updated_customer = request.get_json()
        customers_json = convert_to_json(repo.get_all(Customer))
        for c in customers_json:
            if c["id"] == id:
                c["id"] = updated_customer["id"] if "id" in updated_customer.keys() else None
                c["first_name"] = updated_customer["first_name"] if "first_name" in updated_customer.keys() else None
                c["last_name"] = updated_customer["last_name"] if "last_name" in updated_customer.keys() else None
                c["address"] = updated_customer["address"] if "address" in updated_customer.keys() else None
                c["phone_number"] = updated_customer["phone_number"] if "phone_number" in updated_customer.keys() else None
                c["credit_card_number"] = updated_customer["credit_card_number"] if "credit_card_number" in updated_customer.keys() else None
                repo.update_by_id(Customer, Customer.id, id, c)
                return '{"status": "success"}'
        return '{"status": "not found"}'
    if request.method == 'DELETE':
        deleted_customer = request.get_json()
        customers_json = convert_to_json(repo.get_all(Customer))
        for c in customers_json:
            if c["id"] == id:
                repo.delete_by_id(Customer, Customer.id, id)
                repo.delete_by_id(User, User.id, c["user_id"])
        return f'{json.dumps(deleted_customer)} deleted'
    return '{"status": "not found"}'


app.run()

