import sprinttaskauto.auth as a
import sprinttaskauto.service as s


class CustomSpreadsheet:
    def __init__(self, sheet_access, spreadsheet_id, sheet_id):
        self.sheet_access = sheet_access
        self.spreadsheet_id = spreadsheet_id
        self.sheet_id = sheet_id

    def _build_body(self):
        raise NotImplementedError

    def write(self, data):
        body = self._build_body(data)
        self.sheet_access.batchUpdate(
            spreadsheetId=self.spreadsheet_id, body=body)


def create_custom_spreadsheet(spreadsheet_id, sheet_id):
    credential = a.gservice_credential()
    sheet_access = s.access_spreadsheet(credential)
    return CustomSpreadsheet(sheet_access, spreadsheet_id, sheet_id)
