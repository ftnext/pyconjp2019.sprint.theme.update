from unittest import TestCase
from unittest.mock import call, MagicMock, patch

import sprinttaskauto


class TestMain(TestCase):
    @patch('sprinttaskauto.ANSWER_FILE')
    @patch('sprinttaskauto.SPREADSHEET_ID')
    @patch('sprinttaskauto.SHEET_ID')
    @patch('sprinttaskauto.util.load_data_send_format')
    @patch('sprinttaskauto.util.create_custom_spreadsheet')
    def test_basic(
            self, create_custom_spreadsheet, load_data_send_format,
            sheet_id, spreadsheet_id, answer_file):
        sheet = create_custom_spreadsheet.return_value
        data = load_data_send_format.return_value

        sprinttaskauto.main()

        self.assertEqual(
            [call(spreadsheet_id, sheet_id)],
            create_custom_spreadsheet.call_args_list)
        self.assertEqual(
            [call(answer_file)], load_data_send_format.call_args_list)
        self.assertEqual([call(data)], sheet.write.call_args_list)
