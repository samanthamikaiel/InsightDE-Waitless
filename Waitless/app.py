from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from wtforms import Form, StringField, IntegerField
import boto3
import csv
import json
import pandas

app = Flask(__name__)

colnames = ['RID','Name','ZIPCODE']
data = pandas.read_csv ('New_York_City_Restaurant.csv', names=colnames)
zipcode = data.ZIPCODE.tolist()
name = data.Name.tolist()
kinesis = boto3.client('kinesis')

@app.route ('/')
def index():
    return render_template('home.html')

@app.route ('/about')
def about():
    return render_template('about.html')

class RestaurantForm(Form):
    RID = IntegerField('Resturaunt ID')
    PartySize = IntegerField ('Party Size')
    WaitTime = IntegerField ('Wait Time')

@app.route ('/restaurants', methods=['GET', 'POST'])
def restaurants():
    form = RestaurantForm(request.form)
    if request.method == 'POST':
        RID = form.RID.data
        input = {}
        input['ResturauntID'] = RID
        input['Zipcode']= zipcode[RID]
        input['ResturauntName']=name[RID]
        input['PartySize'] = form.PartySize.data
        input['WaitTime'] = form.WaitTime.data
        Data = json.dumps(input)
        response = kinesis.put_record(StreamName='RI4_fanout', Data=Data, PartitionKey='partitionkey')
        return jsonify(restaurantdata=Data)
        return redirect(url_for('waittimedata', form=form))
    return render_template('restaurants.html', form=form)

@app.route ('/restaurantdata')
def restaurantdata():
    return render_template('restaurantdata.html')

class UserForm(Form):
    Zipcode = IntegerField ('Zip Code')
    PartySize = IntegerField ('Party Size')

@app.route ('/waittime', methods=['GET', 'POST'])
def waittime():
    i=1;
    form = UserForm(request.form)
    if request.method == 'POST':
        i=i+1;
    
        input = {}
        input['UserID'] = request.remote_addr
        input['PartySize']=form.PartySize.data
        input['Zipcode']=form.Zipcode.data
        Data = json.dumps(input)
        print Data
        response = kinesis.put_record(StreamName='UI4', Data=Data, PartitionKey='partitionkey')
        
        shard_id = 'shardId-000000000003'
        pre_shard_it = kinesis.get_shard_iterator(StreamName='UI4', ShardId=shard_id, ShardIteratorType='LATEST')
        shard_it = pre_shard_it ['ShardIterator']
        out = kinesis.get_records(ShardIterator=shard_it, Limit=1000)
        print response
        #return jsonify(waittimedata=Data)
        return redirect(url_for('waittimedata'))
    return render_template('waittime.html', form=form)

@app.route ('/waittimedata')
def waittimedata():
    return render_template('waittimedata.html')

if __name__ == '__main__':
    app.run(debug=True)

