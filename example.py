import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Script to upload toc to ftp-server from CMD"
    )
    parser.add_argument("--file", required=True, type=str)
    args = parser.parse_args()

    f_name = args.file

    print(f'uploading file {f_name}')

# Running the script from the command line:
# python3 example.py --file=123.pdf