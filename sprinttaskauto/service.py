from apiclient import discovery


def access_spreadsheet(credential):
    service = discovery.build('sheets', 'v4', credentials=credential)
    return service.spreadsheets()
