from unittest import TestCase
from unittest.mock import call, MagicMock, patch

import sprinttaskauto.service as s


class TestAccessSpreadsheet(TestCase):
    @patch('sprinttaskauto.service.discovery')
    def test(self, discovery):
        credential = MagicMock()
        service = discovery.build.return_value

        sheet_access = s.access_spreadsheet(credential)

        self.assertEqual(
            [call('sheets', 'v4', credentials=credential)],
            discovery.build.call_args_list)
        self.assertEqual([call()], service.spreadsheets.call_args_list)
        self.assertEqual(sheet_access, service.spreadsheets.return_value)
