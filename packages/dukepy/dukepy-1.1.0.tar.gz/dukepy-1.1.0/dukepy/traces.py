import traceback
from dukepy.config import Config


def print_exception_traces(e):
    config = Config()
    if config["stacktrace"]:
        print(traceback.format_exc())
    else:
        print(e)


if __name__ == "__main__":
    mydict = dict()
    try:
        print(mydict["sdf"])
    except Exception as e:
        print_exception_traces(e)
