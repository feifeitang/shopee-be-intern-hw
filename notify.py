import requests

LINE_ACCESS_TOKEN = "fZKQ1cinveGZu0oUfk1r1mvcFSdQZgmP6D8VL6dCrpr"


def notify(msg):

    url = "https://notify-api.line.me/api/notify"
    # file = {'imageFile': open('top20.png', 'rb')}

    data = ({
        'message': msg
    })
    LINE_HEADERS = {"Authorization": "Bearer "+LINE_ACCESS_TOKEN}
    session = requests.Session()
    session.post(url, headers=LINE_HEADERS,  data=data)
