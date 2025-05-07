import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Script to upload toc to ftp-server from CMD"
    )
    parser.add_argument("--file", required=True, type=str)
    args = parser.parse_args()

    file = args.file

    print(f'upload file {file}')

# Running the script from the command line.

# python tests.py --num1=1 --num2=2 --num3=3