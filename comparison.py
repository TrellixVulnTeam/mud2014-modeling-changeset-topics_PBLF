from gensim.corpora import MalletCorpus, Dictionary
import sys 

def read_project_data(mtc,csc, fname): 
    d1 = Dictionary.load(mtc + ".dict") 
    d2 = Dictionary.load(csc + ".dict")
    #d3 = Dictionary.load('data/postgresql-d4f8dde3-CommitLogCorpus.mallet.dict')
    
    MultiTextCorpus = MalletCorpus(mtc, d1) 
    ChangesetCorpus = MalletCorpus(csc, d2)
    #CommitLogCorpus = MalletCorpus('data/postgresql-d4f8dde3-CommitLogCorpus.mallet', d3)
    
    u1 = set(d1.values())
    u2 = set(d2.values())
    #u3 = set(d3.values())
    
    common = u1.intersection(u2)
    uc_set = (len(u1),len(u2))

    u1_uniq = u1.difference(common)
    u2_uniq = u2.difference(common)
    print(u1_uniq)
    
    fname = "common_words_comparison.txt"
    with open(fname, 'a') as f:
        parts = mtc.split("-")
        f.write(str(parts[0]) + "\n")
        f.write("length of MultiTextCorpus: " + str(len(MultiTextCorpus)) + "\n")
        f.write("length of ChangesetCorpus: " + str(len(ChangesetCorpus)) + "\n" + "\n")
        f.write("(MTC,CSC)  in common" + "\n")
        f.write(str(uc_set) + " " + str(len(common)))
        f.write('\n' + '\n')
        #f.write("note: the length of the multitext corpus and changeset corpus is off by 2. specifically ~ set([u'rapha', u'lalev']) these words occur in the snapshot & not the changeset.")

read_project_data('data/jodatime-b0fcbb95-MultiTextCorpus.mallet','data/jodatime-b0fcbb95-ChangesetCorpus.mallet') 

