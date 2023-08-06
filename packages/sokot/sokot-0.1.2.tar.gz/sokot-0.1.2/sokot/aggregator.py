import copy
import datetime

from beautifultable import BeautifulTable
from sokot.configuration import SokotConfiguration
from sokot.requester import SokotRequester

DAILY_WORKING_API = '/daily-workings?start={}&end={}&additionalFields=currentDateEmployee'
DAILY_SCHEDULE_API = '/daily-schedules?start={}&end={}&additionalFields=currentDateEmployee'
EMPLOYEE_API = '/employees/{}'


class SokotAggretator():
    def __init__(self):
        self._config = SokotConfiguration()
        self._sprints = self._culc_sprint()
        self._requester = SokotRequester()
        self._name_cache = {}

    def _culc_sprint(self):
        sprints = []
        start_day = self._config.get_scrum_start_day()
        sprint_start = start_day
        while True:
            if sprint_start > datetime.date.today():
                break
            sprint_end = sprint_start + datetime.timedelta(days=13)
            sprint = (sprint_start, sprint_end)
            sprints.append(sprint)
            sprint_start = sprint_end + datetime.timedelta(days=1)
        return sprints

    def _get_name(self, employee_code):
        if employee_code in self._name_cache:
            return self._name_cache[employee_code]
        token = self._config.get_token()
        resp = self._requester.get(EMPLOYEE_API.format(employee_code), token)
        name = '{} {}'.format(resp['lastName'], resp['firstName'])
        self._name_cache[employee_code] = name
        return name

    def _print_warning(self, employee_code, date):
        name = self._get_name(employee_code)
        print('{}さんの{}の入力にエラーがあります'.format(name, date))

    def _aggregate_sprint(self, members, sprint_start, sprint_end):
        """
        members: 従業員コードリスト
        """
        token = self._config.get_token()
        resp = self._requester.get(DAILY_WORKING_API.format(sprint_start, sprint_end), token)
        schedules = self._requester.get(DAILY_SCHEDULE_API.format(sprint_start, sprint_end), token)
        sum_min = 0
        for daily_record in resp:
            unfilled_member = copy.deepcopy(members)
            for record in daily_record['dailyWorkings']:
                if record['currentDateEmployee']['code'] in members:
                    # 入力の仕方が間違っている人を抽出
                    if record['isError']:
                        employee_code = record['currentDateEmployee']['code']
                        self._print_warning(employee_code, record['date'])
                    else:
                        sum_min += record['overtime']
                    unfilled_member.remove(record['currentDateEmployee']['code'])
            # そもそも入力していない人を抽出
            for member in unfilled_member:
                daily_schedule = [daily['dailySchedules'] for daily in schedules if daily['date'] == daily_record['date']][0]
                for schedule in daily_schedule:
                    if schedule['currentDateEmployee']['code'] == member and schedule['scheduleTypeName'] == '通常勤務':
                        self._print_warning(member, daily_record['date'])

        return round(sum_min / 60, 2)

    def aggregate(self, agg_type):
        table = BeautifulTable()
        group_names = list(self._config.list_group().keys())
        table.column_headers = ["Sprint No."] + group_names

        sprint_no = 0
        for sprint in self._sprints:
            sprint_no += 1
            sprint_start, sprint_end = sprint[0], sprint[1]
            sprint_str = "Sprint #{} ({} - {})".format(sprint_no, sprint_start, sprint_end)
            group_result = []
            for _, members in self._config.list_group().items():
                result = self._aggregate_sprint(members, sprint_start, sprint_end)
                group_result.append(result)
            table.append_row([sprint_str] + group_result)
        return table
