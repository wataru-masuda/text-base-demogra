# -*- coding: utf-8 -*-
import argparse
import sys

from gensim.corpora.dictionary import Dictionary

from text_process import fetch_contents_from_url, doc2word_list


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--use_domain", action="store_true")
    parser.add_argument("--update", action="store_true")
    parser.add_argument("--save_interval", type=int, default=100)
    args = parser.parse_args()

    if args.update:
        common_dict = Dictionary.load_from_text("./common_dict.txt")
    else:
        common_dict = Dictionary()
    for i, url in enumerate(sys.stdin):
        print("url " + str(i))
        text = fetch_contents_from_url(url.strip(), use_domain=args.use_domain)
        if not text:
            continue

        word_list = doc2word_list(text)
        common_dict.add_documents([word_list])
        
        if i % args.save_interval == args.save_interval - 1:
            common_dict.save_as_text("./common_dict.txt")

    common_dict.save_as_text("./common_dict.txt")

if __name__ == "__main__":
    main()
