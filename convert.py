# Takes three parameters from the cli - github username, repo name, and api
# token

import sys
import csv
import json
import urllib

if len(sys.argv) == 5:
    USERNAME = sys.argv[1]
    ORGNAME = sys.argv[2]
    PROJECT = sys.argv[3]
    AUTH_TOKEN = sys.argv[4]

else:
    USERNAME = sys.argv[1]
    ORGNAME = ''
    PROJECT = sys.argv[2]
    AUTH_TOKEN = sys.argv[3]

TRAC_URL = 'https://addons.omeka.org/trac/report/1?format=csv'

if (ORGNAME == ''):
    ORGNAME = USERNAME

github_url = 'https://github.com/api/v2/json/issues/'
csv_data = urllib.urlopen(TRAC_URL)
reader = csv.DictReader(csv_data)
tickets = []

url = github_url + 'list/%s/%s/open' % (ORGNAME, PROJECT)
response = urllib.urlopen(url)
content = response.read()
issues = json.loads(content)['issues']

for row in reader:
    if row['component'] == PROJECT:
        for key, value in row.items():
            row[key] = row[key].decode('utf-8')

        if filter(lambda i: i['title'] == row['summary'], issues):
            continue

        tickets.append({
            'title': row['summary'],
            'description': row['_description'],
            'tags': [u'ime', row['type'], row['component']],
        })

for ticket in tickets:
    url = github_url + 'open/%s/%s' % (ORGNAME, PROJECT)
    data = urllib.urlencode({
        'login': USERNAME,
        'token': AUTH_TOKEN,
        'title': ticket['title'],
        'body': ticket['description'],
    })

    urllib.urlopen(github_url, data)
    response = urllib.urlopen(url, data)
    content = response.read()

    try:
        issue = json.loads(content)['issue']
    except KeyError:
        raise Exception(content)

    data = urllib.urlencode({
        'login': USERNAME,
        'token': AUTH_TOKEN,
    })

    for tag in ticket['tags']:
        url = github_url + 'label/add/%s/%s/%s/%s' % (
            ORGNAME, PROJECT, tag, issue['number'])
        urllib.urlopen(url, data)

