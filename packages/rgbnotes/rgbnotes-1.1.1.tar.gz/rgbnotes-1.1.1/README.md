# RGB Notes Python Library


The RGB Notes Python library provides convenient access to the RGB Notes API from
applications written in the Python language. It includes a pre-defined set of
classes for API resources that initialize themselves dynamically from API
responses.

## Documentation

See the [API docs](https://rgbnotes.com/help?section=api).

## Installation

You don't need this source code unless you want to modify the package. If you just
want to use the package, just run:

    pip install --upgrade rgbnotes

Install from source with:

    python setup.py install

### Requirements

* Python 2.6+ or Python 3.3+ (PyPy supported)
* Requests Module (PyPy supported)

## Usage

The library needs to be configured with your account's secret key which is
available in your [RGB Notes Settings](https://rgbnotes.com/login.php?r=/settings.php). 


__Config__

1. Edit __rgb\_api.conf__ located in `rgbnotes`
2. Copy and paste your `client_email`, `client_id` and `client_key` in the appropriate fields

# For Developers

## API v1

How to Create an Instance with config file:
Config files with `client_id` and `client_key` can be put in one of those directories:
`/home/user.name/rgb_api.conf`
`/etc/rgb_api.conf`

```py
>>> import rgbnotes
>>> api = rgbnotes.RGB_API(debug_http=True)
DEBUG:requests.packages.urllib3.connectionpool:Starting new HTTPS connection (1): rgbnotes.com
send: 'POST /api/token/client HTTP/1.1\r\nHost: rgbnotes.com\r\nConnection: keep-alive\r\nAccept-Encoding: gzip, deflate\r\nAccept: */*\r\nUser-Agent: python-requests/2.14.2\r\nContent-Length: 58\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nclient_id=0123&client_key=0123456789abcdef0123456789abcdef'
reply: 'HTTP/1.1 200 OK\r\n'
header: Date: Sat, 09 Sep 2017 12:55:11 GMT
header: Server: Apache/2.4.7 (Ubuntu)
header: X-Powered-By: PHP/5.5.9-1ubuntu4.22
header: Cache-Control: no-cache, must-revalidate
header: Expires: Fri, 23 Feb 1979 05:00:00 GMT
header: Content-Length: 200
header: Keep-Alive: timeout=5, max=100
header: Connection: Keep-Alive
header: Content-Type: application/json
DEBUG:requests.packages.urllib3.connectionpool:https://rgbnotes.com:443 "POST /api/token/client HTTP/1.1" 200 200
```

### Load a Custom Config

You may wish to load a different config than the one that comes packaged and loaded by default by the API class. In that case you could do something like this.

```py
>>> import rgbnotes
>>> rgbnotes.api_config.CONFIG_FILE = '/path/to/config.file'
>>> config = rgbnotes.api_config.load_config()
>>> # make an instance of the api
>>> api = rgbnotes.RGB_API(config=config, debug_http=True)
```

### Load instance with client secrets directly

```py
>>> import rgbnotes
>>> api = rgbnotes.RGB_API(client_id='1234', 
                           client_key='123456abcdefghijk123567')
```

## API Methods

### Find Items
```py
>>> api.find('project', ['title', '==', 'Gold Python'])
[{'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing ', 'title': 'Gold Python', 'id': 1376, 'members': [177, 178], 'owner_id': 176}]
```

```py
>>> api.find_one('project', ['title', '==', 'Gold Python'])
{'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing ', 'title': 'Gold Python', 'id': 1376, 'members': [177, 178], 'owner_id': 176}
```

### Project Files
```py
>>> api.get_project_files(1376)
>>> from pprint import pprint
>>> pprint(rgb_api.project_files)
{u'filters': [],
 u'pagination': {u'limit': 20,
                 u'offset': 0,
                 u'sort_by': u'date',
                 u'sort_dir': u'desc',
                 u'total': 2},
 u'results': [{u'dateUploaded': u'2017-09-06 00:19:37',
               u'description': u'Post file using token',
               u'file': u'miss_fortune_surrender_league_anim_workshop.mp4',
               u'filesize': 11877374,
               u'filetype': u'video/mp4',
               u'height': 576,
               u'id': 1098,
               u'project_id': 1376,
               u'q_status': 50,
               u'thumb': 1,
               u'url': u'https://staging.rgbnotes.com/viewer/#1098',
               u'user_id': 177,
               u'width': 1024},
              {u'dateUploaded': u'2017-08-05 01:47:02',
               u'description': u'This assassin doesn\u2019t just strike from the shadows - he is the shadow. And they don\u2019t stand a chance.',
               u'file': u'death_mark_league_animation.mp4',
               u'filesize': 14902288,
               u'filetype': u'video/mp4',
               u'height': 576,
               u'id': 1064,
               u'project_id': 1376,
               u'q_status': 50,
               u'thumb': 1,
               u'url': u'https://staging.rgbnotes.com/viewer/#1064',
               u'user_id': 178,
               u'width': 1024}]}
```

### Project Notes
```py
>>> api.get_project_notes(1376)
>>> pprint(api.project_notes)
{u'filters': [],
 u'pagination': {u'limit': 20,
                 u'offset': 0,
                 u'sort_by': u'date',
                 u'sort_dir': u'desc',
                 u'total': 3},
 u'results': [{u'comment': u'third note',
               u'date': u'2017-08-30 02:23:20',
               u'file_id': 1064,
               u'id': 657,
               u'project_id': 1376,
               u'url': u'https://staging.rgbnotes.com/viewer/#1064/657',
               u'user_id': 176},
              {u'comment': u'second note',
               u'date': u'2017-08-30 02:22:56',
               u'file_id': 1064,
               u'id': 656,
               u'project_id': 1376,
               u'url': u'https://staging.rgbnotes.com/viewer/#1064/656',
               u'user_id': 176},
              {u'comment': u'first note',
               u'date': u'2017-08-30 02:21:20',
               u'file_id': 1064,
               u'id': 655,
               u'project_id': 1376,
               u'url': u'https://staging.rgbnotes.com/viewer/#1064/655',
               u'user_id': 176}]}
```

### Create User
```py
>>> api.create_user('uakari', email='uakari@qtum-ico.com')
Fetching: ['users']
>>> api.created_users
[{u'email': u'uakari@qtum-ico.com', u'id': 182, u'name': u'uakari'}]
```

```py
>>> api.create_user('ether', email='f4ts3@ethereum1.top')
Fetching: ['users']
User "ether" already exists
```


### Project Member Token
```py
>>> api.get_project_member_token(177, 1376)
>>> api.project_member_token
u'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1MDQwNTY4MzksIm5iZiI6MTUwNDA1NjgzOSwiZXhwIjoxNTA0MDYwNDM5LCJwaWQiOiIxMzc1IiwidWlkIjoiMTc3IiwibHZsIjoicHJvamVjdF9tZW1iZXIifQ.0DFXXigbByMkp76dpdONA18S7lCUC2npHe8aeK3GvcQ'
>>> api.project_member_token_header
{'Rgb-Project-Member-Token': u'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1MDQwNTY4MzksIm5iZiI6MTUwNDA1NjgzOSwiZXhwIjoxNTA0MDYwNDM5LCJwaWQiOiIxMzc1IiwidWlkIjoiMTc3IiwibHZsIjoicHJvamVjdF9tZW1iZXIifQ.0DFXXigbByMkp76dpdONA18S7lCUC2npHe8aeK3GvcQ'}
```

### Upload
```py
>>> api.get_project_member_token(178, 1376)
>>> f = open('D:/Videos/youtube-dl/darius_fear_league_anim_workshop.mp4', 'rb')
>>> meta_data = {'description': 'File upload via python api', 'share-emails-array[0]': 'user@domain.com', 'share-ids-array[0]': 176}
>>> file_data = {'file': f}
>>> api.upload_file_request(meta_data, file_data)
```
