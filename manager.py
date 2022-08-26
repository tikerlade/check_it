import os
from typing import List, Tuple
import heapq

from rich.table import Table
from rich.markdown import Markdown
import yaml
import telebot

from task import Task


import logging
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)


class TasksManager:
    """
    Class to manage all tasks and configs.
    """
    tasks: List[Task] = []
    heap: List[Tuple[int, Task]] = []
    last_update_time: int = 0
    destination_chat_id: str = None
    bot: telebot.TeleBot = None
    log = logging.getLogger("rich")

    def __init__(self, filename: str = 'config.yaml'):
        """
        Initializes manager class by loading config file and processing it.
        """

        # Read telebot credentials
        token = os.getenv("BOT_TOKEN", None)
        if token:
            self.log.info("Telegram bot enabled")
            self.bot = telebot.TeleBot(token)
            self.destination_chat_id = os.getenv("MY_TELEGRAM_ID")
        else:
            self.log.info("Telegram bot credentials not found.")

        # Read config file
        with open(filename, 'r') as fin:
            for config in yaml.safe_load_all(fin):
                new_task = Task(**config)

                if new_task:
                    self.tasks.append(new_task)
                    self.heap += [(0, self.tasks[-1])]

    def get_current_table(self) -> Table:
        """
        Provides information about current statuses of all tasks as table.
        :return: Updated status table.
        """
        table = Table()

        table.add_column("ID")
        table.add_column("Link")
        table.add_column("Last check")
        table.add_column("Updated")

        for idx, task in enumerate(self.tasks):
            table.add_row(
                f"{idx}",
                Markdown(f"[{task.url}]({task.url})"),
                task.last_update_time.strftime("%X %d.%m.%Y"),
                task.completed_repr(),
                end_section=True
            )

        return table

    def update(self):
        # TODO
        # Check, maybe new config.yaml was added, so we want to reparse it.

        if self.heap:
            self.last_update_time = self.heap[0][0]

            while self.heap and (self.heap[0][0] == self.last_update_time):
                time, task = heapq.heappop(self.heap)
                task_completed = task.check()

                if not task_completed:
                    heapq.heappush(self.heap, (self.last_update_time + task.request_int, task))
                else:
                    if self.bot:
                        self.bot.send_message(self.destination_chat_id, f"This site was updated: {task.url}!")

    def get_time_to_sleep(self) -> int:
        """
        Amount of time to sleep until next task will require an update.
        :return: milliseconds of sleep.
        """
        if self.heap:
            return self.heap[0][0] - self.last_update_time
        return 0
