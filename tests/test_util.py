from unittest import TestCase
from unittest.mock import call, MagicMock, patch

import sprinttaskauto.util as u


class TestCustomSpreadsheetFactory(TestCase):
    @patch('sprinttaskauto.auth.gservice_credential')
    @patch('sprinttaskauto.service.access_spreadsheet')
    def test_flow(self, access_spreadsheet, gservice_credential):
        secret_path = MagicMock()
        spreadsheet_id = MagicMock()
        sheet_id = MagicMock()
        credential = gservice_credential.return_value
        sheet_access = access_spreadsheet.return_value

        sheet = u.create_custom_spreadsheet(
            secret_path, spreadsheet_id, sheet_id)

        self.assertEqual(
            [call(secret_path)], gservice_credential.call_args_list)
        self.assertEqual([call(credential)], access_spreadsheet.call_args_list)
        self.assertIsInstance(sheet, u.CustomSpreadsheet)
        self.assertEqual(sheet.sheet_access, sheet_access)
        self.assertEqual(sheet.spreadsheet_id, spreadsheet_id)
        self.assertEqual(sheet.sheet_id, sheet_id)
