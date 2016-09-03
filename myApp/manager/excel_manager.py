from excel_response3 import ExcelResponse
from member_manager import memberManager


class ExcelManager(object):
    def __init__(self):
        self.data = []

    def get_members(self):
        members = memberManager.get_members()
        for i in range(0, len(members)):
            user = [members[i]['username'], members[i]['password']]
            self.data.append(user)
        return ExcelResponse(self.data, 'members')

excelManager = ExcelManager()

