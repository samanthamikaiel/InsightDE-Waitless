from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from wtforms import Form, StringField, IntegerField
import boto3
import csv
import json
import pandas
from boto3.dynamodb.conditions import Key, Attr
from flask_table import Table, Col

app = Flask(__name__)

## Set up AWS service Parameters##
colnames = ['RID','Name','ZIPCODE']
data = pandas.read_csv ('New_York_City_Restaurant.csv', names=colnames)
zipcode = data.ZIPCODE.tolist()
name = data.Name.tolist()
kinesis = boto3.client('kinesis', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('resturaunt-input')

##Home page##
@app.route ('/')
def index():
    return render_template('home.html')
##About Page##
@app.route ('/about')
def about():
    return render_template('about.html')

##Form for Resturaunts##
class RestaurantForm(Form):
    RID = IntegerField('Resturaunt ID')
    PartySize = IntegerField ('Party Size')
    WaitTime = IntegerField ('Wait Time')
class ResturauntTable(Table):
    PartySize = Col('Party Size')
    WaitTime= Col('Wait Time')
class Item(object):
    def __init__(self, PartySize, WaitTime):
        self.PartySize = PartySize
        self.WaitTime = WaitTime

##Resturaunts Page##
@app.route ('/restaurants', methods=['GET', 'POST'])
def restaurants():
    form = RestaurantForm(request.form)
    return render_template('restaurants.html',form=form)

##Resturaunts Results Page##
@app.route('/restaurantresult', methods=['GET', 'POST'])
def restaurantresult():
    form = RestaurantForm(request.form)
    if request.method == 'POST': ##after information is submitted##
        table = dynamodb.Table('resturaunt-input')
        RID = form.RID.data
        input = {}
        input['ResturauntID'] = RID
        input['Zipcode']= zipcode[RID]
        input['ResturauntName']=name[RID]
        input['PartySize'] = form.PartySize.data
        input['WaitTime'] = form.WaitTime.data
        Data = json.dumps(input) ##turn information into the right type to go to kinesis
        response = kinesis.put_record(StreamName='RI4_fanout', Data=Data, PartitionKey='partitionkey') #put into stream
        response2 = table.query(KeyConditionExpression=Key('ResturauntID').eq(RID), ProjectionExpression =("PartySize,WaitTime")) #show all wait times for the resturaunt
        rtable = response2['Items']
        table = ResturauntTable(rtable)
        table.border = True
    return render_template('restaurantresult.html', table=table)

##Form for Users##
class UserForm(Form):
    Zipcode = IntegerField ('Zip Code')
    PartySize = IntegerField ('Party Size')
class UserTable(Table):
    ResturauntName = Col('Restaurant Name')
    WaitTime= Col('Wait Time')
class Item(object):
    def __init__(self, ResturauntName, WaitTime):
        self.ResturauntName = ResturauntName
        self.WaitTime = WaitTime

##User Page##
@app.route ('/waittime', methods=['GET', 'POST'])
def waittime():
    form = UserForm(request.form)
    return render_template('waittime.html', form=form)

##User Results Page##
@app.route ('/waittimeresults', methods=['GET', 'POST'])
def waittimeresults():
    form = UserForm(request.form)
    if request.method == 'POST': ##after information is submitted##
        table = dynamodb.Table('resturaunt-input')
        zc = form.Zipcode.data
        ps = form.PartySize.data
        input = {}
        input['PartySize']= int(ps)
        input['Zipcode']= str(zc)
        print input
        zip = str (zc)
        response2 = table.scan(FilterExpression=Attr('Zipcode').eq(zip) & Attr('PartySize').eq(ps),ProjectionExpression =("ResturauntName,WaitTime"))

        items = response2['Items']
        print items

        table = UserTable(items)
        table.border = True
    return render_template('waittimeresults.html', table=table)

if __name__ == '__main__':
    app.run(debug=True)
