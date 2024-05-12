import asyncio
import logging
from collections.abc import Callable


class Scheduler:
    def __init__(self) -> None:
        self.jobs = []

    async def _run_periodically_async(
        self, name: str, wait_time: int, func: Callable, *args: list
    ):
        loop = asyncio.get_running_loop()
        logging.info(f'Job "{name}" started')
        while True:
            loop.create_task(func(*args))
            await asyncio.sleep(wait_time)

    async def schedule_task_periodically(self):
        tasks = []
        for job in self.jobs:
            tasks.append(
                self._run_periodically_async(job.name, job.interval, job.run_async)
            )
        return asyncio.gather(*tasks)

    def register(self, job) -> None:
        self.jobs.append(job)
