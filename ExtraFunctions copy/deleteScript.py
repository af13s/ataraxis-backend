from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key, Attr
import json

d = datetime.now()
date = d.isoformat()

print(date)

#https://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html

session = boto3.Session(
    aws_access_key_id='AKIA2EWPK2SSZVRE734J',
    aws_secret_access_key='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',
)
dynamodb = session.resource('dynamodb',region_name='us-east-1')

def deleteEvent(EventId,time):
	table = dynamodb.Table("events")
	result = table.delete_item(Key={
    'EventId': EventId,
    "EventStart": time})
	print(result)
	print("Deletion complete")


def deleteOldEvents():
	table = dynamodb.Table("events")
	result = table.scan(
    FilterExpression=Attr('eventdate').lt(date)
	)

	# result = json.loads(result["Items"])

	for obj in result["Items"]:
		deleteEvent(obj["EventId"],obj["EventStart"])

	print("Events Deleted")

def deleteAllEvents():
	table = dynamodb.Table("events")
	result = table.scan()

	# result = json.loads(result["Items"])

	for obj in result["Items"]:
		deleteEvent(obj["EventId"],obj["EventStart"])

	print("Events Deleted")

deleteOldEvents()

ans = input("Delete All Events (A) , Delete Old Events (O)")

if str(ans) == "A":
	ans2 = input("Are you sure? Yes/N") 
	if str(ans2.lower()) == "yes":
		deleteAllEvents()

if str(ans) == "T":
	ans2 = input("Are you sure? Y/N") 
	if str(ans2.lower()) == "y":
		deleteOldEvents()
