import bglogs
import logging

logger = bglogs.get_logger('tests')
logger_unstyled = bglogs.get_logger('tests', styled=False)


def log_and_assert(caplog, level, method):

    msg = "test_default_{}".format(method.__name__)

    method(msg)

    for record in caplog.records:
        assert str(record.msg) == msg
        assert record.name == 'tests'
        assert record.levelno == level


def test_logger_info(caplog):
    log_and_assert(caplog, logging.INFO, logger.info)
    log_and_assert(caplog, logging.INFO, logger_unstyled.info)


def test_logger_debug(caplog):
    log_and_assert(caplog, logging.DEBUG, logger.debug)
    log_and_assert(caplog, logging.DEBUG, logger_unstyled.debug)


def test_logger_warning(caplog):
    log_and_assert(caplog, logging.WARNING, logger.warning)
    log_and_assert(caplog, logging.WARNING, logger_unstyled.warning)


def test_logger_error(caplog):
    log_and_assert(caplog, logging.ERROR, logger.error)
    log_and_assert(caplog, logging.ERROR, logger_unstyled.error)


def test_logger_critical(caplog):
    log_and_assert(caplog, logging.CRITICAL, logger.critical)
    log_and_assert(caplog, logging.CRITICAL, logger_unstyled.critical)
