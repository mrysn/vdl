import os

# File system limits
MAX_FILENAME_LENGTH = 255  # Max filename length for most filesystems
RESERVED_LENGTH = 50  # Reserved for directories, extensions, etc.
YT_DLP_FILENAME_TRIM_LENGTH = max(1, MAX_FILENAME_LENGTH - RESERVED_LENGTH)

# yt-dlp configuration
YT_DLP_DEFAULT_ARGS = [
    f"--trim-filenames", str(YT_DLP_FILENAME_TRIM_LENGTH),
    "--write-sub",
    "--write-auto-subs",
    "--sub-lang", "en.*",
    "--sub-format", "ttml",
    "--convert-subs", "srt",
    "--embed-subs",
    "--compat-options", "no-keep-subs",
    "--merge-output-format", "mp4",
    "--ignore-errors",
    "--restrict-filenames",
    "--no-check-certificate",
    "--force-ipv4",
    "--legacy-server-connect",
    "--convert-thumbnail", "jpg",
    "--embed-thumbnail",
    "--add-metadata",
    "--download-archive", "/downloads/yt-dlp-videos-mp4-maxquality.txt",
    "-P", "/downloads"
]

# Default filename output template
YT_DLP_OUTPUT_TEMPLATE = "/downloads/%(channel)s-%(upload_date)s-%(title)s-%(id)s-%(width)sp.%(ext)s"

# Logging configuration
LOG_FILE = os.getenv('LOG_FILE', 'app.log')  # Default log file location
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')  # Default log level (e.g., DEBUG, INFO, WARNING)

# Flask configuration
FLASK_PORT = int(os.getenv('FLASK_PORT', 5050))  # Flask app port
FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')  # Flask app host

# Redis configuration
REDIS_URL = os.getenv('REDIS_URL', 'redis://vdl-redis:6379/0')  # Redis broker URL

# Celery configuration
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
