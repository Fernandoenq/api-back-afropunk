import os
import json

with open(os.path.join(os.getcwd(), 'Application', 'appsettings.json'), 'r') as app_settings:
    app_settings = json.load(app_settings)


class Configuration:
    host = app_settings["ConnectionString"]["Host"]
    user = app_settings["ConnectionString"]["User"]
    password = app_settings["ConnectionString"]["Password"]
    database = app_settings["ConnectionString"]["Database"]

    aws_access_key_id = app_settings["AwsConfiguration"]["AwsAccessKeyId"]
    aws_secret_access_key = app_settings["AwsConfiguration"]["AwsSecretAccessKey"]
    region_name = app_settings["AwsConfiguration"]["RegionName"]
    bucket_name = app_settings["AwsConfiguration"]["BucketName"]
