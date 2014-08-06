#!/usr/bin/env python
# settings.py -- Contain global setup data

import sys, os
import logging

MEDIA_ROOT = "./images/"
LOGGING_LEVEL = logging.INFO
MIN_IMAGE_SIZE = 32

root_logger = logging.getLogger()
root_logger.setLevel(LOGGING_LEVEL)
stdout_stream_channel = logging.StreamHandler(sys.stdout)
stdout_stream_channel.setLevel(LOGGING_LEVEL)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
stdout_stream_channel.setFormatter(formatter)
root_logger.addHandler(stdout_stream_channel)


