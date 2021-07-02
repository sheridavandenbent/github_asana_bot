#!/usr/bin/python

# require pygithub installed
from github import Github
import asana
import os

github_token = os.getenv("GITHUB_TOKEN")
github_repository = 'dema-trading-ai/engine'

asana_token = os.getenv("ASANA_TOKEN")


def main():
    g = Github(github_token)
    repo = g.get_repo(github_repository)
    issues = repo.get_issues().reversed

    client = asana.Client.access_token(asana_token)
    client.options['client_name'] = "github_integration"

    with open('./last_issue.txt', 'r+') as f:
        contents = f.read()
        if contents != "":
            last_issue = int(contents)
        else:
            last_issue = 274

    for issue in issues:
        if 'issue' in issue.html_url and issue.number > last_issue:

            task = {
                "name": issue.title,
                "notes": issue.html_url + "\n " + issue.body,
                "projects": [
                  "1199905539732411"
                ]
              }
            result = client.tasks.create_task(task, opt_pretty=True)
            if result:
                print("Task created for issue " + str(issue.number))
            else:
                print("ERROR: Task failed to create for issue " + str(issue.number))
                break

            last_issue = issue.number

    with open('./last_issue.txt', 'w+') as f:
        f.write(str(last_issue))


if __name__ == '__main__':
    main()
