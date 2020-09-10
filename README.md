## Table of contents
* [General info](#general-info)
* [Dependencies](#dependencies)
* [Deploy](#deploy)
* [Documentation](#documentation)
    * [Context](#context)
    * [Technical Details](#technical-details)
        * [Database table layout](#database-table-layout)
        * [Design](#design)
        * [Usage](#usage)
        

## General info
Flask-task is a simple project to create APIs for interacting with front-end applications.

## Dependencies
1. Flask 1.1.2
2. Python 3.7
3. Flask-SQLAlchemy 2.4.4
4. SQLAlchemy 1.3.19
5. Sqlite3

## Deploy
1. pip install -r requirements.txt
2. git clone https://github.com/madhuragadikar/Flask-task.git
3. Create db: <ul>
      From Python Console type:
          <li> from models import db</li>
          <li> db.create_all()</li>
    </ul>
4. Add data using Postman/sqlite shell</li>
5. flask run

## Documentation
<h3>Context</h3>
This is a simple project to create APIs to interact with front-end. 


<h3>Technical Details</h3>
<h4>Database table layout</h4>
Models consists of two tables:
<ul>
<b>Customer:</b>
<li>Contains only the customer details: email, first name, last name, gender, address, country, postcode, date of birth.
</ul>
<ul>
<b>Questionnaire:</b>
<li>Contains all questions to be displayed to the customer. </li>
<li>Questions are stored such that they can be fetched depending on user selection on the front-end.</li>
</ul>


Database can be updated using the APIs, Postman or sqlite shell. 


<h4>Design</h4>

Files modified:<br>
<ul>
/
<ul>
<li>app.py</li>
<li>models.py</li>
<li>tables.py</li>
<li>test_skinplus.py</li>
<li>requirements.txt</li>
</ul>
</ul>

<ul>
/templates
<ul>
<li>index.html</li>
<li>signup.html</li>
<li>address.html</li>
<li>welcome.html</li>
<li>questions.html</li>
<li>finish.html</li>
</ul>
</ul>

<h4>Usage</h4>
<p>
<ul>
<li><strong>API view:</strong></li>
</ul>

<b>APIs for Customer database.<b><p>
http://127.0.0.1:5000/customer/1        : display details for customer id '1'<p>
http://127.0.0.1:5000/customer/test     : display details for customer name 'test'<p>
http://127.0.0.1:5000/customers/all     : display all customers<p>

<b>APIs for Questionnaires database:<b><p>
http://127.0.0.1:5000/survey/1          : display details for all questionnaire id 1<p>
http://127.0.0.1:5000/surveys/all       : display all questionnaire<p>
<p>
<b>Process for Customer signup:<b><p>
http://127.0.0.1:5000/signup             : Signup with unique email id. Error if email already exists<p>
http://127.0.0.1:5000/signup/address     : Customer address, postcode and country. Postcode validation done assuming country UK only for demo purposes<p>
http://127.0.0.1:5000/signup/welcome     : Customer first name and last name<p>
http://127.0.0.1:5000/signup/question    : Gender details (Radio box displayed) <p>
http://127.0.0.1:5000/finish             : Customer registration successful <p>
<p>
<b>Details stored in session for demo purposes only. Session is not secure and should be avoided in real deployment projects.<b>
