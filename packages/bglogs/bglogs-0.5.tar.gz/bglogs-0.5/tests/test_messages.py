import bglogs
import logging

logger = bglogs.get_logger('tests')


def log_and_assert(caplog, level, method, template, *args, **kwargs):

    method(template, *args, **kwargs)

    for record in caplog.records:
        assert str(record.msg) == template.format(*args, **kwargs)
        assert record.name == 'tests'
        assert record.levelno == level


def test_messages_simple(caplog):
    log_and_assert(caplog, logging.INFO, logger.info, '{}', 'placeholder')


def test_messages_multiple(caplog):
    log_and_assert(caplog, logging.DEBUG, logger.debug, '{}-{}', 'place', 'holder')


def test_messages_pos(caplog):
    log_and_assert(caplog, logging.WARNING, bglogs.warning, '{1}-{0}, {1}{0}', 'holder', 'place')


def test_messages_kw(caplog):
    log_and_assert(caplog, logging.ERROR, bglogs.error, '{place}-{holder}', place='place', holder='holder')


def test_messages_pos_and_kw(caplog):
    log_and_assert(caplog, logging.CRITICAL, logger.critical, '{0} {name}', 2, name='placeholder')
