import requests
import datetime
import sys

def get_trending_repositories(top_size):
    today = datetime.date.today()
    delta = datetime.timedelta(days=7)

    params = {
        'q': 'created:>{}'.format(today - delta),
        'sort': 'stars',
        'order': 'desc',
        'per_page': '{}'.format(top_size),
    }
    try:
        response = requests.get(
            'https://api.github.com/search/repositories',
            params=params,
        )
        repos_dict = response.json()
    except (
            requests.exceptions.ConnectionError,
            requests.exceptions.ConnectTimeout):
        return None

    return repos_dict['items']


def print_repos(repos_dict):
    for repo in repos_dict:
        print('Repo: {}'.format(repo['name']))
        print('Created at: {}'.format(repo['created_at']))
        print('Stars: {}'.format(repo['stargazers_count']))
        print('Open issues: {}'.format(repo['open_issues']))
        print('URL to repo: {}'.format(repo['svn_url']))
        print()


if __name__ == '__main__':
    top_size = 20
    repos_dict = get_trending_repositories(top_size)
    if not repos_dict:
        sys.exit("Connection error or server doesn't response")
    print_repos(repos_dict)
