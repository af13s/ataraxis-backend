import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QListWidget, QVBoxLayout, QLineEdit, QFormLayout, QPushButton, QCompleter, QPlainTextEdit, QLabel, QHBoxLayout, QMessageBox, QDialog
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui
from geopy.geocoders import Nominatim

import boto3
import random
import constants
import json

import requests

from datetime import datetime

from decimal import Decimal

proList = None
eventObjs = None

class inputdialog(QWidget):
   def __init__(self, parent = None):
      super(inputdialog, self).__init__(parent)

      layout = QFormLayout()

      proList = self.getEvents()

      #https://codeloop.org/pyqt5-simple-project-with-qlistwidget/
      self.list = QListWidget()

      if proList is not None:
         self.list.addItems(proList)
         self.list.setCurrentRow(1)

      print("clicked:" , self.list.currentRow())


      layout.addRow(self.list)

      # self.btn = QPushButton("Refresh")
      # self.btn.clicked.connect(self.refresh)

      self.chart = QLabel(self)

      self.sim = None

      self.Event_ID = QLineEdit()
      self.Event_ID.setPlaceholderText("Event ID")
      self.btn = QPushButton("GEN ID")
      self.btn.clicked.connect(self.genID)
      layout.addRow(self.btn,self.Event_ID)
		
      self.Event_Name = QLineEdit()
      self.Event_Name.setPlaceholderText("Event Name")
      layout.addRow(self.Event_Name)

      self.Date = QLineEdit()
      self.Date.setPlaceholderText("Date")
      self.Time = QLineEdit()
      self.Time.setPlaceholderText("Time")
      layout.addRow(self.Date,self.Time)

      # self.End_Time = QLineEdit()
      # self.End_Time.setPlaceholderText("End Time")
      # layout.addRow(self.End_Time)

      # self.City = QLineEdit()
      # self.City.setPlaceholderText("City")
      # layout.addRow(self.City)

      self.Location_Name= QLineEdit()
      self.Location_Name.setPlaceholderText("Location Name")
      layout.addRow(self.Location_Name)

      self.address = QLineEdit()
      self.address.setPlaceholderText("address")
      layout.addRow(self.address)


      # self.Summary = QLineEdit()
      # self.Summary.setPlaceholderText("Summary")
      # layout.addRow(self.Summary)

      self.img_url = QLineEdit()
      self.img_url.setPlaceholderText("Image Url")
      layout.addRow(self.img_url)      

      self.Description = QPlainTextEdit(self)
      self.Description.setPlaceholderText("Description")
      layout.addRow(self.Description)

      self.Add_Event = QPushButton("Add Event")
      self.Add_Event.clicked.connect(self.addevent)

      self.Delete_Event= QPushButton("Delete Event")
      self.Delete_Event.clicked.connect(self.deleteevent)

      self.Update_Event = QPushButton("Update Event")
      self.Update_Event.clicked.connect(self.updateevent)

      layout.addRow(self.Add_Event, self.Delete_Event)

      
      self.responselabel = QLabel(self)
      self.responselabel.setText("Response")

      self.response = QPlainTextEdit(self)

      layout.addRow(self.responselabel)
      layout.addRow(self.response)

      self.setLayout(layout)
      self.setWindowTitle("ataraxis")

      self.genID()

   def deleteEvent(self,index):
      
      obj = eventObjs[index]
      try:
         resp = requests.get('https://7hzuz2cd7d.execute-api.us-east-1.amazonaws.com/dev/deleteEvent/{}/{}'.format(obj["EventId"], obj["EventStart"]))
         del proList[index]
         del eventObjs[index]
      except:
         self.response.setPlainText("Delete Unsuccessful")
      else:
         self.response.setPlainText(resp)


   def getEvents(self):
      resp = requests.get('https://7hzuz2cd7d.execute-api.us-east-1.amazonaws.com/dev/getAllEvents')
      result = []
      eventObjs = []
      for obj in  resp.json():
         result.append(obj["EventName"])
         eventObjs.append(obj)

      return result

		
   def genID(self):
      ID = "adminevent" + str(random.randint(10000,200000))
      self.Event_ID.setText(ID)

   def formatTime(self,Date,Time):

      # datetime_object = datetime.strptime(9/01 2019  1:33PM', '%b %d %Y %I:%M%p')
      # https://stackoverflow.com/questions/466345/converting-string-into-datetime
      datetime_object = datetime.strptime('{} 2019 {}'.format(Date,Time), '%m/%d %Y %I:%M%p')
      datetime_object_iso = datetime_object.isoformat()

      print(datetime_object_iso)

      return str(datetime_object_iso)
   
   def getPosition(self, address):

      geolocator = Nominatim(user_agent="swift_ui")
      location = geolocator.geocode(address)

      return location.latitude, location.longitude


   def addevent(self):

      session = boto3.Session(
          aws_access_key_id=constants.AWS_ACCESS_KEY_ID,
          aws_secret_access_key=constants.AWS_SECRET_ACCESS_KEY,
          region_name='us-east-1'
      )

      dynamodb = session.resource('dynamodb')

      latitude , longitude = self.getPosition(self.address.text().strip())

      print(latitude, longitude)

      if self.Description.toPlainText == ""  or self.Description.toPlainText == None:
         self.Description.setPlainText("No Description Available")

      try:

         event = {
            "EventId": self.Event_ID.text().strip(),
            "EventName": self.Event_Name.text().strip(),
            "EventStart": self.formatTime(self.Date.text().strip(), self.Time.text().strip()),
            # "EventEnd": self.End_Time.text().strip(),
            # "city": self.City.text().strip(),
            "EventLocationName" : self.Location_Name.text().strip(),
            "EventAddress": self.address.text().strip(),
            "Latitude": str(latitude),
            "Longitude": str(longitude),
            # "summary": self.Summary.text().strip(),
            "EventDescription": self.Description.toPlainText().strip().replace("'",""),
            "ImageUrl" : self.img_url.text().strip()
         }

         print(event)

         table = dynamodb.Table("experiences")
         response = table.put_item(Item=event)
      
      except Exception as e:
         self.response.setPlainText(str(e))
      else:
         self.response.setPlainText(str(response))

      self.list.clear()
      proList = self.getEvents()
      self.list.addItems(proList)
      self.genID()

   def deleteevent(self):
      pass

   def updateevent(self):
      pass
			
def main(): 
   app = QApplication(sys.argv)
   ex = inputdialog()
   ex.show()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()