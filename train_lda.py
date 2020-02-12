import argparse
import datetime
import os
import sys

import dask.dataframe as dd
from gensim.models.ldamodel import LdaModel
from gensim.models import TfidfModel


def validate_date_arg(arg):
    if len(arg) != 8:
        print("[ERROR] Invalid format of argument '{}'. Correct format is '%Y%m%d'".format(
            arg), file=sys.stderr)
        sys.exit(1)
    if not arg.isdigit():
        print("[ERROR] Invalid type of argument '{}'. It must be digit".format(
            arg), file=sys.stderr)
        sys.exit(1)


def convert_bow2topics(row, lda):
    corpus = [(bow.split(":")[0], bow.split(":")[1])
              for bow in row["bow"].split()]
    try:
        doc_topics = lda.get_document_topics(corpus, minimum_probability=1e-30)
        doc_topics = [str(tup[0])+":"+str(tup[1]) for tup in doc_topics]
        row["topics"] = "\t".join(doc_topics)
        return row.drop("bow")
    except:
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", type=str, default="lda_tfidf.model")
    parser.add_argument("--rawdata_gcs_prefix", type=str,
                        default="gs://geniee-test-gcs/gid2bow_")
    parser.add_argument("--date_user_actions_log", type=str, default=None)
    parser.add_argument("--training_dataset_size", type=int, default=1000000)
    parser.add_argument("--num_topics", type=int, default=8)
    args = parser.parse_args()

    date_user_actions_log = args.date_user_actions_log if args.date_user_actions_log else (
        datetime.datetime.now() - datetime.timedelta(1)).strftime("%Y%m%d")
    validate_date_arg(date_user_actions_log)

    rawdata_gcs_pattern = args.rawdata_gcs_prefix + date_user_actions_log +  "-*.csv.gz"
    gid2bow = dd.read_csv(
        rawdata_gcs_pattern, compression="gzip")

    gid2bow_sample = gid2bow.compute()[:args.training_dataset_size]
    corpus = []
    gid2bow_sample_list = list(gid2bow_sample["bow"])
    for row in gid2bow_sample_list:
        bow_list = []
        for b in row.split():
            index, freq = b.split(":")
            bow_list.append((int(index), int(freq)))
        corpus.append(bow_list)

    tfidf = TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    lda = LdaModel(corpus_tfidf, num_topics=args.num_topics)

    lda.save(args.model_path)


if __name__ == "__main__":
    main()
