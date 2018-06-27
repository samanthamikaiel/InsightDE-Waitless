from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from wtforms import Form, StringField, IntegerField
import boto3
import csv
import json
import pandas
from boto3.dynamodb.conditions import Key, Attr


app = Flask(__name__)

## Set up AWS service Parameters##
colnames = ['RID','Name','ZIPCODE']
data = pandas.read_csv ('New_York_City_Restaurant.csv', names=colnames)
zipcode = data.ZIPCODE.tolist()
name = data.Name.tolist()
kinesis = boto3.client('kinesis')
dynamodb = boto3.resource('dynamodb')
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

##Resturaunts Page##
@app.route ('/restaurants', methods=['GET', 'POST'])
def restaurants():
    form = RestaurantForm(request.form)
    if request.method == 'POST': ##after information is submitted##
        RID = form.RID.data
        input = {}
        input['ResturauntID'] = RID
        input['Zipcode']= zipcode[RID]
        input['ResturauntName']=name[RID]
        input['PartySize'] = form.PartySize.data
        input['WaitTime'] = form.WaitTime.data
        Data = json.dumps(input) ##turn information into the right type to go to kinesis
        response = kinesis.put_record(StreamName='RI4_fanout', Data=Data, PartitionKey='partitionkey') #put into stream
        
        response2 = table.query(KeyConditionExpression=Key('ResturauntID').eq(RID)) #show all wait times for the resturaunt
    
        return jsonify(str(response2))
    return render_template('restaurants.html', form=form)

##Form for Users##
class UserForm(Form):
    Zipcode = IntegerField ('Zip Code')
    PartySize = IntegerField ('Party Size')

##User Page##
@app.route ('/waittime', methods=['GET', 'POST'])
def waittime():
    i=1;
    form = UserForm(request.form)
    if request.method == 'POST': ##after information is submitted##
        i=i+1;
        zc = form.Zipcode.data
        ps = form.PartySize.data
        input = {}
        input['UserID'] = i #request.remote_addr ## UID = IP address
        input['PartySize']=ps
        input['Zipcode']=zc
        Data = json.dumps(input)
        print Data
        response = kinesis.put_record(StreamName='UI8', Data=Data, PartitionKey='partitionkey')

        shard_id = 'shardId-000000000006'
        pre_shard_it = kinesis.get_shard_iterator(StreamName='UI8', ShardId=shard_id, ShardIteratorType='LATEST')
        shard_it = pre_shard_it ['ShardIterator']

        out = kinesis.get_records(ShardIterator=shard_it, Limit=1000)

        for record in out['Records']:
            input = json.loads(record['Data'])
            if input:
                #for ri in input:
                uid = input ['UserID']
                zc = str(input['Zipcode'])
                ps = int(input['PartySize'])
        
            response2 = table.scan(FilterExpression=Attr('Zipcode').eq(zc) & Attr('PartySize').eq(ps))
       
            items = response2['Items']
            Output = json.dumps(str(items))
            print(items)
  
        return jsonify(response)
    
    return render_template('waittime.html', form=form)

@app.route ('/waittimedata')
def waittimedata():
    return render_template('waittimedata.html')

if __name__ == '__main__':
    app.run(debug=True)

