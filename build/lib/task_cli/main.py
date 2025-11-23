import argparse

parser = argparse.ArgumentParser()
parser.add_argument("name")
args = parser.parse_args()

def main():
    return print("Привет,", args.name)

if __name__ == '__main__':
    main()