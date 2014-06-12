Topic of Change
===============

Basic idea: compare LDA models built with two different sources of documents. The first being a traditional source code snapshot, and the second being variations on a changeset snapshot.

Be sure to read [Contributing](https://github.com/cscorley/topic-of-change/wiki/Contributing)

### Using the Wiki

Log all progress in the [wiki](https://github.com/cscorley/topic-of-change/wiki) (on left).

The project description can be found there, as well.

### Installing

You will need to install a few libraries before you can begin work on
this project. 

    $ pip install -r requirements.txt

This *should* take care of everything you'll need. Next, install this
project as an 'editable' version (changes propagate without reinstall).

    $ pip install --editable .

Now, you should be able to run commands:

    $ topicofchange --help

    Usage: topicofchange [OPTIONS] COMMAND [ARGS]...

      Topic of Change

    Options:
      --verbose
      --help     Show this message and exit.

    Commands:
      corpora     Builds the basic corpora for a project
      evaluate    Evalutates the models
      model       Builds a model for the corpora
      preprocess  Runs the preprocessing steps on a corpus
      run_all     Runs corpora, preprocess, model, and evaluate...
