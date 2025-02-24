import csv
from github import Github
from github import Auth

import dotenv
import os
import tqdm

# get github api key from env
dotenv.load_dotenv()
GITHUB_API_KEY = os.getenv('GITHUB_API_KEY')
auth = Auth.Token(GITHUB_API_KEY)
github = Github(auth=auth)


def get_first_commit_each_year(owner, repo, github):
    repo = github.get_repo(f'{owner}/{repo}')

    # given since – datetime
    #until – datetime
    commits = repo.get_commits() # PaginatedList of github.Commit.Commit
    # we want to get the first commit, then the first commit of the next year, etc.
    
    prior_year = None
    last_commit = commits[0]
    last_commit_date = last_commit.commit.author.date
    commits=[last_commit]
    print(f'commit: {last_commit_date}')
    # construct next_year to be jan 1 of the next year after the first commit
    
    prior_year = last_commit_date.replace(year=last_commit_date.year, month=1, day=1)
    while commit := repo.get_commits(until=prior_year):
        # print(commit)
        for c in commit:
            commits.append(c)
            print(f'First commit of {prior_year.year}: {c.commit.author.date}')
            # build prior_year from the date of the commit
            prior_year = c.commit.author.date.replace(year=c.commit.author.date.year, month=1, day=1)
            break
        else:
            break
            
        # get the first commit from the paginated list        
    # now, query repo.get_commits(since=first_commit_date)
    

    return commits

def find_github_urls_in_csv(csv_file):
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            for cell in row:
                if 'https://github.com' in cell:
                    print(cell)

if __name__ == '__main__':
    owner = 'faims'
    repo = 'FAIMS3'
    find_github_urls_in_csv("open-archaeo-updated-run1.csv")
    find_github_urls_in_csv("tool_references_not_clean.csv")

    # first_commits = get_first_commit_each_year(owner, repo, github)
    # with open('first-commits.csv', 'w') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(['year', 'sha', 'message'])
    #     for commit in first_commits:
    #         commit_date = commit.commit.author.date
    #         writer.writerow([commit_date.year])