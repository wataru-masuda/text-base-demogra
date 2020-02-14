# text-base-demogra

##  これは何？

ユーザの行動（訪問したurl）履歴からコンテンツ情報をスクレイピングにより抜き出し、次元圧縮等を施したものをそのユーザの特徴量として機械学習モデルの入力等に用いる。

## Requirements

- gensim

- beautifulsoup4

- mecab-python3

  Mecab

  ```
  brew install mecab mecab-ipadic git curl xz # 必要なもののみインストールする
  git clone --depth 1 git@github.com:neologd/mecab-ipadic-neologd.git
  cd mecab-ipadic-neologd
  ./bin/install-mecab-ipadic-neologd -n
  ```

- dask[dataframe]

- gcsfs



## 特徴量作成のための下準備

1. urlのリストから単語の辞書を作成する。

   ```shell
   cd preprocess
   cat sample_urllist.txt | pipenv run python make_common_dict.py
   ```

   

2. 単語辞書から不要な単語を除く（1でストップワードとして弾く処理を入れた方がいいかも）。

3. urlとBoW (Bag of Words) のマップを作る。

   ```shell
   cd preprocess
   cat sample_urllist.txt | pipenv run python make_url2bow_map.py
   ```

   

4. 3で作成した`url2bow.csv`を参照して、bqテーブルを作成する。

   https://console.cloud.google.com/bigquery?cloudshell=false&hl=ja&organizationId=426825513162&project=gj-lamp&p=gj-lamp&d=masuda_partial_data&t=url2bow&page=table

5. ユーザ行動履歴`masuda_partial_data.auction_user_actions_YYYYmmdd`テーブルと4で作成したurl2bowテーブルから、gidごとのBoWを作成する。

6. 5で作成したgid2bowテーブルをdaskで読み込めるようにgcsにエクスポートしておく。

## LDAモデルの学習

gidごとのbowからLDAモデルの学習を行う。

```
pipenv run python lda/train_lda.py 
```

オプション

- model_path : ldaモデルファイルの保存先。`default="./lda_tfidf.model"`
- rawdata_gcs_prefix : 学習データのパスのprefix。学習データのファイル名は`rawdata_gcs_prefix + <YYYYmmdd> +  "-*.csv.gz"`になる。`default="gs://geniee-test-gcs/gid2bow_"`
- date_user_actions_log : 学習データに用いるユーザ行動履歴のlogの日付。設定しない場合は一昨日の日付になる。
- training_dataset_size : 学習データのサイズ。`default=1000000`
- num_topics : LDAモデルのトピック数。`default=8`

## 特徴量作成

学習済みLDAモデルでgidごとのBoWからgidごとのtopicsに変換する。

```
pipenv run python lda/generate_lda.py
```

オプション

- model_path : 学習済みldaモデルファイルの保存先。`default="./lda_tfidf.model"`

- rawdata_gcs_prefix : 生成用データのパスのprefix。`default="gs://geniee-test-gcs/gid2bow_"`

  デフォルトの値の場合、生成されたgidごとの特徴量のデータファイルのパスは`gs://geniee-test-gcs/gid2topics/<YYYYmmdd>-*.csv.gz`になる。

- date_user_actions_log : 生成用データに用いるユーザ行動履歴のlogの日付。設定しない場合は一昨日の日付になる。

