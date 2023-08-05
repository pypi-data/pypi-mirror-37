# Copyright (C) 2016-2017  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from swh.scheduler.task import Task
from swh.vault.cookers import get_cooker


class SWHCookingTask(Task):
    """Main task to cook a bundle."""

    task_queue = 'swh_vault_cooking'

    def run_task(self, obj_type, obj_id):
        cooker = get_cooker(obj_type)(obj_type, obj_id)
        cooker.cook()


# TODO: remove once the scheduler handles priority tasks
class SWHBatchCookingTask(Task):
    """Temporary task for the batch queue."""

    task_queue = 'swh_vault_batch_cooking'

    def run_task(self, obj_type, obj_id):
        cooker = get_cooker(obj_type)(obj_type, obj_id)
        cooker.cook()
