#!/usr/bin/env python
#-*- coding: utf-8 -*-
import logging
import sys
import os

IS_DEBUG = os.environ.get('DEBUG', 'False')
if IS_DEBUG == "True":
    LOGGING_LEVEL = logging.DEBUG
else:
    LOGGING_LEVEL = logging.INFO

logger = logging.getLogger("")
__formatter = logging.Formatter("[%(levelname)-5s][%(asctime)s][%(filename)s:%(lineno)d] %(message)s", "%d %b %Y %H:%M:%S")
__streamHandler = logging.StreamHandler(sys.stderr)
__streamHandler.setFormatter(__formatter)
__fileHandler = logging.FileHandler("/tmp/s3_obj_version.log")
__fileHandler.setFormatter(__formatter)

logger.setLevel(LOGGING_LEVEL)
logger.addHandler(__streamHandler)
logger.addHandler(__fileHandler)
