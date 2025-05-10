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
    parser.add_argument('-l', '--lib', required=False, type=str, default='', help='library, used for remote path')

    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = get_file()
    p_local = args.file.split('/')
    f_name = p_local[-1]
    print('/'.join([x for x in p_local[:-1]]) + '/')
    print(f_name)
    print(args.file.split('/')[-1])
    print(f'file: {args.file.split("/")[-1]}, path: {args.file.split("/")[:-1]}, lib: {args.lib}')
    if not re.search('\\bw[ai][en]\\b', args.lib.lower()):
        print('please specify a valid library')