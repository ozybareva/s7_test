from s7_test.logic.file_processor import FileProcessor
from s7_test.settings import Settings


class ProcessFileJob:
    def __init__(self, settings: Settings, file_processor: FileProcessor) -> None:
        self.file_processor = file_processor
        self.file_process_interval = settings.file_process_interval

    @property
    def name(self) -> str:
        return "Process file"

    @property
    def interval(self) -> int:
        return self.file_process_interval

    async def run_async(self) -> None:
        await self.file_processor.process_flight_info()
