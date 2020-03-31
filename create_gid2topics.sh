DATE="20200328"
bq extract --compression GZIP masuda_partial_data.gid2bow_$DATE gs://geniee-test-gcs/gid2bow_$DATE-*.csv.gz
gsutil cp gs://geniee-test-gcs/gid2bow_$DATE*.csv.gz .
gsutil rm gs://geniee-test-gcs/gid2bow_$DATE*.csv.gz
ls -1 gid2bow_$DATE*.csv.gz | xargs -P16 -IXXX pipenv run python3 lda/generate_lda.py XXX
gsutil mv gid2topics_$DATE-* gs://geniee-test-gcs/
bq load --source_format=CSV masuda_partial_data.gid2topics_$DATE gs://geniee-test-gcs/gid2topics_$DATE*.csv.gz gid:STRING,topic_index:INTEGER,prob:FLOAT
gsutil rm gs://geniee-test-gcs/gid2topics_$DATE*.csv.gz
