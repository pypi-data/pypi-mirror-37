import requests


class Client:
    def __init__(self, base_url, apikey, author, project, taskname, expected_time):
        self.base_url = base_url
        self.apikey = apikey
        self.author = author
        self.project = project
        self.taskname = taskname
        self.expected_time = expected_time
        self.id = None

    def start(self):
        payload = {
            'apikey': self.apikey,
            'author': self.author,
            'project': self.project,
            'taskname': self.taskname,
            'expected_time': self.expected_time,
        }
        try:
            response = requests.get('{}start'.format(self.base_url), params=payload)
            if response.status_code == 200:
                self.id = response.json()['id']
                print('MonitoringSmithClient: start')
            else:
                print('MonitoringSmithClient: internal problem occurred \n{}'.format(response.json()['message']))
        except Exception as err:
            print('MonitoringSmithClient: internal problem occurred \n{}'.format(err))

    def comment(self, comment):
        payload = {
            'apikey': self.apikey,
            'id': self.id,
            'comment': comment
        }
        try:
            response = requests.get('{}comment'.format(self.base_url), params=payload)
            if response.status_code == 200:
                print('MonitoringSmithClient: {}'.format(comment))
        except Exception as err:
            print('MonitoringSmithClient: internal problem occurred \n{}'.format(err))

    def finish(self, comment):
        payload = {
            'apikey': self.apikey,
            'id': self.id,
            'comment': comment
        }
        try:
            response = requests.get('{}finish'.format(self.base_url), params=payload)
            if response.status_code == 200:

                print('MonitoringSmithClient: success')
        except Exception as err:
            print('MonitoringSmithClient: internal problem occurred \n{}'.format(err))

    def fail(self, comment, external_error):
        payload = {
            'apikey': self.apikey,
            'id': self.id,
            'comment': comment
        }
        try:
            response = requests.get('{}fail'.format(self.base_url), params=payload)
            if response.status_code == 200:
                print('MonitoringSmithClient: {}'.format(external_error))
        except Exception as err:
            print('MonitoringSmithClient: internal problem occurred \n{}'.format(err))
