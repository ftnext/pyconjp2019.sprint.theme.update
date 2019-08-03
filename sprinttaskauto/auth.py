import google.auth


def gservice_credential():
    credentials, project = google.auth.default(
        scopes=['https://www.googleapis.com/auth/spreadsheets'])
    return credentials
