from tests.processor_factory import create_processor


def test_should_stop():
    processor = create_processor()
    processor.start()
    processor.stop()
