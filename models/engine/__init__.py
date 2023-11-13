#!/usr/bin/python3
"""Creating a file sotrage module to use at
the instant the application begins to run
"""

from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()