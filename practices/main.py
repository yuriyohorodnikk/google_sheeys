import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('static/credentials/credentials.json', scope)
gc = gspread.authorize(creds)
page = gc.open('ACCT practices db').sheet1
page.resize(20, 7)

is_unique = page.findall("Юрій Олександрович Огороднік")
row_count = page.row_count

srange = page.range("G3:G100").__str__()
if "Юрій Олександрович Огороднік" in srange:
    print("YES")
else:
    print("NO")