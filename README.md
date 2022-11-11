# hiring_tweets_to_S3_using_airflow

There are two main files in this repo.
1. tweets_hiring.py : uses twitter API and collects tweets that have selected hashtags (like #hiring AND one of: #data #datascientist #dataengineering)
2. hiring_tweets_dag.py : the airflow DAG file for this ETL process

Destination: S3 bucket -> new file each day

The code also supports local csv creation (and daily append) and can be run using local machine's cron jobs. sample output .csv files are added in the repo as well
