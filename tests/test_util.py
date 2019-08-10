import os

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
        batch_update = sheet_access.batchUpdate.return_value

        sheet.write(data)

        self.assertEqual([call(data)], build_body.call_args_list)
        self.assertEqual(
            [call(spreadsheetId=spreadsheet_id, body=body)],
            sheet_access.batchUpdate.call_args_list)
        self.assertEqual([call()], batch_update.execute.call_args_list)


class TestCustomSpreadsheetBuildBody(TestCase):
    def test(self):
        sheet_access = MagicMock()
        spreadsheet_id = MagicMock()
        sheet_id = MagicMock()
        sheet = u.CustomSpreadsheet(sheet_access, spreadsheet_id, sheet_id)
        data = MagicMock()
        expected = {
            'requests': {
                'pasteData': {
                    'coordinate': {
                        'sheetId': sheet_id,
                        'rowIndex': 0,
                        'columnIndex': 0
                    },
                    'data': data,
                    'type': 'PASTE_VALUES',
                    'delimiter': ',',
                }
            }
        }

        actual = sheet._build_body(data)

        self.assertEqual(expected, actual)


class TestLoadDataSendFormat(TestCase):
    @patch('sprinttaskauto.util._format_answer_line_list')
    @patch('sprinttaskauto.util._create_answer_line_list')
    @patch('sprinttaskauto.util._select_leader_lines')
    def test(
            self, select_leader_lines, create_answer_line_list,
            format_answer_line_list):
        answer_file = MagicMock()
        leader_lines = select_leader_lines.return_value
        answer_line_list = create_answer_line_list.return_value

        data = u.load_data_send_format(answer_file)

        self.assertEqual(
            [call(answer_file)], select_leader_lines.call_args_list)
        self.assertEqual(
            [call(leader_lines)], create_answer_line_list.call_args_list)
        self.assertEqual(
            [call(answer_line_list)], format_answer_line_list.call_args_list)
        self.assertEqual(data, format_answer_line_list.return_value)


class TestSelectLeaderLines(TestCase):
    @patch('builtins.open')
    @patch('csv.reader')
    def test_call_args(self, csv_reader, mock_open):
        answer_file = MagicMock()
        fin = mock_open.return_value.__enter__.return_value

        u._select_leader_lines(answer_file)

        self.assertEqual(
            [call(answer_file, encoding='shift_jis_2004')],
            mock_open.call_args_list)
        self.assertEqual([call(fin)], csv_reader.call_args_list)

    def test_integrate(self):
        answer_file = os.path.join(
            os.path.dirname(__file__), 'data', 'test_select_leader_lines.csv')

        leader_lines = u._select_leader_lines(answer_file)

        self.assertEqual(2, len(leader_lines))
        self.assertEqual(
            ['参加枠名', 'ユーザー名', '表示名', 'コメント',
             '参加ステータス', '出欠ステータス',
             'スプリントリーダーやりたい / I would like to lead a sprint',
             'リーダーをやりたいプロジェクトを一言で言うと？ / In a word, '
             'what project do you want to lead a sprint for?',
             'プロジェクトの詳細やスプリントで達成したいことを教えてください '
             '/  Tell us some details about your project '
             'or what you want to achieve in the sprint',
             '参加者に一言お願いします / Anything you wish to say to potential '
             'sprint partners （例：初心者用のチケットも用意してお待ちしています！）',
             '更新日時', '受付番号'
             ], leader_lines[0])
        self.assertEqual(
            ['Leader（リーダー）', '高坂麗奈', 'reina',
             'PyCon JP 2019 Sprint に参加を申し込みました！', '参加', '',
             'はい / Yes', '特別になりたい', '他の奴らと,同じになりたくない',
             '悔しくって死にそう', '2019年7月13日 13時02分', '1234567'],
            leader_lines[1])


class TestCreateAnswerLineList(TestCase):
    def test(self):
        leader_lines = [
            ['参加枠名', 'ユーザー名', '表示名', 'コメント',
             '参加ステータス', '出欠ステータス',
             'スプリントリーダーやりたい / I would like to lead a sprint',
             'リーダーをやりたいプロジェクトを一言で言うと？ / In a word, '
             'what project do you want to lead a sprint for?',
             'プロジェクトの詳細やスプリントで達成したいことを教えてください '
             '/  Tell us some details about your project '
             'or what you want to achieve in the sprint',
             '参加者に一言お願いします / Anything you wish to say to potential '
             'sprint partners （例：初心者用のチケットも用意してお待ちしています！）',
             '更新日時', '受付番号'
             ],
            ['Leader（リーダー）', '高坂麗奈', 'reina',
             'PyCon JP 2019 Sprint に参加を申し込みました！', '参加', '',
             'はい / Yes', '特別になりたい', '他の奴らと,同じになりたくない',
             '悔しくって死にそう', '2019年7月13日 13時02分', '1234567']
        ]

        answer_line_list = u._create_answer_line_list(leader_lines)

        self.assertEqual(1, len(answer_line_list))
        answer_line = answer_line_list[0]
        self.assertIsInstance(answer_line, u.AnswerLine)
        self.assertEqual('reina', answer_line.leader_name)
        self.assertEqual('特別になりたい', answer_line.project)
        self.assertEqual('他の奴らと,同じになりたくない', answer_line.goal)
        self.assertEqual('悔しくって死にそう', answer_line.message)


class TestFormatAnswerLineList(TestCase):
    @patch('sprinttaskauto.util.AnswerLine.data_for_spreadsheet')
    def test(self, data_for_spreadsheet):
        header = ('"表示名",'
                  '"リーダーをやりたいプロジェクトを一言で言うと？ / In a word, '
                  'what project do you want to lead a sprint for?",'
                  '"プロジェクトの詳細やスプリントで達成したいことを教えてください /  '
                  'Tell us some details about your project '
                  'or what you want to achieve in the sprint",'
                  '"参加者に一言お願いします / '
                  'Anything you wish to say to potential sprint partners '
                  '（例：初心者用のチケットも用意してお待ちしています！）"')
        data_for_spreadsheet.return_value = (
            '"表示名","特別になりたい","他の奴らと,同じになりたくない",'
            '"悔しくって死にそう"')
        line_a = data_for_spreadsheet.return_value

        answer_line_list = [
            u.AnswerLine(
                'reina', '特別になりたい', '他の奴らと,同じになりたくない',
                '悔しくって死にそう')
        ]
        data = u._format_answer_line_list(answer_line_list)

        self.assertEqual([call()], data_for_spreadsheet.call_args_list)
        self.assertEqual(f'{header}\n{line_a}', data)


class TestAnswerLineDataForSpreadsheet(TestCase):
    def test_not_double_quote(self):
        answer_line = u.AnswerLine(
            'kumiko', 'うまくなりたい', '悔しくって死にそう',
            '頑張れば何かがあるって信じてる')
        expected = ('"kumiko","うまくなりたい","悔しくって死にそう",'
                    '"頑張れば何かがあるって信じてる"')

        actual = answer_line.data_for_spreadsheet()

        self.assertEqual(expected, actual)

    def test_include_double_quote(self):
        answer_line = u.AnswerLine(
            'mizo"re', '"オーボエ"だってやってない', '希美が私の"全部"なの',
            '希美は私の"トクベツ"'
        )
        expected = ('"mizo\'re","\'オーボエ\'だってやってない",'
                    '"希美が私の\'全部\'なの","希美は私の\'トクベツ\'"')

        actual = answer_line.data_for_spreadsheet()

        self.assertEqual(expected, actual)


class TestEscapeDoubleQuote(TestCase):
    def test(self):
        actual = u.escape_double_quote('"Isn\'t," they said.')
        self.assertEqual('\'Isn\'t,\' they said.', actual)
