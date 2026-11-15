import sys
from app.bootstrap import Bootstrap


def main():
    # Parse log level from command line if provided
    log_level = "INFO"  # default
    for arg in sys.argv[1:]:
        if arg in ("-l", "--level"):
            idx = sys.argv.index(arg) + 1
            if idx < len(sys.argv):
                log_level = sys.argv[idx]

    app = Bootstrap(log_level=log_level)
    app.start()


if __name__ == "__main__":
    main()