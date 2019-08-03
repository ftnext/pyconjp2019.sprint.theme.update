from unittest import TestCase
from unittest.mock import call, MagicMock, patch

import sprinttaskauto.util as u


class TestCustomSpreadsheetFactory(TestCase):
    @patch('sprinttaskauto.auth.gservice_credential')
    @patch('sprinttaskauto.service.access_spreadsheet')
    def test_flow(self, access_spreadsheet, gservice_credential):
        spreadsheet_id = MagicMock()
        sheet_id = MagicMock()
        credential = gservice_credential.return_value
        sheet_access = access_spreadsheet.return_value

        sheet = u.create_custom_spreadsheet(spreadsheet_id, sheet_id)

        self.assertEqual([call()], gservice_credential.call_args_list)
        self.assertEqual([call(credential)], access_spreadsheet.call_args_list)
        self.assertIsInstance(sheet, u.CustomSpreadsheet)
        self.assertEqual(sheet.sheet_access, sheet_access)
        self.assertEqual(sheet.spreadsheet_id, spreadsheet_id)
        self.assertEqual(sheet.sheet_id, sheet_id)


class TestCustomSpreadsheetWrite(TestCase):
    @patch('sprinttaskauto.util.CustomSpreadsheet._build_body')
    def test(self, build_body):
        sheet_access = MagicMock()
        spreadsheet_id = MagicMock()
        sheet_id = MagicMock()
        sheet = u.CustomSpreadsheet(sheet_access, spreadsheet_id, sheet_id)
        data = MagicMock()
        body = build_body.return_value

        sheet.write(data)

        self.assertEqual([call(data)], build_body.call_args_list)
        self.assertEqual(
            [call(spreadsheetId=spreadsheet_id, body=body)],
            sheet_access.batchUpdate.call_args_list)
