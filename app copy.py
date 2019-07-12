from flask import Flask
from flask import Response
from flask_cors import CORS
from flask import request
import boto3
import json
import constants
from boto3.dynamodb.conditions import Key, Attr
import dateutil.parser
from datetime import datetime
from datetime import timedelta
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration
import random

sentry_sdk.init("https://04164b20f97546b7b6b36230d923302c:da003222489e4a45b2c5c96518d8671c@sentry.io/1498534", integrations=[AwsLambdaIntegration(),FlaskIntegration()])

def admin_access_session():
    session = boto3.Session(
        aws_access_key_id=constants.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=constants.AWS_SECRET_ACCESS_KEY,
        region_name='us-east-1'
    )

    return session
    

def dynambo_admin_access_session():
    session = admin_access_session()
    dynamodb = session.resource('dynamodb')

    return dynamodb

#Table commands for dynamodb
#https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html 

# https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-device-tracking.html

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Server Online'

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

# SIGN IN
@app.route('/signIn', methods=['POST'])
def signIn():

    AuthDict= json.loads(request.data)

    USER = AuthDict['User']
    PASS = AuthDict['Pass']
    
    client = boto3.client(
    'cognito-idp',
    aws_access_key_id=constants.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=constants.AWS_SECRET_ACCESS_KEY,
    region_name=constants.REGION_NAME)

    response = auth = client.initiate_auth(
    ClientId = constants.APP_CLIENT_ID,
    AuthFlow='USER_PASSWORD_AUTH',
    AuthParameters={'USERNAME':USER,'PASSWORD':PASS})

    return str(response).replace("'", '"')

#SIGN UP
@app.route('/signUp', methods=['POST'])
def signUp():
    AuthDict= json.loads(request.data)

    USER = AuthDict['User']
    PASS = AuthDict['Pass']

    EMAIL = AuthDict['Email']
    PHONE = AuthDict['Phone']
    NAME = AuthDict['Name']
    GENDER = AuthDict['Gender']
    
    client = boto3.client('cognito-idp',region_name=constants.REGION_NAME)

    response = client.sign_up(
    ClientId=constants.APP_CLIENT_ID,
    Username=USER,
    Password=PASS,
    UserAttributes=[
        {
            'Name': 'name',
            'Value': NAME,
        },
        {
            'Name': 'email',
            'Value': EMAIL,
        },
        {
            'Name': 'gender',
            'Value': GENDER,
        },
        {
            'Name': 'phone_number',
            'Value': PHONE,
        },
    ],
    # ValidationData=[
    #     {
    #         'Name': 'admin',
    #         'Value': 'newuser'
    #     },
    # ],
    # AnalyticsMetadata={
    #     'AnalyticsEndpointId': 'string'
    # },
    # UserContextData={
    #     'EncodedData': 'string'
    # }
    )

    return str(response).replace("'", '"')

# CONFIRM SIGN UP
@app.route('/confirmSignUp', methods=['POST'])
def confirmsignUp():

    client = boto3.client('cognito-idp',region_name=constants.REGION_NAME)

    AuthDict= json.loads(request.data)

    Username = AuthDict["Username"]
    ConfirmationCode = AuthDict["ConfirmationCode"]

    response = client.confirm_sign_up(
    ClientId=constants.APP_CLIENT_ID,
    Username=Username,
    ConfirmationCode=ConfirmationCode,
    ForceAliasCreation=False
    # AnalyticsMetadata={
    #     'AnalyticsEndpointId': 'string'
    # },
    # UserContextData={
    #     'EncodedData': 'string'
    # }
    )
    print(response)

    return str(response).replace("'", '"')

@app.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0

## COMMON APIS ##
@app.route('/addEntry', methods=['POST'])
def addEntry():

    entryDict= json.loads(request.data)

    # Auth = getAuth(entryDict)
    # dynamodb = start_dynambodb_session(Auth)

    dynamodb = dynambo_admin_access_session()

    
    # for key in entryDict:
    #     entryDict[key] = userField[key](entryDict[key])

    for key in entryDict["Entries"]:
        table = dynamodb.Table(constants.tablename[key[0]])
        response = table.put_item(Item=entryDict["Entries"][key])


    return str(response).replace("'", '"')


## turn into get event details
@app.route('/getEvent/<EventId>/<time>', methods=['GET'])
def getEvent(EventId,time):

    # entryDict= json.loads(request.data)

    # Auth = getAuth(entryDict)
    # dynamodb = start_dynambodb_session(Auth)

    dynamodb = dynambo_admin_access_session()

    table = dynamodb.Table("experiences")
    response = table.get_item(Key={
    'EventId': EventId,
    "EventStart": time})

    return str(response).replace("'", '"')

@app.route('/deleteEvent/<EventId>/<time>', methods=['GET'])
def deleteEvent(EventId,time):

    # entryDict= json.loads(request.data)

    # Auth = getAuth(entryDict)
    # dynamodb = start_dynambodb_session(Auth)

    dynamodb = dynambo_admin_access_session()

    table = dynamodb.Table("experiences")
    response = table.delete_item(Key={
    'EventId': EventId,
    "EventStart": time})

    return str(response).replace("'", '"')


# def getPosition(address):

#     geolocator = Nominatim(user_agent="swift_ui")
#     location = geolocator.geocode(address)
#     print(location.address)

#     return location.latitude, location.longitude


@app.route('/getHeaderPhotos/', methods=['GET'])
def getHeaderPhotos():

    dynamodb = dynambo_admin_access_session()
    table = dynamodb.Table("headerimages")
    response = table.scan()
    urls = response["Items"]
    urlList = []

    nums = {}

    for _ in range(5):
        try:
            rand = random.randint(0, len(urls)-1)
            if rand not in nums:
                urlList.append(urls[rand]["url"])
                nums.add(rand)
        except:
            print(rand)

    resp = Response(response=json.dumps(urlList),content_type="application/json")

    return resp


#Turn into get few details: title, time, location, summary
@app.route('/getAllEvents/', methods=['GET'])
@app.route('/getAllEvents/<timeframe>', methods=['GET'])
def getAllEvents(timeframe=False):

    # entryDict= json.loads(request.data)

    # Auth = getAuth(entryDict)
    # dynamodb = start_dynambodb_session(Auth)

    dynamodb = dynambo_admin_access_session()

    table = dynamodb.Table("experiences")
    response = table.scan()
    newlist = response["Items"]
    newlist = sorted(newlist, key=lambda k: k['EventStart'])

    # for eventobj in newlist:
    #     if "latitude" not in eventobj or "longitude" not in eventobj:
    #         eventobj["latitude"] , eventobj["longitude"] = getPosition(eventobj["EventAddress"])

    temp = []
    for event in newlist:
        keyDate = dateutil.parser.parse(event['EventStart'])
        if keyDate >= datetime.now()-timedelta(hours=2):
            temp.append(event)
    
    newlist = temp

    if timeframe == 'week':
        weekLimit = datetime.today()+timedelta(days=7)
        for i,key in enumerate(newlist):
            keyDate = dateutil.parser.parse(key['EventStart'])
            if keyDate > weekLimit:
                del newlist[i:]
                break

    if timeframe == 'day':
        dayLimit = datetime.now()+timedelta(hours=12)
        for i,key in enumerate(newlist):
            keyDate = dateutil.parser.parse(key['EventStart'])
            if keyDate > dayLimit:
                del newlist[i:]
                break
                
    resp = Response(response=json.dumps(newlist),content_type="application/json")

    return resp




@app.route('/getAllEventsBETA/<timeframe>', methods=['GET'])
@app.route('/getAllEventsBETA', methods=['GET'])
def getAllEventsBETA(timeframe=None):
    
    # Rocket / Details

    if timeframe == "week" or timeframe == "day":
        events = getAllEvents(timeframe)
    else:
        events = getAllEvents()

    newlist = []

    count = 0

    for event in events.get_json():
        testdictt = json.loads(testdict)
        testdictt["mission_name"] = event["EventName"]
        testdictt["flight_number"] = count
        testdictt["launch_date_utc"] = event["EventStart"]
        testdictt["latitude"] = event["Latitude"]
        testdictt["longitude"] = event["Longitude"]
        # testdictt["flight_number"] = event["EventLocationName"]
        try:   
            testdictt["address"]= event["EventAddress"]
        except:
            pass
            # print("no EventAddress using default")
        try:   
            testdictt["rocket"]["rocket_phone"] = event["phone"]
        except:
            pass
            # print("no phone using default")
        try:   
            testdictt["rocket"]["rocket_website"] = event["website"]
        except:
            pass
            # print("no website using default")

        testdictt['links']['flickr_images'] = [event["ImageUrl"]]
        testdictt["launch_site"]["site_name"] = event["EventLocationName"]
        testdictt["details"] = event["EventDescription"]
        newlist.append(testdictt)
        count+=1
        
    
    resp = Response(response=json.dumps(newlist),content_type="application/json")

    return resp

def getAuth(response):

    if "AuthenticationResult" in response:
        Auth = response
    else:
        Auth = None

    return Auth


def start_dynambodb_session(Auth=None):

    client = boto3.client('cognito-identity',region_name=constants.REGION_NAME)
    
    session = None

    if Auth==None or not Auth:
        iid = response = client.get_id(AccountId=constants.ACCOUNT_ID, IdentityPoolId=constants.IDENTITY_POOL_ID)
        cred  = response = client.get_credentials_for_identity(IdentityId=iid['IdentityId'])

        session = boto3.Session(
        aws_access_key_id= cred['Credentials']['AccessKeyId'],
        aws_secret_access_key=cred['Credentials']['SecretKey'],
        aws_session_token =cred['Credentials']['SessionToken'])
        dynamodb = session.resource('dynamodb',region_name='us-east-1')

    else:

        response = iid = client.get_id(
        AccountId=constants.ACCOUNT_ID,
        IdentityPoolId=constants.IDENTITY_POOL_ID,
        Logins={
        'cognito-idp.us-east-1.amazonaws.com/{}'.format(constants.USER_POOL_ID): Auth['AuthenticationResult']['IdToken']
        })

        print("get_id response", response)
        print()

        cred  = response = client.get_credentials_for_identity(
        IdentityId=iid['IdentityId'],
        Logins={
        'cognito-idp.us-east-1.amazonaws.com/{}'.format(constants.USER_POOL_ID): Auth['AuthenticationResult']['IdToken']
        })

        if datetime.today()+timedelta(seconds=300) > cred["Credentials"]["Expiration"]:
            cred = refreshtoken(Auth)

        cred = format_cred(cred)

        session = boto3.Session(
        aws_access_key_id= cred['AccessKeyId'],
        aws_secret_access_key=cred['SecretKey'],
        aws_session_token =cred['SessionToken'])
        dynamodb = session.resource('dynamodb',region_name='us-east-1')


    return dynamodb


def refreshtoken(auth):
    client = boto3.client(
    'cognito-idp',
    aws_access_key_id=constants.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=constants.AWS_SECRET_ACCESS_KEY,
    region_name=constants.REGION_NAME
    )

    response = newcred = client.initiate_auth(
    ClientId = constants.APP_CLIENT_ID,
    AuthFlow='REFRESH_TOKEN_AUTH',
    AuthParameters={
        "REFRESH_TOKEN": auth["AuthenticationResult"]["RefreshToken"]
    })

    return newcred

def format_cred(cred):
    temp = {}
    temp["AccessKeyId"] = cred["Credentials"]["AccessKeyId"]
    temp["SecretKey"] = cred["Credentials"]["SecretKey"]
    temp["SessionToken"] = cred["Credentials"]["SessionToken"]
    # temp["Expiration"] = cred["Credentials"]["Expiration"].strftime('%Y-%m-%d:%X')

    print(temp["Expiration"])

    return temp

#Updating an element
@app.route('/updateEvent', methods=['POST'])
def updateEvent():

    dynamodb = dynambo_admin_access_session()
    table = dynamodb.Table("experiences")

    entryDict= json.loads(request.data)
    key = entryDict["Key"]
    UE = "SET "

    for var in entryDict["UpdateVars"]:
        UE += "{} = :{}, ".format(var,var)

    UE = UE[:-2]

    EAV={}

    for i in range(len(entryDict["UpdateVars"])):
        EAV[":"+entryDict["UpdateVars"][i]] = entryDict["ExpressionAttributeValues"][i]


    response = table.update_item(Key=key, UpdateExpression=UE, ExpressionAttributeValues=EAV)

    return str(response).replace("'", '"')



# @app.route('/SeverPostTest', methods=["POST"])
# def SeverPostTest():

#     #accepting the data
#     print("raw",request.data)

#     #parse the data to a python dictionary
#     datapydict = json.loads(request.data)

#     #convert the data to json string
#     datastring = json.dumps(request.data)

#     print("py dict",datastore)
#     return str(type(request.data))

testdict = """{
        "flight_number": 83,
        "mission_name": "Amos-17",
        "mission_id": [],
        "latitude": "0",
        "longitude": "0",
        "launch_year": "2019",
        "launch_date_unix": 1561939200,
        "launch_date_utc": "2019-07-01T00:00:00.000Z",
        "launch_date_utc_end": "2019-07-01T00:00:00.000Z",
        "launch_date_local": "2019-06-30T20:00:00-04:00",
        "address" : "700 north woodward ave Apt 902, Tallahassee FL",
        "is_tentative": true,
        "tentative_max_precision": "hour",
        "tbd": true,
        "launch_window": null,
        "rocket": {
            "rocket_id": "falcon9",
            "rocket_phone" : "9543984645",
            "rocket_website": "www.fsu.edu",
            "rocket_name": "Andrew F",
            "rocket_type": "FT",
            "first_stage": {
                "cores": [
                    {
                        "core_serial": null,
                        "flight": null,
                        "block": null,
                        "gridfins": null,
                        "legs": null,
                        "reused": null,
                        "land_success": null,
                        "landing_intent": null,
                        "landing_type": null,
                        "landing_vehicle": null
                    }
                ]
            },
            "second_stage": {
                "block": null,
                "payloads": [
                    {
                        "payload_id": "Amos-17",
                        "norad_id": [],
                        "reused": false,
                        "customers": [
                            "Spacecom"
                        ],
                        "nationality": "Israel",
                        "manufacturer": "Boeing Satellite Systems",
                        "payload_type": "Satellite",
                        "payload_mass_kg": 5500,
                        "payload_mass_lbs": 12125.42,
                        "orbit": "GTO",
                        "orbit_params": {
                            "reference_system": "geocentric",
                            "regime": "geostationary",
                            "longitude": 17,
                            "semi_major_axis_km": null,
                            "eccentricity": null,
                            "periapsis_km": null,
                            "apoapsis_km": null,
                            "inclination_deg": null,
                            "period_min": null,
                            "lifespan_years": 15,
                            "epoch": null,
                            "mean_motion": null,
                            "raan": null,
                            "arg_of_pericenter": null,
                            "mean_anomaly": null
                        }
                    }
                ]
            },
            "fairings": {
                "reused": false,
                "recovery_attempt": false,
                "recovered": false,
                "ship": null
            }
        },
        "ships": [],
        "telemetry": {
            "flight_club": null
        },
        "launch_site": {
            "site_id": "ksc_lc_39a",
            "site_name": "KSC LC 39A",
            "site_name_long": "Kennedy Space Center Historic Launch Complex 39A"
        },
        "launch_success": null,
        "links": {
            "mission_patch": null,
            "mission_patch_small": null,
            "reddit_campaign": null,
            "reddit_launch": null,
            "reddit_recovery": null,
            "reddit_media": null,
            "presskit": null,
            "article_link": null,
            "wikipedia": null,
            "video_link": null,
            "youtube_id": null,
            "flickr_images": []
        },
        "details": null,
        "upcoming": true,
        "static_fire_date_utc": null,
        "static_fire_date_unix": null,
        "timeline": null,
        "crew": null
    }"""

