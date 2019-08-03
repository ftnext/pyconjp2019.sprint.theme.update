from unittest import TestCase
from unittest.mock import call, MagicMock, patch

import sprinttaskauto


class TestMain(TestCase):
    @patch('sprinttaskauto.data')
    @patch('sprinttaskauto.SECRET_PATH')
    @patch('sprinttaskauto.SPREADSHEET_ID')
    @patch('sprinttaskauto.SHEET_ID')
    @patch('sprinttaskauto.util.create_custom_spreadsheet')
    def test_basic(
            self, create_custom_spreadsheet, sheet_id,
            spreadsheet_id, secret_path, data):
        sheet = create_custom_spreadsheet.return_value

        sprinttaskauto.main()

        self.assertEqual(
            [call(secret_path, spreadsheet_id, sheet_id)],
            create_custom_spreadsheet.call_args_list)
        self.assertEqual([call(data)], sheet.write.call_args_list)
