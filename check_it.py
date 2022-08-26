import time

from rich.live import Live

from manager import TasksManager

manager = TasksManager()
with Live(manager.get_current_table()) as live:
    while True:
        manager.update()
        live.update(manager.get_current_table())
        time.sleep(60 * manager.get_time_to_sleep())
