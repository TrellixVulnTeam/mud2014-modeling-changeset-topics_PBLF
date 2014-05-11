Topic of Change
===============

Basic idea: compare LDA models built with two different sources of documents. The first being a traditional source code snapshot, and the second being variations on a changeset snapshot.

### Model sources

1. Traditional source code snapshot:
    - Each document is a text file in the release
    - No programming language parsing, just use the entire file for now
2. Changeset snapshot:
    - Each document is the diff between two commits
    - Will use some parsing to get rid of metadata and split the diff into groups of:
          - added lines
          - removed lines
          - context lines
          - all combinations of the above 3
    - This will produce several sets of documents, each of which can be compared to the traditional documents
    - The 'pilot' study can just use all of the lines: added & removed & context
    - The 'extended' study will look at which combination is better is the pilot seems successful

### Preprocessing

All documents in from all sources will need some pre-processing:
    - All punctuation removed
    - English stop words removed
    - Programming language keywords removed (e.g. if, while, for, &c)
    - camelCase and under_score words are split into: camel, case, under, score
    - All words converted into lowercase utf-8 strings

### Training the models

Use gensim.

### Evaluation

Once the models are built, we need to have a way to evaluate them.

One thing we can do is calculate the perplexity of the model with a held-out corpus. That is, withhold 80% of the documents when training each model and calculate the perplexity on the remaining 20%. This is how Blei's group evaluates their modeling techniques.

Can use a query-based evaluation system similar to Bassett & Kraft (ICPC'13). Not sure how to compare the two models, since one is built on file-based documents and another commit-based documents. It would be possible to split the commit-based documents further into their respective files so that each `document_nm` would be the changes that occured to `file n` at `commit m`.


### Idea box:

- We could extend the comparison to include LSI
