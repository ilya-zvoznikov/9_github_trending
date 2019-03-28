import requests
import datetime


def get_trending_repositories(top_size):
    today = datetime.date.today()
    delta = datetime.timedelta(days=7)

    headers = {}
    params = {
        'q': 'created:>{}'.format(today - delta),
        'sort': 'stars',
        'order': 'desc',
        'per_page': '20',
    }
    response = requests.get(
        'https://api.github.com/search/repositories',
        headers=headers,
        params=params,
    )
    r = response.json()

    return r['items']


def get_open_issues_amount(repo_owner, repo_name):
    headers = {}
    params = {
        'state': 'open',
    }
    response = requests.get(
        'https://api.github.com/repos/{}/{}/issues'.format(
            repo_owner,
            repo_name,
        ),
        headers=headers,
        params=params,
    )

    r = response.json()

if __name__ == '__main__':
    repos = get_trending_repositories(None)
    # get_open_issues_amount(rep['owner']['login'], rep['name'])
    for repo in repos:
        print(repo['name'])
        print(repo['created_at'])
        print(repo['stargazers_count'])
        print(repo['open_issues'])
        print(repo['svn_url'])
        print()