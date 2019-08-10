import csv
from dataclasses import dataclass

import sprinttaskauto.auth as a
import sprinttaskauto.service as s


class CustomSpreadsheet:
    def __init__(self, sheet_access, spreadsheet_id, sheet_id):
        self.sheet_access = sheet_access
        self.spreadsheet_id = spreadsheet_id
        self.sheet_id = sheet_id

    def _build_body(self, data):
        return {
            'requests': {
                'pasteData': {
                    'coordinate': {
                        'sheetId': self.sheet_id,
                        'rowIndex': 0,
                        'columnIndex': 0
                    },
                    'data': data,
                    'type': 'PASTE_VALUES',
                    'delimiter': ',',
                }
            }
        }

    def write(self, data):
        body = self._build_body(data)
        batch_update = self.sheet_access.batchUpdate(
            spreadsheetId=self.spreadsheet_id, body=body)
        batch_update.execute()


def create_custom_spreadsheet(spreadsheet_id, sheet_id):
    credential = a.gservice_credential()
    sheet_access = s.access_spreadsheet(credential)
    return CustomSpreadsheet(sheet_access, spreadsheet_id, sheet_id)


def load_data_send_format(answer_file):
    leader_lines = _select_leader_lines(answer_file)
    answer_line_list = _create_answer_line_list(leader_lines)
    return _format_answer_line_list(answer_line_list)


def _select_leader_lines(answer_file):
    leader_lines = []
    with open(answer_file, encoding='shift_jis_2004') as fin:
        reader = csv.reader(fin)
        header = next(reader)
        type_index = header.index('参加枠名')
        status_index = header.index('参加ステータス')
        leader_lines.append(header)
        for row in reader:
            if row[type_index] == 'Leader（リーダー）' \
                    and row[status_index] == '参加':
                leader_lines.append(row)
    return leader_lines


def _create_answer_line_list(leader_lines):
    header = leader_lines[0]
    name_index = header.index('表示名')
    project_index = header.index(
        'リーダーをやりたいプロジェクトを一言で言うと？ / '
        'In a word, what project do you want to lead a sprint for?')
    goal_index = header.index(
        'プロジェクトの詳細やスプリントで達成したいことを教えてください /  '
        'Tell us some details about your project '
        'or what you want to achieve in the sprint')
    message_index = header.index(
        '参加者に一言お願いします / '
        'Anything you wish to say to potential sprint partners '
        '（例：初心者用のチケットも用意してお待ちしています！）')
    return [AnswerLine(
                line[name_index], line[project_index],
                line[goal_index], line[message_index])
            for line in leader_lines[1:]]


def _format_answer_line_list(answer_line_list):
    datum = [
        '"表示名",'
        '"リーダーをやりたいプロジェクトを一言で言うと？ / In a word, '
        'what project do you want to lead a sprint for?",'
        '"プロジェクトの詳細やスプリントで達成したいことを教えてください /  '
        'Tell us some details about your project '
        'or what you want to achieve in the sprint",'
        '"参加者に一言お願いします / '
        'Anything you wish to say to potential sprint partners '
        '（例：初心者用のチケットも用意してお待ちしています！）"'
    ]
    for answer_line in answer_line_list:
        datum.append(answer_line.data_for_spreadsheet())
    return '\n'.join(datum)


@dataclass
class AnswerLine:
    leader_name: str
    project: str
    goal: str
    message: str

    def data_for_spreadsheet(self):
        leader_name = escape_double_quote(self.leader_name)
        project = escape_double_quote(self.project)
        goal = escape_double_quote(self.goal)
        message = escape_double_quote(self.message)
        return f'"{leader_name}","{project}","{goal}","{message}"'


def escape_double_quote(string):
    """ダブルクォートをシングルクォートに置き換えた文字列を返す"""
    return string.replace('"', "'")
