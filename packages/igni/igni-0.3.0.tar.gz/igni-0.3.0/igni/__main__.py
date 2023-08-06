import sys
from igni import run


def main():
    if len(sys.argv) < 2:
        print("No argument supplied")

    print(run(sys.argv))


if __name__ == "__main__":
    main()
