# Copyright (C) 2018  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from swh.scheduler.task import Task

from .loader import PyPILoader


class LoadPyPI(Task):
    task_queue = 'swh_loader_pypi'

    def run_task(self, project_name, project_url, project_metadata_url=None):
        loader = PyPILoader()
        loader.log = self.log
        return loader.load(project_name,
                           project_url,
                           project_metadata_url=project_metadata_url)
