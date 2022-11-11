import requests
import os
import json
import pandas as pd
import csv
from datetime import date, datetime, timedelta
from io import StringIO
import boto3

def bearer_oauth(r):
    bearer_token = os.environ.get("BEARER_TOKEN")
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    #print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def get_tweets(search_url, query_params):
    json_response = connect_to_endpoint(search_url, query_params)
    df = pd.DataFrame(json_response['data'])
    df['link']='https://twitter.com/i/web/status/'+df['id']
    df.drop(['author_id','id','edit_history_tweet_ids'],inplace=True, axis=1)
    return df

def write_to_csv_local(df,csv_file_name):
    file_exists = os.path.isfile(csv_file_name)
    if(file_exists):
        df.to_csv(csv_file_name,mode='a', header=False, index=False)
    else:
        df.to_csv(csv_file_name,mode='a', header=True, index=False)

def write_to_csv_s3(df,s3_bucket_name,csv_file_name):
    file_exists = os.path.isfile(csv_file_name)
    # new file daily 
    csv_buffer = StringIO()
    output_file = df.to_csv(csv_buffer)
    s3_resource = boto3.resource('s3')
    s3_resource.Object(s3_bucket_name, csv_file_name).put(Body=csv_buffer.getvalue())

def get_hiring_tweets_to_s3():
    dtformat = '%Y-%m-%dT%H:%M:%SZ'
    end_time = date.today()
    start_time=end_time - timedelta(days = 1)
    start_time, end_time = start_time.strftime(dtformat), end_time.strftime(dtformat)
    search_url = "https://api.twitter.com/2/tweets/search/recent"
    query_params = {'query': '#hiring (#dataengineering OR #data OR #datascientist) -is:retweet ','start_time': start_time,'end_time': end_time,'tweet.fields': 'created_at','max_results':100,'expansions':'author_id','user.fields':'description'}
    csv_file_name='hiring_tweets.csv'
    s3_bucket_name='kalai-airflow-etl'

    df=get_tweets(search_url, query_params)
    write_to_csv_local(df,csv_file_name)
    csv_file_name = str(date.today())+"_"+csv_file_name # new file daily for S3, not appending
    write_to_csv_s3(df,s3_bucket_name,csv_file_name)

get_hiring_tweets_to_s3()
