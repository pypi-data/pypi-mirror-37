"""
Define a class used to access GitLab Rest API.
"""

import json
import logging
import os
from urllib import request


class GitLab:
    """
    The GitLab class provides methods to access data through the GitLab server's REST API.
    """

    def __init__(self, url, api_token):
        self.url = url
        self.api_token = api_token


    def _find_project(self, url, name):
        response = self._request(url)
        if not response:
            logging.error("No project found.")
            return None
        elif len(response) > 1:
            for project in response:
                if project['name'] == name:
                    return project
            logging.error("Project not found.")
            return None
        return response[0] if response[0]['name'] == name else None


    def find_project(self, user, name):
        """
        Find a project in the given user domain with the given name.
        """
        url = '%s/api/v4/users/%s/projects?search=%s' % (self.url, user, name)
        return self._find_project(url, name)


    def find_project_from_group(self, group, name):
        """
        Find a project in the given user domain with the given name.
        """
        url = '%s/api/v4/groups/%s/projects?search=%s' % (self.url, group, name)
        return self._find_project(url, name)


    def list_pipelines(self, project):
        """
        Lists all the pipelines for the given project.
        """
        url = '%s/api/v4/projects/%d/pipelines' % (self.url, project['id'])
        return self._request(url)


    def list_jobs(self, project, pipeline_id):
        """
        Lists all the jobs for the given pipeline of the given project.
        """
        url = '%s/api/v4/projects/%d/pipelines/%d/jobs' % (self.url, project['id'], pipeline_id)
        return self._request(url)


    def download_artifacts(self, project, job, download_dir):
        """
        Download the artifacts for the given job of the given project.
        """
        logging.debug('Downloading %s\'s artifacts...', job['name'])

        url = '%s/api/v4/projects/%d/jobs/%d/artifacts' % (self.url, project['id'], job['id'])
        filename = os.path.join(download_dir, job['artifacts_file']['filename'])
        with open(filename, 'wb') as artifacts_file:
            self._download(url, artifacts_file)
        return filename


    def _request(self, url):
        """
        Request the given REST URL and returns the json response as a Python object.
        """
        opener = request.build_opener()
        opener.addheaders = [('PRIVATE-TOKEN', self.api_token)]
        return json.load(opener.open(url))


    def _download(self, url, dest_file, monitor=None):
        """
        Downloads the file from the given url.
        """
        logging.debug('Downloading %s as %s...', url, dest_file.name)

        opener = request.build_opener()
        opener.addheaders = [('PRIVATE-TOKEN', self.api_token)]
        with opener.open(url) as connection:
            meta = connection.info()
            file_size = int(meta['Content-Length'])

            bytes_read = 0
            block_size = 8192
            while True:
                buf = connection.read(block_size)
                if not buf:
                    break

                bytes_read += len(buf)
                dest_file.write(buf)
                if monitor:
                    monitor(os.path.basename(url), bytes_read, file_size)
