
"""
Standard interface to all supported code hosting platforms.

Two important distinctions comparing to
1. URLs must include the code hosting platform itself, i.e. instead of
    `cmustrudel/strudel.scraper` one should use
    `github.com/cmustrudel/strudel.scraper`.
2. Returned objects are simplified to a common subset of fields
"""

import github, bitbucket, gitlab


def parse_github_commit(commit):
    github_author = commit['author'] or {}
    commit_author = commit['commit'].get('author') or {}
    return {
        'sha': commit['sha'],
        'author': github_author.get('login'),
        'author_name': commit_author.get('name'),
        'author_email': commit_author.get('email'),
        'authored_date': commit_author.get('date'),
        'message': commit['commit']['message'],
        'committed_date': commit['commit']['committer']['date'],
        'parents': tuple(p['sha'] for p in commit['parents']),
        'verified': commit.get('verification', {}).get('verified')
    }


def parse_github_issue(issue):
    return {
        'author': issue['user']['login'],
        'closed': issue['state'] != "open",
        'created_at': issue['created_at'],
        'updated_at': issue['updated_at'],
        'closed_at': issue['closed_at'],
        'number': issue['number'],
        'title': issue['title'],
        'body': issue['body'],
        'labels': [l['name'] for l in issue['labels']],
        'assignee': issue.get('assignee') and issue['assignee'].get('login'),
        'pull_request': issue.get('pull_request') and issue['pull_request'].get('url')
    }


def parse_github_pullrequest(pr):
    head = pr.get('head') or {}
    head_repo = head.get('repo') or {}
    base = pr.get('base') or {}
    base_repo = base.get('repo') or {}
    return {
        'id': int(pr['number']),  # no idea what is in the id field
        'title': pr['title'],
        'body': pr['body'],
        'labels': 'labels' in pr and [l['name'] for l in pr['labels']],
        'created_at': pr['created_at'],
        'updated_at': pr['updated_at'],
        'closed_at': pr['closed_at'],
        'merged_at': pr['merged_at'],
        'author': pr['user']['login'],
        'head': head_repo.get('full_name'),
        'head_branch': head.get('label'),
        'base': base_repo.get('full_name'),
        'base_branch': base.get('label'),
    }


def parse_github_issue_comment(comment):
    return {
        'body': comment['body'],
        'author': comment['user']['login'],
        'created_at': comment['created_at'],
        'updated_at': comment['updated_at'],
    }


def parse_github_review_comment(comment):
    return {
        'id': comment['id'],
        'body': comment['body'],
        'author': comment['user']['login'],
        'created_at': comment['created_at'],
        'updated_at': comment['updated_at'],
        'author_association': comment['author_association']
    }