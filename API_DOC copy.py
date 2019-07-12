#API DOC

BASE_URL = 'https://z769th3to5.execute-api.us-east-1.amazonaws.com/dev'


## POST REQUESTS ##

SIGN_IN = '/signIn'

EXAMPLE REQUEST = {

	"User": "+19543984645",
	"Pass": "password"
}

RESPONSE = {
	"AuthenticationResult": {
		"AccessToken": "STRING",
		"ExpiresIn": 3600, 
		"TokenType": "Bearer", 
		"RefreshToken": "STRING",
		"IdToken" : "STRING",
		}
	}


SIGN_UP = '/signUp'

EXAMPLE REQUEST = {

	"User": "+19543984645",
	"Pass": "password",
	"Email": "andrewflorial@gmail.com",
	"Name": "Andrew Florial",
	"Gender": "male",
	"Phone": "+19543984645"

}


CONFIRM_SIGN_UP = '/confirmSignUp'

EXAMPLE REQUEST = {
	"Username" : "+19543984645",
	"ConfirmationCode": "987019"
}

RESPONSE = {
	'ResponseMetadata':
	{
		'RequestId': 'e38d3616-8997-11e9-bccc-49dec0da1541', 
		'HTTPStatusCode': 200, 
		'HTTPHeaders': 
		{
			'date': 'Sat, 08 Jun 2019 02:48:26 GMT', 
			'content-type': 'application/x-amz-json-1.1', 
			'content-length': '2', 
			'connection': 'keep-alive', 
			'x-amzn-requestid': 'e38d3616-8997-11e9-bccc-49dec0da1541'
		}, 

		'RetryAttempts': 0
	}
}


UPDATE_EVENT = '/updateEvent'

EXAMPLE REQUEST = {
	"Key":{
        "EventId": "e51234",
        "EventStart": "900PM"
    },
    "UpdateVars":[
    "description",
    "EventName"
    ],
    "ExpressionAttributeValues":[
        "This is an event description to be  viewed",
        "NEW NAME"
    ]
    
}


## GET REQUESTS ##

# NO CREDENTIALS REQUIRED

#GET INDIVIDUAL EVENT DETAILS
GET_EVENT = '/getEvent/<EVENT_ID>/<TIME>'
EXAMPLE = '/getEvent/e51234/900AM'

# GET ALL EVENTS FOR PREVIEW SCROLL
GET_ALL_EVENTS = '/getAllEvents'

RESPONSE = [{

	"EventId": "realevent1",
	"EventName": "International Coffee Hour",
	"EventStart": "5:00PM",
	"EventEnd": "6:30PM",
	"city": "Tallahassee",
	"locationname" : "Global and Multicultural Engagement Building (GME), The Globe Dining Room"
	"address": "110 S Woodward Ave., Tallahassee, FL",
	"summary": "The Globe Dining Room for refreshments from a featured culture",
	"description": "Join us every Friday from 5-6:30 p.m. in The Globe Dining Room for refreshments from a featured culture and interact with students, scholars, and faculty from around the world. This event is open to all current FSU students, faculty and staff.",
"img-url" : "https://images.localist.com/photos/503059/huge/c04d9c39e5d04df9fc1637a65004a01c4159e6f5.jpg"
	},

	"""more items"""
	]
# CREDENTIALS REQUIRED







