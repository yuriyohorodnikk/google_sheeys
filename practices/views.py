from django.shortcuts import render
from pprint import pprint
from django.http import HttpResponseRedirect
from django.urls import reverse

import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from django.contrib.auth import logout
import gspread
from oauth2client.service_account import ServiceAccountCredentials


'''This part of code is getting service to use Google Sheets API via gspread
'''
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('static/credentials/credentials.json', scope)
gc = gspread.authorize(creds)
page = gc.open('ACCT practices db').sheet1


'''This part of code is getting service to use Google Sheets API
'''
CREDENTIALS_FILE = "static/credentials/credentials.json"
spreadsheet_id = '1bEpU2mHiDa3ku-LTAuAAZrS-3DuVxc1EKo8hbrOa_l8'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE, 
    [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
)
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)


#---------------------------------------------------------------------------


def get_sheet_values(range, majorDimension):
    
    spreadsheet = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range,
        majorDimension=majorDimension
    ).execute()

    return spreadsheet


def show_list(request):

    """This method wrote to show table inside list.html
    """

    title = get_sheet_values('A1', 'ROWS')
    spreadsheet = get_sheet_values('A2:F', 'ROWS')

    context = {
        'title': title['values'][0][0],
        'headings': spreadsheet['values'][0],
        'items': spreadsheet['values'][1:],
    }

    return render(request, 'list.html', context=context)


def my_logout(request):

    """This method does user logout
    """

    logout(request)
    return HttpResponseRedirect('/list/')


def update_sheet(request, id):

    """This method writes data to a specific cell inside sheet
    """
    username = request.user.first_name + " " + request.user.last_name

    srange = page.range("G3:G100").__str__()
    if username in srange:
        context = {
            "value": "Ви уже обрали місце проходження практики"
        }
        return render(request, 'thanks.html', context=context)
    else:
        cell_value = page.cell(id+2, 7).value

        update_data = cell_value + "\n" + username  

        page.update_cell(id+2, 7, update_data)

        context = {
            'value': "Дякуємо за ваш вибір."
        }

        return render(request, 'thanks.html', context=context)
