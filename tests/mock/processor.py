from lyrid.core.command_processing_loop import Command


class ProcessorMock:
    def __init__(self):
        self.process__command = None

    def process(self, command: Command):
        self.process__command = command

    def start(self):
        pass

    def stop(self):
        pass
