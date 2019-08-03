from unittest import TestCase
from unittest.mock import call, MagicMock, patch

import sprinttaskauto.auth as a


class TestGserviceCredential(TestCase):
    @patch('google.auth.default')
    def test(self, gauth_default):
        gauth_default.return_value = [MagicMock(), MagicMock()]
        credential = a.gservice_credential()

        self.assertEqual(
            [call(scopes=['https://www.googleapis.com/auth/spreadsheets'])],
            gauth_default.call_args_list)
        self.assertEqual(credential, gauth_default.return_value[0])
