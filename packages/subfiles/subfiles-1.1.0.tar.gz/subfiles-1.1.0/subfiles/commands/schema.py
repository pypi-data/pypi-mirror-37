"""The schema command."""


from json import dumps

from .base import Base

from .utils import files_by_extensions

import sys

import collections

class Schema(Base):

    def run(self):

        level = 2

        if len(sys.argv) == 3:
            try:
                level = int(sys.argv[-1])
            except:
                pass

        results = collections.OrderedDict()
        for level in range(levels):
            results.update(files_by_extensions('.', level))

        for key, val in enumerate(results):
            print("[*.{key}]".format(**{'key':val}))
            print("\n"),
