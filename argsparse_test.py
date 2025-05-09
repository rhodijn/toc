import argparse, datetime, json, os, paramiko, project_data, re

def get_file():
    """
    Get path to toc file from input

    Returns:
    args.file : str = path to to file
    """
    parser = argparse.ArgumentParser(
        prog = 'toc uploader',
        description = 'upload toc to ftp-server from terminal',
        epilog = 'zhaw hsb, cc-by-sa'
    )
    parser.add_argument('-f', '--file', required=True, type=str, help='name of toc file')
    parser.add_argument('-p', '--path', required=False, type=str, help='name of toc file')
    parser.add_argument('-l', '--lib', required=True, type=str, help='library, used for remote path')

    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = get_file()
    print(f'file: {args.file}, path: {args.path.rstrip('/')}, lib: {args.lib}')
    if not re.search('\\b[wW][aAiI][eEnN]\\b', args.lib):
        print('please specify a valid library')