from rest_framework.response import Response
from rest_framework import status

class JsonResponse():
    GENRIC_MESSAGE = 'Currently Unable to Process this request, Please try later'
    json_messages = []
    json_data = {}
    sucess = True
    http_status_code = status.HTTP_200_OK

    def __init__(self):
        self.json_messages = []
        self.json_data = {}
        self.success = True
        self.http_status_code = status.HTTP_200_OK
        print('created new json response')

    def add_json_messages(self, messages):
        self.json_messages = self.json_messages + messages

    def mark_failed(self, messages):
        self.sucess = False
        self.json_messages = self.json_messages + messages
        self.http_status_code = status.HTTP_400_BAD_REQUEST

    def override_status(self, status_value):
        self.http_status_code = status_value

    def add_data(self, key, data):
        self.json_data[key] = data

    def export(self):
        data = { 'messages' : self.json_messages, 'data' : self.json_data , 'success' : self.sucess}
        return Response(data, status=self.http_status_code)


