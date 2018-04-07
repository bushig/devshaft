from time import sleep

from django.conf import settings
from django.utils import timezone

from github import Github


class GitHubHandler:
    url_regex = '(http|https|git)://github.com/'
    url = 'https://github.com'
    repo_regex = r'(?:http|https|git)://github.com/[^/]*/([^/]*)/{0,1}'
    slug_regex = repo_regex

    def __init__(self):
        if settings.GITHUB_TOKEN:
            self.github = Github(settings.GITHUB_TOKEN)
        else:
            self.github = Github()

    def manage_ratelimit(self):
        print("ratelimit: ", self.github.rate_limiting)
        while self.github.rate_limiting[0] < 10:
            sleep(1)

    def _get_repo(self, asset):
        repo_name = asset.repo_name()
        print(repo_name)
        if repo_name.endswith("/"):
            repo_name = repo_name[:-1]
        return self.github.get_repo(repo_name)

    def fetch_metadata(self, asset):
        self.manage_ratelimit()
        repo = self._get_repo(asset)
        print(repo)
        if repo is None:
            return asset

        asset.repo_stars = repo.stargazers_count
        asset.repo_forks = repo.forks
        asset.repo_description = repo.description
        asset.repo_updated = timezone.now()
        commit_activity = []
        for stat in repo.get_stats_commit_activity():
            commit_activity.append(str(sum(stat.days)))
        asset.commits = ",".join(commit_activity)

        # contributors = []
        # for contributor in repo.iter_contributors():
        #     contributors.append(contributor.login)
        #     self.manage_ratelimit()
        #
        # if contributors:
        #     package.participants = ','.join(uniquer(contributors))

        return asset

    # def fetch_commits(self, package):
    #
    #     self.manage_ratelimit()
    #     repo = self._get_repo(package)
    #     if repo is None:
    #         return package
    #
    #     from package.models import Commit  # Added here to avoid circular imports
    #
    #     for commit in repo.iter_commits():
    #         self.manage_ratelimit()
    #         try:
    #             commit_record, created = Commit.objects.get_or_create(
    #                 package=package,
    #                 commit_date=commit.commit.committer['date']
    #             )
    #             if not created:
    #                 break
    #         except Commit.MultipleObjectsReturned:
    #             continue
    #         # If the commit record already exists, it means we are at the end of the
    #         #   list we want to import
    #
    #     package.save()
    #     return package


github_handler = GitHubHandler()
