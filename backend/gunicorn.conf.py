import os
import multiprocessing

# Workers
workers = multiprocessing.cpu_count() * 2 + 1  # Adjust based on your app's needs
worker_class = "uvicorn.workers.UvicornWorker"  # Use Uvicorn for ASGI support

# Binding
bind = "0.0.0.0:{}".format(os.environ.get("PORT", 8080))
# Cloud Run provides the PORT; defaults to 8080 locally

# Logging (adjust as needed)
accesslog = "-"  # Log to stdout
errorlog = "-"

# Timeouts (adjust based on your API's typical response times)
timeout = 60
keepalive = 5

# Worker Processes (adjust for your needs)
worker_connections = 1000
