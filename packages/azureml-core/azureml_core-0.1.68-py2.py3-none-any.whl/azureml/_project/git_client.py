# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import os
from io import BytesIO

import azureml._project.file_utilities as file_utilities

from dulwich import (
    porcelain,
    client as dulwich_client,
    errors as dulwich_errors
)


class GitClient(object):
    def __init__(self):
        self._dulwich_auth = dulwich_client.default_urllib2_opener(None)

    def clone(self, repo_url, path, bare=None):
        """
        Clone a repo and return a GitRepo

        :type repo_url: str repo_url
        :type path: str
        :type bare: bool

        :rtype: GitRepo
        """
        outstream = BytesIO()
        errstream = BytesIO()

        try:
            repo = porcelain.clone(repo_url, path, bare, errstream=errstream,
                                   outstream=outstream, opener=self._dulwich_auth)
            repo.close()
        except dulwich_errors.NotGitRepository:
            raise ValueError("{} is not a valid Git repo url".format(repo_url))

        # https://github.com/jelmer/dulwich/issues/585
        file_utilities.make_file_or_directory_hidden(os.path.join(path, ".git"))
