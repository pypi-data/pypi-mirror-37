from os import path
import sys

here = path.abspath(path.dirname(__file__))
sys.path.append(here)

if __name__ == "__main__":
    from nauta import main
    main(sys.argv[1:])
