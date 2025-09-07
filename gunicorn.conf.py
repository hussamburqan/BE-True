# gunicorn.conf.py
import os, multiprocessing

bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"
workers = int(os.getenv("WEB_CONCURRENCY", (multiprocessing.cpu_count() * 2) + 1))
threads = int(os.getenv("GUNICORN_THREADS", "2"))
worker_class = "gthread"

timeout = int(os.getenv("GUNICORN_TIMEOUT", "60"))
graceful_timeout = int(os.getenv("GUNICORN_GRACEFUL_TIMEOUT", "30"))
keepalive = int(os.getenv("GUNICORN_KEEPALIVE", "5"))

loglevel = os.getenv("LOG_LEVEL", "info")
accesslog = "-"
errorlog = "-"

preload_app = os.getenv("GUNICORN_PRELOAD", "1") == "1"
