# hiring_tweets_to_S3_using_airflow

Purpose:
There are quite a handful of jobs announced on twitter that are not on linkedin. this is an attempt to curate Dataengineering and Datascience related hiring jobs in a daily CSV. Please feel free to edit it for other job roles as well / adding more hashtag constraints (ex: #remote etc)

There are two main files in this repo.
1. tweets_hiring.py : uses twitter API and collects tweets that have selected hashtags (like #hiring AND one of: #data #datascientist #dataengineering)
2. hiring_tweets_dag.py : the airflow DAG file for this ETL process

Destination: S3 bucket -> new file each day

The code also supports local csv creation (and daily append) and can be run using local machine's cron jobs. sample output .csv files are added in the repo as well

Token:
Add BEARER_TOKEN (from twitter) to environment

Common pitfalls / fixes:
1. check airflow.cfg for DAG name mismatch
2. t2.micro isnt enough. recommended is 4GB RAM. t3a.medium is convenient (roughly $0.05 USD/hour)
