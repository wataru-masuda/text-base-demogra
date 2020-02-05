# -*- coding: utf-8 -*-
import argparse
import sys

from gensim.corpora.dictionary import Dictionary

from text_process import fetch_contents_from_url, doc2word_list

            
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--use_domain", action="store_true")
    parser.add_argument("--update", action="store_true")
    args = parser.parse_args()

    common_dict = Dictionary.load_from_text("./common_dic.txt")

    f = open("url2bow_map.csv", "a")
    for i, url in enumerate(sys.stdin):
        print("url " + str(i))
        text = fetch_contents_from_url(url.strip(), use_domain=args.use_domain)
        if not text:
            continue
        
        word_list = doc2word_list(text)
        bow = common_dict.doc2bow(word_list)
        if bow:
            print(bow)
            for b in bow:
                f.write(url.strip() + "," + str(b[0]) + "," + str(b[1]) + "\n")
        if i % 100 == 99:
            f.close()
            f = open("url2bow_map.csv", "a")
    f.close()
            
if __name__ == "__main__":
    main()
