
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
    python clear_duplicates.py compare FILE_1.txt FILE_2.txt
```

## Clear duplicates from a single file
```sh
    python clear_duplicates.py dedup FILE_1.txt
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
