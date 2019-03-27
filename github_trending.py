import requests


def get_trending_repositories(top_size):
    headers = {
        'content-type': 'Accept: application/vnd.github.mercy-preview+json',
    }
    params = {
        'q': 'created:2019-03-26',
        'sort': 'stars',
        'order': 'desc',
        'per_page': '20',
    }
    response = requests.get('https://api.github.com/search/repositories',
                            headers=headers,
                            params=params
                            )
    r = response.json()
    for item in r['items']:
        print(item['stargazers_count'])
        # print(item['created_at'])


def get_open_issues_amount(repo_owner, repo_name):
    pass


if __name__ == '__main__':
    get_trending_repositories(None)
