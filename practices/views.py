from django.shortcuts import render
from pprint import pprint
from django.http import HttpResponseRedirect
from django.urls import reverse

import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from django.contrib.auth import logout


def get_sheet_values(range, majorDimension):
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

    spreadsheet = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range,
        majorDimension=majorDimension
    ).execute()

    return spreadsheet

    spreadsheet = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A2:F',
        majorDimension='ROWS'
    ).execute()

    title = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A1',
        majorDimension='ROWS'
    ).execute()


def show_list(request):
    title = get_sheet_values('A1', 'ROWS')
    spreadsheet = get_sheet_values('A2:F', 'ROWS')

    context = {
        'title': title['values'][0][0],
        'headings': spreadsheet['values'][0],
        'items': spreadsheet['values'][1:],
    }

    return render(request, 'list.html', context=context)


def my_logout(request):
    logout(request)
    return HttpResponseRedirect('/list/')


def update_sheet(request, id):
    return render(request, 'thanks.html')
