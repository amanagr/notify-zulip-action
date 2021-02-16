import requests
import os
import json
import sys
import urllib.parse

def actionStatus(status):
    """
    Get a transformed status based on the workflow status.
    """

    if status == 'success':
        return 'passed'
    elif status == 'failure':
        return 'failed'

    return 'passed with warnings'

def notify_zulip(job_status, notify_when):
    bot_key = os.getenv('ZULIP_BOT_KEY')
    repo = os.getenv('GITHUB_REPOSITORY')
    if not bot_key:
        return
    branch = os.getenv('GITHUB_REF').split('/')[-1]
    topic = urllib.parse.quote(f'{branch} failing')
    stream = urllib.parse.quote(os.getenv('STREAM'))
    url = f"https://chat.zulip.org/api/v1/external/circleci?api_key={bot_key}&stream={stream}&topic={topic}"
    workflow = os.getenv('GITHUB_WORKFLOW')
    status_message = actionStatus(job_status)
    run_id = os.getenv('GITHUB_RUN_ID')

    run_url = f'https://github.com/{repo}/actions/runs/{run_id}'
    committer = os.getenv('GITHUB_ACTOR')

    payload = {
        "payload" : {
            'reponame': repo,
            'branch': branch,
            'status': status_message,
            'build_url': run_url,
            'username': committer,
        }
    }

    payload = json.dumps(payload)

    headers = {'Content-Type': 'application/json'}

    if notify_when is None:
        notify_when = 'success,failure,warnings'

    if job_status in notify_when and not testing:
        res = requests.post(url, data=payload, headers=headers)
        print(res)


def main():
    job_status = os.getenv('INPUT_STATUS')
    notify_when = os.getenv('INPUT_NOTIFY_WHEN')
    notify_zulip(job_status, notify_when)


if __name__ == '__main__':
    try:
        testing = True if sys.argv[1] == '--test' else False
    except IndexError as e:
        testing = False

    main()
