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

import nltk
import gensim
import dulwich, dulwich.repo, dulwich.patch
import gittle

CODECS = ['utf8', 'latin1', 'ascii']
tokenize = nltk.word_tokenize

def to_unicode(document, info=str()):
    document = document.replace('\x00', ' ') #remove nulls
    document = document.strip()
    if not isinstance(document, unicode):
        for codec in CODECS:
            try:
                return unicode(document, encoding=codec)
            except UnicodeDecodeError as e:
                logger.debug('%s %s %s' %(codec, str(e), info))

    return document

class MultiTextCorpus(gensim.corpora.TextCorpus):
    def __init__(self, repo, ref=u'HEAD'):
        self.repo = repo
        if type(ref) is unicode:
            self.ref = ref.encode('utf-8')
        else:
            self.ref = ref

        assert type(self.ref) is str, 'ref is not a str, it is: %s' % str(type(self.ref))

        super(MultiTextCorpus, self).__init__('.')

    def get_texts(self):
        length = 0

        for k, file_info in self.repo.get_commit_files(self.ref).items():
            fname = file_info['path']
            document = file_info['data']
            if dulwich.patch.is_binary(document):
                continue
            document = to_unicode(document, ' '.join([fname, self.ref]))
            length += 1

            words = tokenize(document)
            # split
            # lower
            words = (word.lower() for word in words)
            # remove
            if self.metadata:
                yield words, (fname, u'en')
            else:
                yield words

        self.length = length # only reset after iteration is done.

class ChangesetCorpus(gensim.corpora.TextCorpus):

    def __init__(self, repo):
        self.repo = repo
        super(ChangesetCorpus, self).__init__('.')


    def _get_diff(self, changeset):
        """ Return a text representing a `git diff` for the files in the
        changeset.

        """
        patch_file = StringIO()
        dulwich.patch.write_object_diff(patch_file,
                self.repo.repo.object_store,
                changeset.old, changeset.new)
        return patch_file.getvalue()

    def _walk_changes(self, reverse=False):
        """ Returns one file change at a time, not the entire diff.

        """

        for walk_entry in self.repo.repo.get_walker(reverse=reverse):
            commit = walk_entry.commit

            # initial revision, has no parent
            if len(commit.parents) == 0:
                for changes in dulwich.diff_tree.tree_changes(
                        self.repo.repo.object_store,
                        None,
                        commit.tree):
                    diff = self._get_diff(changes)
                    yield commit.id, None, diff

            for parent in commit.parents:
                # do I need to know the parent id?

                for changes in dulwich.diff_tree.tree_changes(
                        self.repo.repo.object_store,
                        self.repo.repo[parent].tree,
                        commit.tree):
                    diff = self._get_diff(changes)
                    yield commit.id, parent, diff

    def get_texts(self):
        length = 0
        unified = re.compile(r'^[+ -].*')
        current = None
        low = list() # collecting the list of words

        for commit, parent, diff in self._walk_changes():
            # write out once all diff lines for commit have been collected
            # this is over all parents and all files of the commit
            if current is None:
                # set current for the first commit, clear low
                current = commit
                low = list()
            elif current != commit:
                # new commit seen, yield the collected low
                if self.metadata:
                    yield low, (current, u'en')
                else:
                    yield low
                length += 1
                current = commit
                low = list()


            # to process out whitespace only changes, the rest of this
            # loop will need to be structured differently. possibly need
            # to actually parse the diff to gain structure knowledge
            # (ie, line numbers of the changes).

            diff_lines = filter(lambda x: unified.match(x),
                                diff.splitlines())
            if len(diff_lines) < 2:
                continue # useful for not worrying with binary files

            # sanity?
            assert diff_lines[0].startswith('--- '), diff_lines[0]
            assert diff_lines[1].startswith('+++ '), diff_lines[1]
            #parent_fn = diff_lines[0][4:]
            #commit_fn = diff_lines[1][4:]

            diff_lines = diff_lines[2:] # chop off file names hashtag rebel
            lines = [line[1:] for line in diff_lines] # remove unified markers
            document = ' '.join(lines)
            if dulwich.patch.is_binary(document):
                continue
            document = to_unicode(document, ' '.join([commit, str(parent), diff]))

            # call the tokenizer
            words = tokenize(document)
            # split
            # lower
            words = (word.lower() for word in words)
            # remove
            low.extend(words)

        if self.metadata:
            # have reached the end, yield whatever was collected last
            yield low, (current, u'en')
        else:
            yield low
        length += 1

        self.length = length # only reset after iteration is done.
