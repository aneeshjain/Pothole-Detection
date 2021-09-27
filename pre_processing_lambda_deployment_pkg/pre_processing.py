import json
import numpy as np
import boto3
import pandas as pd
import io
import math

s3 = boto3.client('s3')


def lambda_handler(event, context):
    # TODO implement
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    target_bucket = "pothole-data-pre-processed"
    #print(bucket, key)
    obj = s3.get_object(Bucket = bucket, Key = key)
    dataFullCombined = pd.read_csv(io.BytesIO(obj['Body'].read()))
    #rows = obj['Body'].read().decode('utf-8').split()
    
    #print(df.head(5))
    dataFullCombined.replace(" ",np.nan,inplace=True)
    dataFullCombined['x_acc'].replace(0,np.nan,inplace=True)
    dataFullCombined['y_acc'].replace(0,np.nan,inplace=True)
    dataFullCombined['z_acc'].replace(0,np.nan,inplace=True)
    dataFullCombined['x_gyro'].replace(0,np.nan,inplace=True)
    dataFullCombined['y_gyro'].replace(0,np.nan,inplace=True)
    dataFullCombined['z_gyro'].replace(0,np.nan,inplace=True)
    
    
    
    #dataFullCombined['Pothole'].fillna(0,inplace=True)
    
    dataFullCombined['speed'].fillna(method='ffill',inplace=True)
    dataFullCombined['latitude'].fillna(method='ffill',inplace=True)
    dataFullCombined['longitude'].fillna(method='ffill',inplace=True)
    
    
    
    dataFullCombined.fillna(method='bfill',inplace=True)
    
    columnNames=['Time','x_mean_acc','y_mean_acc','z_mean_acc','x_mean_gyro','y_mean_gyro','z_mean_gyro','mean_speed','x_std_acc','y_std_acc','z_std_acc','x_std_gyro','y_std_gyro','z_std_gyro','std_speed','x_max_acc','y_max_acc','z_max_acc','x_max_gyro','y_max_gyro','z_max_gyro','x_min_acc','y_min_acc','z_min_acc','x_min_gyro','y_min_gyro','z_min_gyro','latitude','longitude']
    
    newTotalDataCombined=pd.DataFrame(columns=columnNames,index=range(0,math.ceil(len(dataFullCombined)/4)))
    
    for i in range(0,len(newTotalDataCombined)):
        newTotalDataCombined['Time'][i]=np.mean(dataFullCombined['time stamp'][i*4:(i+1)*4])
        newTotalDataCombined['x_mean_acc'][i]=np.mean(dataFullCombined['x_acc'][i*4:(i+1)*4])
        newTotalDataCombined['y_mean_acc'][i]=np.mean(dataFullCombined['y_acc'][i*4:(i+1)*4])
        newTotalDataCombined['z_mean_acc'][i]=np.mean(dataFullCombined['z_acc'][i*4:(i+1)*4])
        newTotalDataCombined['x_mean_gyro'][i]=np.mean(dataFullCombined['x_gyro'][i*4:(i+1)*4])
        newTotalDataCombined['y_mean_gyro'][i]=np.mean(dataFullCombined['y_gyro'][i*4:(i+1)*4])
        newTotalDataCombined['z_mean_gyro'][i]=np.mean(dataFullCombined['z_gyro'][i*4:(i+1)*4])
        newTotalDataCombined['mean_speed'][i]=np.mean(dataFullCombined['speed'][i*4:(i+1)*4])
        newTotalDataCombined['x_std_acc'][i]=np.std(dataFullCombined['x_acc'][i*4:(i+1)*4])
        newTotalDataCombined['y_std_acc'][i]=np.std(dataFullCombined['y_acc'][i*4:(i+1)*4])
        newTotalDataCombined['z_std_acc'][i]=np.std(dataFullCombined['z_acc'][i*4:(i+1)*4])
        newTotalDataCombined['x_std_gyro'][i]=np.std(dataFullCombined['x_gyro'][i*4:(i+1)*4])
        newTotalDataCombined['y_std_gyro'][i]=np.std(dataFullCombined['y_gyro'][i*4:(i+1)*4])
        newTotalDataCombined['z_std_gyro'][i]=np.std(dataFullCombined['z_gyro'][i*4:(i+1)*4])
        newTotalDataCombined['std_speed'][i]=np.std(dataFullCombined['speed'][i*4:(i+1)*4])
        newTotalDataCombined['x_max_acc'][i]=np.max(dataFullCombined['x_acc'][i*4:(i+1)*4])
        newTotalDataCombined['y_max_acc'][i]=np.max(dataFullCombined['y_acc'][i*4:(i+1)*4])
        newTotalDataCombined['z_max_acc'][i]=np.max(dataFullCombined['z_acc'][i*4:(i+1)*4])
        newTotalDataCombined['x_max_gyro'][i]=np.max(dataFullCombined['x_gyro'][i*4:(i+1)*4])
        newTotalDataCombined['y_max_gyro'][i]=np.max(dataFullCombined['y_gyro'][i*4:(i+1)*4])
        newTotalDataCombined['z_max_gyro'][i]=np.max(dataFullCombined['z_gyro'][i*4:(i+1)*4])
        newTotalDataCombined['x_min_acc'][i]=np.min(dataFullCombined['x_acc'][i*4:(i+1)*4])
        newTotalDataCombined['y_min_acc'][i]=np.min(dataFullCombined['y_acc'][i*4:(i+1)*4])
        newTotalDataCombined['z_min_acc'][i]=np.min(dataFullCombined['z_acc'][i*4:(i+1)*4])
        newTotalDataCombined['x_min_gyro'][i]=np.min(dataFullCombined['x_gyro'][i*4:(i+1)*4])
        newTotalDataCombined['y_min_gyro'][i]=np.min(dataFullCombined['y_gyro'][i*4:(i+1)*4])
        newTotalDataCombined['z_min_gyro'][i]=np.min(dataFullCombined['z_gyro'][i*4:(i+1)*4])
        newTotalDataCombined['latitude'][i]=np.max(dataFullCombined['latitude'][i*4:(i+1)*4])
        newTotalDataCombined['longitude'][i]=np.max(dataFullCombined['longitude'][i*4:(i+1)*4])
    
    csv_buffer = io.StringIO()
    #print(type(csv_buffer))
    newTotalDataCombined.to_csv(csv_buffer)
    s3_resource = boto3.resource('s3')
    s3_resource.Object(target_bucket, 'pre_processed.csv').put(Body=csv_buffer.getvalue())
        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
