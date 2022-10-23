from email.policy import default
import json
from unicodedata import name
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
# from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from pytz import timezone
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from flask_migrate import Migrate
#from forms import *
from jinja2.utils import markupsafe
from markupsafe import Markup
markupsafe.Markup()
Markup('')

app = Flask(__name__)
app.secret_key = "Ife Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:root@localhost:5432/crud'
SQLALCHEMY_TRACK_MODIFICATIONS = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Data(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100), nullable = False)
	email = db.Column(db.String(100), nullable = False)
	phone = db.Column(db.String(100), nullable = False)
#creating class constructor
	def __init__(self, name, email, phone):
		self.name = name
		self.email = email
		self.phone = phone
		 
#GETTING DATA FROM DATABASE
@app.route('/')
def Index():
	all_data = Data.query.all() #remember the Data model///i am getting all Data Table and storing it into a variable
	return render_template("index.html", employees = all_data) # sending the data to index.html for viewstate using employees 
	#(we will refer to this in HTML view#TABLE AND UPDATE SINCE THEY BOTH USE VIEW) variable


#INSERTING DATA INTO DATA BASE
@app.route('/insert', methods = ['POST']) #routing to insert function() ROUTING makes it possible to call it in HTML
def insert(): #creating insert function 
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		phone = request.form['phone']

		my_data = Data(name,email,phone) #Data is the model name
		db.session.add(my_data)
		db.session.commit()

		flash("New Employee added succesfully") #MESSAGE TO THE USER
		return redirect(url_for('Index')) #GO BACK TO INDEX

		# or
		# db.session.add(Data(name,email,phone))
		# db.session.commit()
#INSERTING DATA INTO DATA BASE ends

#UPDATING DATA INTO DATA BASE
@app.route('/update', methods = ['GET', 'POST']) #creating update method  #routing to update function() ROUTING makes it possible to call it in HTML
def update():
	if request.method == 'POST':
		my_data = Data.query.get(request.form.get('id'))
		my_data.name = request.form['name']
		my_data.email = request.form['email']
		my_data.phone = request.form['phone']

		db.session.commit()
		flash(" Employee updated succesfully") #MESSAGE TO THE USER
		return redirect(url_for('Index'))
#UPDATING DATA INTO DATA BASE ends 

#DELETING DATA FROM DATA BASE
@app.route('/delete/<id>/', methods = ['GET', 'POST']) #creating update method  #routing to update function() ROUTING makes it possible to call it in HTML
def delete(id):
	my_data = Data.query.get(id)
	db.session.delete(my_data)
	db.session.commit()
	flash(" Employee with id deleted succesfully") #MESSAGE TO THE USER
	return redirect(url_for('Index'))
#DELETING DATA FROM DATA BASE

if __name__ == "__main__":
	app.run(debug=True)

	#you only need to edit your HTML for VIEW 