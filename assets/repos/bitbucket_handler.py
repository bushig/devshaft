import json

from django.utils import timezone

import requests

from warnings import warn

API_TARGET = "https://api.bitbucket.org/1.0/repositories"

class BitbucketHandler():
    url_regex = 'https://bitbucket.org/'
    url = 'https://bitbucket.org'
    repo_regex = r'https://bitbucket.org/[\w\-\_]+/([\w\-\_]+)/{0,1}'
    slug_regex = r'https://bitbucket.org/[\w\-\_]+/([\w\-\_]+)/{0,1}'

    def _get_bitbucket_commits(self, package):
        repo_name = package.repo_name()
        if repo_name.endswith("/"):
            repo_name = repo_name[0:-1]
        target = "%s/%s/changesets/?limit=50" % (API_TARGET, repo_name)
        try:
            data = self.get_json(target)
        except requests.exceptions.HTTPError:
            return []
        if data is None:
            return []  # todo: log this?

        return data.get("changesets", [])

    def get_json(self, target):
        """
        Helpful utility method to do a quick GET for JSON data.
        """
        r = requests.get(target)
        if r.status_code != 200:
            r.raise_for_status()
        return json.loads(r.content.decode('utf-8'))

    def fetch_metadata(self, asset):
        # prep the target name
        repo_name = asset.repo_name()
        target = API_TARGET + "/" + repo_name
        if not target.endswith("/"):
            target += "/"

        try:
            data = self.get_json(target)
            print(data)
        except requests.exceptions.HTTPError as e:
            print(e)
            return asset

        if data is None:
            # TODO - log this better
            message = "%s had a JSONDecodeError during bitbucket.repo.pull" % (asset.name)
            warn(message)
            return asset

        # description
        asset.repo_description = data.get("description", "")

        # # get the forks of a repo
        # url = "{0}forks/".format(target)
        # try:
        #     data = self.get_json(url)
        # except requests.exceptions.HTTPError:
        #     return asset
        asset.repo_forks = data['forks_count']

        # # get the followers of a repo
        # url = "{0}followers/".format(target)
        # try:
        #     data = self.get_json(url)
        # except requests.exceptions.HTTPError:
        #     return asset
        asset.repo_stars = data['followers_count']
        asset.repo_updated = timezone.now()

        return asset

bitbucket_handler = BitbucketHandler()