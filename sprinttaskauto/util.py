import sprinttaskauto.auth as a
import sprinttaskauto.service as s


class CustomSpreadsheet:
    pass


def create_custom_spreadsheet(secret_path, spreadsheet_id, sheet_id):
    credential = a.gservice_credential(secret_path)
    sheet_access = s.access_spreadsheet(credential)
    return CustomSpreadsheet()
