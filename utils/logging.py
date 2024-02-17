from sys import stdout

from loguru import logger

format = "{time:YYYY-MM-DD HH:mm:ss Z}| {level} | {name}:{line} | {message}"
config = {
    "handlers": [
        {
            "sink": "logs/service.log",
            "format": format,
            "level": "DEBUG",
            "enqueue": True,
            "backtrace": True,
            "rotation": "100MB",
        },
        {
            "sink": "logs/service.json.log",
            "format": format,
            "serialize": True,
            "level": "DEBUG",
            "enqueue": True,
            "backtrace": True,
            "rotation": "100MB",
        },
        {"sink": stdout, "format": format, "level": "DEBUG", "enqueue": True},
    ]
}
logger.configure(**config)
