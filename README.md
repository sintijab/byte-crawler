
# Web crawler for byte.fm archive

## Install virtualenv and deps
```python
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
```

## Run the application
```sh
    python app.py --dates YYYY-MM-DD YYYY-MM-DD
```

## Clear duplicates from two files
```sh
    python3 clear_duplicates.py compare FILE_1.txt FILE_2.txt
```

## Clear duplicates from a single file
```sh
    python clear_duplicates.py dedup FILE_1.txt
```

## Clear duplicates by title from JSON
```sh
    python dedup_json_by_title.py FILE_1.json
```

## Clear errors from logs
```sh
    python clear_errors.py error_log.txt
```

## Run with docker
```sh
    docker build -t sound-archive .
    docker run sound-archive --date 2025-05-11
```

## Troubleshooting
```sh
 python test.py
```
