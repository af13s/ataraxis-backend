#constants.py

import json

API_URL = "https://z769th3to5.execute-api.us-east-1.amazonaws.com/dev"

time_format = "ISO 8601"

#AWS CREDENTIALS
# AWS_ACCESS_KEY_ID='AKIA2EWPK2SS5QAFPT5F'
# AWS_SECRET_ACCESS_KEY = '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'

AWS_ACCESS_KEY_ID='AKIA2EWPK2SSZVRE734J'
AWS_SECRET_ACCESS_KEY = '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'
REGION_NAME='us-east-1'

#USER POOL INFO
USER_POOL_ID= 'us-east-1_L7p78Das9'
APP_CLIENT_ID = '3kv0b17tnq3udjd9ifeuuj0sjo'
ACCOUNT_ID = '697293264037'

# IDENTITY POOL
IDENTITY_POOL_ID = 'us-east-1:e131a431-e062-489a-a474-be29c1785e84'

APP_URL='https://ataraxis.auth.us-east-1.amazoncognito.com'


tablename = {
	"u": "users",
	"e" : "events"
}


"""
json structure

{
{
	"e1": {
	"EventId": "e51234",
	"EventName": "TEST EVENT 1",
	"EventStart": "900PM",
	"EventEnd": "1000PM",
	"eventdate": "06-03-2019",
	"city": "Tallahassee",
	"address": "Landis",
	"summary": "Summer Welcome Back",
	"description": "A student get together held on-campus in landis"
	},
	 "e2":
	 {
	"EventId": "e51235",
	"EventName": "TEST EVENT 2",
	"EventStart": "1000PM",
	"EventEnd": "1100PM",
	"eventdate": "06-03-2019",
	"city": "Tallahassee",
	"address": "Landis",
	"summary": "Summer Welcome Back Part 2",
	"description": "A student get together held on-campus in landis"
	},
	"e3":
	 {
	"EventId": "e51236",
	"EventName": "TEST EVENT 3",
	"EventStart": "1100PM",
	"EventEnd": "1200PM",
	"eventdate": "06-04-2019",
	"city": "Tallahassee",
	"address": "Landis",
	"summary": "Summer Welcome Back Part 2",
	"description": "A student get together held on-campus in landis"
	}
}
"""

userFields = {
	"userid": str,
	"firstname": str,
	"lastname": str,
	"biography": str,
	"age": int,
	"gender": str,
	"phone": str,
	"email": str,
}

eventFields = {
	"EventId": str,
	"EventName": str,
	"EventStart": str,
	"EventEnd": str,
	"eventdate": str,
	"city": str,
	"address": str,
	"summary": str,
	"description": str,
	#"isPublic",
	#"capacity",
}