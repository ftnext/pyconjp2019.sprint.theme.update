import os
import sprinttaskauto.util as u


data = '1,2,3\n"a,b",c,d\n'
SECRET_PATH = 'secret/PyConJP Stuff Automation.json'
SHEET_ID = '0'
SPREADSHEET_ID = '1SNQsUUar-TD5AHfdDxupgjpdmvBF6Ao_wQ_lf5kJFjo'


def main():
    credential_env_name = 'GOOGLE_APPLICATION_CREDENTIALS'
    assert os.environ.get(credential_env_name) ==\
        f"{os.environ.get('PWD')}/{SECRET_PATH}",\
        (f'Googleスプレッドシートへの認証情報のJSONを{SECRET_PATH}に配置し、\n'
         f'認証情報のJSONのフルパスを環境変数{credential_env_name}に設定してください')
    sheet = u.create_custom_spreadsheet(SPREADSHEET_ID, SHEET_ID)
    sheet.write(data)
