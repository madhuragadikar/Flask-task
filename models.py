from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skincare.db?check_same_thread=False'

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(100))
    postcode = db.Column(db.String(100))
    country = db.Column(db.String(100))
    gender = db.Column(db.String(10))
    dob = db.Column(db.DateTime)

    def __init(self, first_name='NULL', last_name='NULL', email='NULL', address='NULL', postcode='NULL', country='NULL', gender='M', dob='2020'):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address
        self.postcode = postcode
        self.country = country
        self.gender = gender
        self.dob = dob

# Customer Schema
class CustomerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'address', 'postcode', 'country', 'gender', 'dob')

# Init schema
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

#TODO: Questionnaire to be stored in database to be able to display next question
# based on customer selection of answers.
class Questionnaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    current_question = db.Column(db.String(100))
    next_question = db.Column(db.String(100))
    gender = db.Column(db.String(10))
    is_pregnant_nursing_conceiving = db.Column(db.Boolean, default=False)
    is_severe = db.Column(db.Integer(), default=1)
    is_allergic = db.Column(db.Boolean, default=False)
    is_on_medication = db.Column(db.Boolean, default=False)

    def __init__(self, name='NULL', current_question='NULL', next_question='NULL', gender='M', is_pregnant_nursing_conceiving=False, is_severe=False, is_allergic=False, is_on_medication=False):
        self.name = name
        self.current_question = current_question
        self.next_question = next_question
        self.gender = gender
        self.is_pregnant_nursing_conceiving = is_pregnant_nursing_conceiving
        self.is_severe = is_severe
        self.is_allergic = is_allergic
        self.is_on_medication = is_on_medication

# Questionnaire Schema
class QuestionnaireSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'current_question', 'next_question', 'gender', 'is_pregnant_nursing_conceiving', 'is_severe', 'is_allergic', 'is_on_medication')

# Init schema
question_schema = QuestionnaireSchema()
questions_schema = QuestionnaireSchema(many=True)


#TODO: Store customer Health details to be able to recommend products/medicine
class CustomerHealthDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    allergies_details = db.Column(db.String(500))
    is_pregnant_nursing_conceiving = db.Column(db.Boolean)
    medication_details = db.Column(db.String(500))
    recommended_products = db.Column(db.String(500))

    def __init__(self, cust_id, allergies_details, is_pregnant_nursing_conceiving, medication_details, recommended_products):
        self.cust_id = cust_id
        self.allergies_details = allergies_details
        self.is_pregnant_nursing_conceiving = is_pregnant_nursing_conceiving
        self.medication_details = medication_details
        self.recommended_products = recommended_products

# CustomerHealth Schema
class CustomerHealthSchema(ma.Schema):
    class Meta:
        fields = ('id', 'cust_id', 'allergies_details', 'medication_details', 'is_pregnant_nursing_conceiving', 'recommended_products')

# Init schema
customer_health_schema = CustomerHealthSchema()
customers_health_schema = CustomerHealthSchema(many=True)

# TODO: Set-up Allergy table to store list of all known allergies
# for humans along with severity
# class AllergyData(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     is_severe = db.Column(db.Integer(), nullable=False)
#
#     def __repr__(self):
#         return self.name
#

# TODO: Collection of products/medication available with SkinPlus
# class Products(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#
#     def __repr__(self):
#         return self.name
