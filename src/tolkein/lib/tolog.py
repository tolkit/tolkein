#!/usr/bin/env python3
"""Log events."""

import logging


def logger_config(debug=False):
    """Configure log format."""
    if debug:
        log_format = "%(asctime)s [%(levelname)s] line %(lineno)d %(message)s"
        level = logging.DEBUG
    else:
        log_format = "%(asctime)s [%(levelname)s] %(message)s"
        level = logging.INFO
    return {"level": level, "format": log_format, "filemode": "w"}


def logger(name="tolkein", debug=False):
    """Create logger."""
    config = logger_config(debug)
    logging.basicConfig(**config)
    _logger = logging.getLogger(name)
    _logger.propagate = False
    # _logger.handlers = []
    _logger.setLevel(config["level"])
    stream_h = logging.StreamHandler()
    formatter = logging.Formatter(config["format"])
    stream_h.setFormatter(formatter)
    _logger.addHandler(stream_h)
    for handler in _logger.handlers:
        handler.formatter.default_msec_format = "%s.%03d"
    return _logger


class DisableLogger:
    """Logger context management."""

    def __enter__(self):
        """Set logging level to critical."""
        logging.disable(logging.CRITICAL)

    def __exit__(self, x, y, z):
        """Set logging level back to default."""
        logging.disable(logging.NOTSET)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
