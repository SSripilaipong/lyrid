import multiprocessing as mp

from lyrid.core.processor import ProcessorStopCommand
from tests.processor_factory import create_processor


def test_should_stop_processor():
    processor = create_processor()
    processor.start()
    processor.stop()


def test_should_stop_processor_loop_by_processor_stop_command():
    command_queue = mp.Queue()
    command_queue.put(ProcessorStopCommand())
    processor = create_processor(command_queue=command_queue)
    processor.processor_loop()
