import traceback
from app import Config


def print_exception_traces(e):
    config = Config()
    if config["stacktrace"]:
        print(traceback.format_exc())
    else:
        print(e)
