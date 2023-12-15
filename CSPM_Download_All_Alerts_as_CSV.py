import requests
import json
import csv
import pandas as pd
import time

### Prisma Cloud Professional Services
### Created on December 4, 2023
### Created by llatorre@paloaltonetworks.com
### Version: 2023.12.15.B

"""
API(s):
https://pan.dev/prisma-cloud/api/cspm/submit-an-alert-csv-download-job/
https://pan.dev/prisma-cloud/api/cspm/get-alert-csv-job-status/
https://pan.dev/prisma-cloud/api/cspm/download-alert-csv/
"""


## Set-up your Env
## Create and Manage Access Keys --> https://docs.prismacloud.io/en/classic/cspm-admin-guide/manage-prisma-cloud-administrators/create-access-keys
PCAccessKey="<YOUR-ACCESS-KEY>"
PCSecretKey="<YOUR-SECRET-KEY>" 
### Prisma Cloud API URLs --> https://pan.dev/prisma-cloud/api/cspm/api-urls/
### set api based on tenant (api3, api2, api)
CSPMApi = "<YOUR-API-TENANT>" 

### Retrieve a token from the CSPM Login alt text endpoint with your CSPM user credentials
### https://pan.dev/prisma-cloud/api/cwpp/access-api-saas/#accessing-the-api-using-prisma-cloud-login-token

login_url = f"https://{CSPMApi}.prismacloud.io/login"

login_payload = json.dumps({
  "password": PCSecretKey,
  "username": PCAccessKey
})
login_headers = {
  'Content-Type': 'application/json'
}

auth_token = requests.request("POST", login_url, headers=login_headers, data=login_payload)
token = auth_token.json()["token"]

### Submit an Alert CSV download job:

cspm_request = f"https://{CSPMApi}.prismacloud.io/alert/csv"

cspm_request_payload = "{\n  \"filters\":[\n\t{\"name\":\"timeRange.type\",\"operator\":\"=\",\"value\":\"ALERT_STATUS_UPDATED\"},\n\t{\"name\":\"alert.status\",\"operator\":\"=\",\"value\":\"open\"},\n\t{\"name\":\"policy.severity\",\"operator\":\"=\",\"value\":\"critical\"}\n  ],\n  \"timeRange\":{\n      \"type\":\"to_now\",\n      \"value\":\"epoch\"}\n}"
cspm_request_headers = {
  'x-redlock-auth': token,
  'Content-Type': 'application/json',
  'Accept': 'application/json; charset=UTF-8'
}

response_cspm = requests.request("POST", cspm_request, headers=cspm_request_headers, data=cspm_request_payload)
response_cspm_id = response_cspm.json()['id']

### For troubleshooting
#print(response_cspm.text)
#print(response_cspm_id)

### Wait for 3 minutes
time.sleep(180)

### Download file

cspm_request_csv = f"https://{CSPMApi}.prismacloud.io/alert/csv/{response_cspm_id}/download"

cspm_request_payload_csv = {}
cspm_request_headers_csv = {
  'x-redlock-auth': token,
}

response_cspm_csv = requests.request("GET", cspm_request_csv, headers=cspm_request_headers_csv, data=cspm_request_payload_csv)

### For troubleshooting
#print(response_cspm_csv.text)

### Create a new CSV file  
with open("All_Critical_Alerts.csv", "w") as f:
    f.write(response_cspm_csv.text)
