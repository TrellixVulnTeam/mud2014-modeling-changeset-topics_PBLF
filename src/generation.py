#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# [The "New BSD" license]
# Copyright (c) 2014 The Board of Trustees of The University of Alabama
# All rights reserved.
#
# See LICENSE for details.

"""
Code for generating the corpora.
"""

from __future__ import print_function
from StringIO import StringIO
import os
import re

import gensim
import dulwich, dulwich.repo, dulwich.patch

class MultiTextCorpus(gensim.corpora.TextCorpus):
    """ Iterates over all files within `top_dir`, yielding each file as
    a document and the fully qualified name of the file as the metadata.

    """

    def __init__(self, top_dir):
        # set top_dir first so get_texts doesn't get lost during TextCorpus.__init__
        self.top_dir = top_dir

        # giving it top_dir doesn't matter;
        # just forces TextCorpus to build a dictionary so docs aren't garbage
        # might be worthwhile to build the dictionary within get_texts
        super(MultiTextCorpus, self).__init__(top_dir)

    def get_texts(self):
        length = 0

        for root, dirs, files in os.walk(self.top_dir):
            # walk all files and subdirectories, yielding the contents of each
            for fname in files:
                fpath = os.path.join(root, fname)
                length += 1

                with open(fpath) as f:
                    document = f.read()

                if self.metadata:
                    yield gensim.utils.tokenize(document, lower=True), (fpath, u'en')
                else:
                    yield gensim.utils.tokenize(document, lower=True)

        self.length = length # only reset after iteration is done.

class ChangesetCorpus(gensim.corpora.TextCorpus):
    """ Iterates over all files within `top_dir`, yielding each file as
    a document and the fully qualified name of the file as the metadata.

    """

    def __init__(self, git_dir):
        self.repo = dulwich.repo.Repo(git_dir)
        super(ChangesetCorpus, self).__init__(git_dir)


    def _get_diff(self, changeset):
        patch_file = StringIO()
        dulwich.patch.write_object_diff(patch_file, self.repo.object_store,
                (changeset.old.path, changeset.old.mode, changeset.old.sha),
                (changeset.new.path, changeset.new.mode, changeset.new.sha))
        return patch_file.getvalue()

    def _walk_changes(self, reverse=False):
        """ Returns one file change at a time, not the entire diff. """

        for walk_entry in self.repo.get_walker(reverse=reverse):
            commit = walk_entry.commit

            # initial revision, has no parent
            if len(commit.parents) == 0:
                for changes in dulwich.diff_tree.tree_changes(
                        self.repo.object_store,
                        None,
                        commit.tree):
                    diff = self._get_diff(changes)
                    yield commit, None, diff

            for parent in commit.parents:
                # do I need to know the parent id?

                for changes in dulwich.diff_tree.tree_changes(
                        self.repo.object_store,
                        self.repo[parent].tree,
                        commit.tree):
                    diff = self._get_diff(changes)
                    yield commit, parent, diff

    def get_texts(self):
        length = 0
        unified = re.compile(r'^[+ -].*')
        current = None
        low = list()

        for commit, parent, diff in self._walk_changes():
            # write out once all diff lines for commit have been collected
            # this is over all parents and all files of the commit
            if current is None:
                current = commit
                low = list()
            elif current != commit:
                if self.metadata:
                    yield low, (current.id, u'en')
                else:
                    yield low
                length += 1
                current = commit
                low = list()

            diff_lines = filter(lambda x: unified.match(x),
                                diff.splitlines())
            if len(diff_lines) < 2:
                continue

            # sanity?
            assert diff_lines[0].startswith('--- '), diff_lines[0]
            assert diff_lines[1].startswith('+++ '), diff_lines[1]
            #parent_fn = diff_lines[0][4:]
            #commit_fn = diff_lines[1][4:]

            diff_lines = diff_lines[2:] # chop off file names hashtag rebel
            lines = [line[1:] for line in diff_lines] # remove unified markers
            document = ' '.join(lines)

            words = gensim.utils.tokenize(document, lower=True)
            low.extend(words)

        length += 1
        if self.metadata:
            yield low, (current.id, u'en')
        else:
            yield low

        self.length = length # only reset after iteration is done.
