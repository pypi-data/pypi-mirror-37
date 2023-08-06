# -*- coding: utf-8 -*-
import os
import json
from collections import defaultdict

from moose.conf import settings
from moose.shortcuts import ivisit
from moose.utils._os import safe_join
from moose.utils.encoding import smart_text
from moose.connection.cloud import AzureBlobService
from moose.utils.module_loading import import_string

from .base import IllegalAction, InvalidConfig, SimpleAction

import logging
logger = logging.getLogger(__name__)


class BaseUpload(SimpleAction):
    """

    """
    # default filename pattern to match, eg. '*.wav', ('*.png', '*.jpg')
    default_pattern = None
    # whether case sensetive when matching files
    ignorecase      = True

    # string of import path to module `FileObject`,
    # which representing a file and operations on it.
    file_object_cls = ''

    def lookup_files(self, root, context):
        """
        Finds all files under the `root` while matches the given pattern.
        """
        pattern     = context.get('pattern', self.default_pattern)
        ignorecase  = context.get('ignorecase', self.ignorecase)
        logger.debug("Visit '%s' with pattern: %s..." % (root, pattern))

        files   = []
        for filepath in ivisit(root, pattern=pattern, ignorecase=ignorecase):
            files.append(filepath)
        logger.debug("%d files found." % len(files))
        return files

    def get_blobpairs(self, files, start):
        """
        Converts filepath to blobpair which consists of `(blobname, filepath)`
        while blobname is the relative path to `start`.
        """
        blobpairs = []
        for filepath in files:
            blobname = os.path.relpath(filepath, start)
            blobpairs.append((blobname, filepath))
        return blobpairs


    def get_fileobjs(self, context):
        root    = context['root']
        # uses root if relpath was not provided
        start   = context.get('basepath', root)
        # subdirs are ought to be the relpath (from the start directory)
        # to files were to upload.
        # If it was not provided in the context, then uploads all files under root.
        subdirs = context.get('subdirs', ['', ])

        self.fileobj_class = import_string(self.file_object_cls)
        fileobjs  = []
        for subdir in subdirs:
            dirpath = safe_join(root, subdir)
            files   = self.lookup_files(dirpath, context)
            self.stats.set_value(u"files/"+subdir, len(files))
            for filepath in files:
                fileobj = self.fileobj_class(filepath, self.stats, context)
                fileobjs.append(fileobj)
        return fileobjs

    def enumerate_fileobj(self, fileobjs, context):
        pass

    def handle_fileobj(self. fileobj):
        pass

    def upload(self, fileobjs, task_id):
        pass

    def dump(self, fileobjs):
        pass

    def index(self, fileobjs):
        pass

    def execute(self, context):
        fileobjs = self.get_fileobjs(context)
        self.stats.set_value("files/all", len(fileobjs))
        for fileobj in self.enumerate_fileobj(fileobjs, context):
            self.handle_fileobj(fileobj)
        self.terminate(context)
        return self.get_stats_id(context)
