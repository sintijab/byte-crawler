
# Web crawler for byte.fm archive

## Install virtualenv and deps
```python
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
```

## Run the application
```sh
    python app.py --date=YYYY-MM-DD
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
