from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from . import script
from . import config
import requests
import json
import xlsxwriter
import datetime
import mimetypes
# Create your views here.

CLIENT_ID = 'client_id'
CLIENT_SECRET = 'client_secret'
TENANT = 'tenant'
ACCESS_TOKEN = 'access_token'
data = list()

def _get_access_token(tenant, client_id, client_secret):
        data = {
            CLIENT_ID: client_id,
            'scope': 'https://graph.microsoft.com/.default',
            CLIENT_SECRET: client_secret,
            'grant_type': 'client_credentials'
        }
        access_token = requests.post(
            f'https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token',
            data=data
        ).json()[ACCESS_TOKEN]
        print(access_token)
        return access_token
    
def index(request):
       list1 = dict()
       list2 = list()
       global data
       access_token =_get_access_token(
            config.graph_auth[TENANT],
            config.graph_auth[CLIENT_ID],
            config.graph_auth[CLIENT_SECRET])
       print(access_token)
       response = requests.get('https://graph.microsoft.com/v1.0/DeviceManagement/ManagedDevices', headers={'Authorization' : 'Bearer ' + access_token})
       #print(response.json())
       data = response.json()
       print(type(data))
       print(data['value'][0]['deviceName'])
       #print(data['deviceName'])
       print(len(data['value']))
       for i in range(0, len(data['value'])):
           list1['deviceName'] = data['value'][i]['deviceName']
           list1['enrolledDateTime'] = data['value'][i]['enrolledDateTime']
           list1['userPrincipalName'] = data['value'][i]['userPrincipalName']
           list1['userDisplayName'] = data['value'][i]['userDisplayName']
           list2.append(list1)
           #list1.append({'deviceName' : data['value'][i]['deviceName']})
       print(list2)
       #list2.append({'deviceName': 'DESKTOP-NLNO7UC', 'enrolledDateTime': '2020-02-10T07:55:20Z', 'userPrincipalName': 'AllanD@M365x201590.OnMicrosoft.com', 'userDisplayName': 'Allan Deyoung'})
       data = list2
       return render(request, 'index.html', {'data': list2 })

def export(request):
    print('Exported data')
    print(data)
    date = str(datetime.datetime.now().strftime("%Y-%m-%d_%H_%M") )+ '.xlsx'
    fileName = 'documents_'+ date
    fl_path = 'C:\\Users\\user\\Downloads'
    fl = open(fl_path, 'r')
    workbook = xlsxwriter.Workbook(fileName)
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'Device Name')
    worksheet.write('B1', 'Enrolled Date And Time')
    worksheet.write('C1', 'User Principla Name')
    worksheet.write('D1', 'User Display Name')
    row = 1
    column = 0
    for item in data:
        print(item)
        for key in item:
            #print(key)
            print(item[key])
            worksheet.write(row, column, item[key])
            column = column + 1
        column = 0
        row = row + 1
    workbook.close() 
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % fileName
    return response
