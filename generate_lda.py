import argparse
import datetime
import os
import sys

import dask.dataframe as dd
from gensim.corpora import Dictionary
from gensim.models.ldamodel import LdaModel


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
    parser.add_argument("--common_dict", type=str, default="common_dict.txt")
    parser.add_argument("--model_path", type=str, default="lda_tfidf.model")
    parser.add_argument("--rawdata_gcs_prefix", type=str,
                        default="gs://geniee-test-gcs/gid2bow_")
    parser.add_argument("--date_user_actions_log", type=str, default=None)
    args = parser.parse_args()

    date_user_actions_log = args.date_user_actions_log if args.date_user_actions_log else (
        datetime.datetime.now() - datetime.timedelta(1)).strftime("%Y%m%d")
    validate_date_arg(date_user_actions_log)

    dictionary = Dictionary.load_from_text(args.common_dict)

    lda = LdaModel.load(args.model_path)

    rawdata_gcs_pattern = args.rawdata_gcs_prefix + date_user_actions_log +  "-*.csv.gz"
    gid2bow = dd.read_csv(
        rawdata_gcs_pattern, compression="gzip")

    gcs_upload_path = os.path.join(args.rawdata_gcs_prefix.replace("bow_", "topics"), date_user_actions_log + "-*.csv.gz")
    gid2bow.apply(convert_bow2topics, lda=lda, axis=1, meta={"gid": "str", "topics": "str"}).dropna(
    ).to_csv(gcs_upload_path, index=None, compression='gzip')


if __name__ == "__main__":
    main()
