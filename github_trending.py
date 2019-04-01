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


def get_open_issues_amount(repo_owner, repo_name):
    issues_amount = 0
    page = 1
    while True:
        params = {
            'state': 'open',
            'per_page': '100',
            'page': '{}'.format(str(page))
        }
        try:
            response = requests.get(
                'https://api.github.com/repos/{}/{}/issues'.format(
                    repo_owner,
                    repo_name,
                ),
                params=params,
            )

            issues_dict = response.json()
        except (
                requests.exceptions.ConnectionError,
                requests.exceptions.ConnectTimeout,
        ):
            return None

        if not issues_dict:
            break

        for issue in issues_dict:
            if 'id' in issue and 'pull_request' not in issue:
                issues_amount += 1

        page += 1

    return issues_amount


def print_repos(repos_dict, reponames_with_issues_dict):
    for repo in repos_dict:
        print('Repo: {}'.format(repo['name']))
        print('Created at: {}'.format(repo['created_at']))
        print('Stars: {}'.format(repo['stargazers_count']))
        print(
            'Open issues: {}'.format(reponames_with_issues_dict[repo['name']]))
        print('URL to repo: {}'.format(repo['svn_url']))
        print()


if __name__ == '__main__':
    top_size = 20
    repos_dict = get_trending_repositories(top_size)
    if not repos_dict:
        sys.exit("Connection error or server doesn't response")

    reponames_with_issues_dict = {}
    for repo in repos_dict:
        reponames_with_issues_dict[repo['name']] = get_open_issues_amount(
            repo['owner']['login'], repo['name'])
        if reponames_with_issues_dict[repo['name']] is None:
            sys.exit("Connection error or server doesn't response")

    print_repos(repos_dict, reponames_with_issues_dict)
