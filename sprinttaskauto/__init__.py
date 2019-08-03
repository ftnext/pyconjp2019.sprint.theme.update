import sprinttaskauto.util as u


data = '1,2,3\n"a,b",c,d\n'
SECRET_PATH = 'secret/drive_client_secret.json'
SHEET_ID = '0'
SPREADSHEET_ID = '1SNQsUUar-TD5AHfdDxupgjpdmvBF6Ao_wQ_lf5kJFjo'


def main():
    sheet = u.create_custom_spreadsheet(SECRET_PATH, SPREADSHEET_ID, SHEET_ID)
    sheet.write(data)
