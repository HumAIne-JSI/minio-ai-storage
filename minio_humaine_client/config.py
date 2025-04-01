import os

DEFAULT_BASE_URL = os.getenv("HUMAINE_API_BASE_URL", "https://humaine-minio-api.euprojects.net")
REQUEST_TIMEOUT = int(os.getenv("HUMAINE_API_TIMEOUT", 30))
