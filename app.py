import requests
import pycountry
from flask import Flask, jsonify, request, abort, session, redirect, url_for, render_template
from flask_restful import Api
from models import Customer, Questionnaire, CustomerHealthDetails
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import and_

from models import customer_schema, customers_schema, question_schema, questions_schema, customer_health_schema

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skincare.db'
app.config['SECRET_KEY'] = 'Qp-PKPCsNmEOS4A0O6wB6g'

db = SQLAlchemy(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        return redirect(url_for('signup'))
        return render_template('signup.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        req = request.form
        user_email = req.get('email')
        data = {"email":user_email}

        '''
        Only unique email id allowed to be registered by the customer.
        Display error in case email already exist in db
        '''
        json_data = error_if_exists(Customer, ['email'], data)

        if json_data['error']:
            error = json_data['error']
            return render_template('signup.html', error=error)

        session['EMAIL'] = user_email
        return redirect(url_for('signup_address'))

    return render_template('signup.html')

@app.route('/signup/address', methods=['GET','POST'])
def signup_address():
    if request.method == 'GET':
        return render_template('address.html')
    if request.method == 'POST':
        req = request.form
        # EMAIL is required for registration;
        # signup page will be displayed if session does not have email details.
        if session.get('EMAIL', None) is not None:
            '''
            Error if postcode left blank or invalid - country UK is assumed here
            but can be extended for other countries using specific APIs.
            '''
            json_data = validate_postcode(req.get('postcode'))
            if json_data['status'] !=200 and json_data['error']:
                return redirect(url_for('signup_address'))
            session['POSTCODE'] = req.get('postcode')
            session['COUNTRY'] = req.get('country')
            session['ADDRESS'] = req.get('address')
            return redirect(url_for('signup_start'))
        else:
            return redirect(url_for('signup'))

    return render_template('welcome.html')

@app.route('/signup/welcome', methods=['GET','POST'])
def signup_start():
    if request.method == 'GET':
        return render_template('welcome.html')

    if request.method == 'POST':
        req = request.form
        # EMAIL  required for registration;
        # signup page will be displayed if session does not have email details.
        if session.get('EMAIL', None) is not None:
            if req.get('first_name', None) is None or req.get('last_name', None) is None:
                return redirect(url_for('signup_start'))
            session['FIRST_NAME'] = req.get('first_name')
            session['LAST_NAME'] = req.get('last_name')
            return redirect(url_for('questions'))
        else:
            return redirect(url_for('signup'))

    return render_template('questions.html')


@app.route('/questions', methods=['GET','POST'])
def questions():
    if request.method == 'GET':
        return render_template('questions.html')

    if request.method == 'POST':
        req = request.form
        # EMAIL is required for registration;
        # signup page will be displayed if session does not have email details.
        if session.get('EMAIL', None) is not None:
            if req.get('gender', None) is None:
                return redirect(url_for('signup_start'))
            session['GENDER'] = req.get('gender')
            return render_template('finish.html')
        else:
            return redirect(url_for('signup'))

    return render_template('finish.html')

@app.route('/finish', methods=['GET','POST'])
def finish():
    if request.method == 'GET':
        return render_template('finish.html')

    if request.method == 'POST':
        if session.get('EMAIL', None) is None:
            return redirect(url_for('signup'))

        new_customer = Customer()
        new_customer.first_name = session['FIRST_NAME']
        new_customer.last_name = session['LAST_NAME']
        new_customer.email = session['EMAIL']
        new_customer.postcode = session['POSTCODE']
        new_customer.address = session['ADDRESS']
        new_customer.country = session['COUNTRY']
        new_customer.gender = session['GENDER']

        data = {"email":session['EMAIL']}

        json_data = error_if_exists(Customer, ['email'], data)

        if json_data['error']:
            error = json_data['error']
            return render_template('signup.html', error=error)
        else:
            db.session.add(new_customer)
            db.session.commit()

    #Remove session now that customer added
    session.pop('EMAIL', None)
    session.pop('FIRST_NAME', None)
    session.pop('LAST_NAME', None)
    session.pop('EMAIL', None)
    session.pop('POSTCODE', None)
    session.pop('ADDRESS', None)
    session.pop('COUNTRY', None)
    session.pop('GENDER', None)

    return redirect(url_for('signup'))


'''
Customer APIs
'''

@app.route('/customer', methods=['POST'])
def add_customer():
    new_customer = Customer()
    for k,v in request.json.items():
        setattr(new_customer, k, v)

    db.session.add(new_customer)
    db.session.commit()

    return customer_schema.jsonify(new_customer)

@app.route('/customers/all', methods=['GET'])
def get_all_customers():
    all_customers = Customer.query.all()
    results = customers_schema.dump(all_customers)
    return jsonify(results)

@app.route('/customer/<int:id>', methods=['GET'])
def get_customer_by_id(id):
    data = {"id":id}
    result = error_if_does_not_exist(Customer, ['id'], data)
    response = Customer.query.get(id) if result['status'] == 200 else result['error']
    return customer_schema.jsonify(response)

@app.route('/customer/<string:name>', methods=['GET'])
def get_customer_by_name(name):
    data = {"first_name":name}
    result = error_if_does_not_exist(Customer, ['first_name'], data)
    response = Customer.query.filter_by(first_name=name).first() if result['status'] == 200 else result['error']
    return customer_schema.jsonify(response)

@app.route('/customer/<int:id>', methods=['PUT'])
def update_customer(id):
    response = {}
    customer = Customer.query.get(id)
    data = {"id":id}
    result = error_if_does_not_exist(Customer, ['id'], data)

    if result['status'] == 200:
        for k,v in request.json.items():
            setattr(customer, k, v)

        response = customer
        try:
            db.session.commit()
        except requests.exceptions.RequestException as e:
            print(f'Exception: ', e.args)
    else:
        return result

    return customer_schema.jsonify(response)

'''
Questionnaire APIs
'''
@app.route('/survey', methods=['POST'])
def add_question():
    new_question = Questionnaire()
    for k,v in request.json.items():
        setattr(new_question, k, v)

    db.session.add(new_question)
    db.session.commit()

    return question_schema.jsonify(new_question)

@app.route('/survey/<int:id>', methods=['PUT'])
def update_question(id):
    response = {}
    question = Questionnaire.query.get(id)
    data = {"id":id}
    result = error_if_does_not_exist(Questionnaire, ['id'], data)
    if result['status'] == 200:
        for k,v in request.json.items():
            setattr(question, k, v)

        response = question
        try:
            db.session.commit()
        except requests.exceptions.RequestException as e:
            print(f'Exception: ', e.args)
    else:
        return result

    return question_schema.jsonify(response)


@app.route('/survey/<int:id>', methods=['GET'])
def query_question_by_id(id):
    question = Questionnaire.query.get(id)
    return question_schema.jsonify(question)

@app.route('/surveys/all', methods=['GET'])
def get_all_questions():
    all_questions = Questionnaire.query.all()
    results = questions_schema.dump(all_questions)
    return jsonify(results)

'''
Errors/Validations
'''
def error_if_exists(table, lookups, form_data):
    json_data = {"status": 200, "error":""}
    conditions = [
        getattr(table, field_name) == form_data[field_name] for field_name in lookups if form_data[field_name]
    ]
    result = table.query.filter(and_(*conditions)).first()
    if result:
        json_data = {"status": 409, "error":"Already exists"}

    return json_data

def error_if_does_not_exist(table, lookups, form_data):
    json_data = {"status": 200, "error":""}
    conditions = [
        getattr(table, field_name) == form_data[field_name] for field_name in lookups if form_data[field_name]
    ]

    result = table.query.filter(and_(*conditions)).first()
    if not result:
        json_data = {"status": 409, "error":"Does not exist"}

    return json_data

def validate_postcode(postcode):
    postcode = postcode.replace(' ', '%20')
    main_api = 'http://api.postcodes.io/postcodes/'
    url = main_api+postcode
    json_data = requests.get(url).json()
    return json_data


#TODO: Create CustomerHealth database to dynamically update details depending on selection
# on the questionnaire
@app.route('/customer-health/<int:id>', methods=['GET'])
def get_customer_health_by_id(id):
    customer_health = CustomerHealthDetails.query.get(id)
    return customer_health_schema.jsonify(customer_health)

@app.route('/customer-health/<int:id>', methods=['PUT'])
def update_customer_health(id):
    customer_health = CustomerHealthDetails.query.get(cust_id=id)
    customer_health.allergies_details = request.json['allergies_details']
    customer_health.is_pregnant_nursing_conceiving = request.json['is_pregnant_nursing_conceiving']
    customer_health.medication_details = request.json['medication_details']
    customer_health.recommended_products = request.json['recommended_products']
    db.session.commit()

    return customer_health_schema.jsonify(customer_health)

@app.route('/customer-health', methods=['POST'])
def add_customer_health():
    cust_id = request.json['cust_id']
    allergies_details = request.json['allergies_details']
    is_pregnant_nursing_conceiving = request.json['is_pregnant_nursing_conceiving']
    medication_details = request.json['medication_details']
    recommended_products = request.json['recommended_products']
    new_customer_health = CustomerHealthDetails(
        cust_id,
        allergies_details,
        is_pregnant_nursing_conceiving,
        medication_details,
        recommended_products)
    db.session.add(new_customer_health)
    db.session.commit()

    return customer_health_schema.jsonify(new_customer_health)

if __name__ == "__main__":
    app.run(debug=True)
