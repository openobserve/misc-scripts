# Download parquet files from S3/GCS

e.g.

### Download from GCS



```bash
mkdir logs

gsutil -m cp -r \
  "gs://bucket/files/org/logs/default/2023/10/18/00" \
  "gs://bucket/files/org/logs/default/2023/10/18/01" \
  logs
```

### Ingest parquet files

```bash
python ingest_parquet.py logs/00
```


