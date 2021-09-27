#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 21 18:57:14 2019

@author: aneesh
"""

import json
import sklearn
import pandas as pd
import pickle
import io
from sklearn.preprocessing import StandardScaler
import boto3

s3 = boto3.client('s3')


def lambda_handler(event, context):
    # TODO implement
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    target_bucket = "pothole-data-inferenced"
    
    obj = s3.get_object(Bucket = bucket, Key = key)
    X_features = pd.read_csv(io.BytesIO(obj['Body'].read()))
    #df2 = X_features
    #print(X_features.dtypes)
    latitudes = X_features['latitude']
    longitudes = X_features['longitude']
    
    del X_features['Time']
    del X_features['Unnamed: 0']
    del X_features['latitude']
    del X_features['longitude']
    #print(list(df2.columns.values))
    
    scaler=StandardScaler().fit(X_features)
    X_features = scaler.transform(X_features)
    
    with open("finalized_model.sav", 'rb') as pickle_file:
        model = pickle.load(pickle_file)
        model.n_jobs = 1
        predictions = model.predict(X_features)
    
    
    
    final = {"Latitudes":latitudes, "Longitudes": longitudes, "Predictions":predictions}
    final = pd.DataFrame(final)
    
    csv_buffer = io.StringIO()
    #print(type(csv_buffer))
    final.to_csv(csv_buffer)
    s3_resource = boto3.resource('s3')
    s3_resource.Object(target_bucket, 'inferenced.csv').put(Body=csv_buffer.getvalue())
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
