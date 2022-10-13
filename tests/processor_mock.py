from lyrid.core.processor import Command


class ProcessorMock:
    def __init__(self):
        self.process_command = None

    def process(self, command: Command):
        self.process_command = command

    def start(self):
        pass

    def stop(self):
        pass
