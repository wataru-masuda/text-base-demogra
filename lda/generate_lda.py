import argparse
import gzip
import sys

from gensim.models.ldamodel import LdaModel


def convert_bow2topics(bow, lda):
    corpus = [(b.split(":")[0], b.split(":")[1])
              for b in bow.split()]
    try:
        topics = lda.get_document_topics(corpus, minimum_probability=1e-30)
        topics = [str(tup[0])+":"+str(tup[1]) for tup in topics]
        topics = "\t".join(topics)
        return topics
    except Exception:
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    parser.add_argument("--model_path", type=str, default="lda_tfidf.model")
    args = parser.parse_args()

    lda = LdaModel.load(args.model_path)

    rf = gzip.open(args.filename, "rt")
    wf = gzip.open(args.filename.replace("bow", "topics"), "wt")
    for i, row in enumerate(rf):
        if i == 0:
            continue
        gid, bow = row.split(",", 1)
        topics = convert_bow2topics(bow, lda)
        sys.stdout.write("\r{}, {}".format(i, topics))
        if topics:
            wf.write(gid + "," + topics + "\n")

    rf.close()
    wf.close()
    

if __name__ == "__main__":
    main()
