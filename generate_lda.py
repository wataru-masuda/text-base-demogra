import argparse

import dask.dataframe as dd
from gensim.corpora import Dictionary
from gensim.models.ldamodel import LdaModel


def convert_bow2topics(row):
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
    parser.add_argument("--rawdata_gcs_pattern", type=str,
                        default="gs://geniee-test-gcs/gid2bow_partial_20200202csv.gz")
    args = parser.parse_args()

    dictionary = Dictionary.load_from_text(args.common_dict)

    lda = LdaModel.load(args.model_path)

    gid2bow = dd.read_csv(
        args.rawdata_gcs_pattern, compression="gzip")

    gid2bow.apply(convert_bow2topics, axis=1, meta={"gid": "str", "topics": "str"}).dropna(
    ).to_csv("./gid2topics_partial_20200202", index=None, compression='gzip')


if __name__ == "__main__":
    main()
