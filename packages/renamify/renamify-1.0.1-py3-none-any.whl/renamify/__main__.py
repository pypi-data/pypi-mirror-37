from argparse import ArgumentParser
from renamify.core import bulk_rename


def get_args():
    parser = ArgumentParser(description="Rename files in bulk using regular expressions for matching.")
    parser.add_argument('source_pattern', metavar='file_match_pattern', action='store',
                        help="The pattern to use to match file names to rename.")
    parser.add_argument('target_pattern', metavar='file_rename_pattern', action='store',
                        help="The pattern to use to determine what name to save renamed files as.")
    parser.add_argument('-d', '--dir', dest='input_dir', action='store', default=None,
                        help=("The directory to operate in during the rename process. Defaults to the working directory"
                              " of the user when invoked."))
    parser.add_argument('-o', '--output-dir', dest='output_dir', action='store', default=None,
                        help=("The directory to place renamed files in. Defaults to the value of the -d flag if not"
                              " provided."))
    parser.add_argument('-a', '--all', dest='include_dirs', action='store_true', default=False,
                        help="Instructs the tool to rename directories as well as files.")
    parser.add_argument('-n', '--dry-run', dest='dry_run', action='store_true', default=False,
                        help="Do not actually perform the copy. Useful for building patterns for matching.")
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    rename_kwargs = {'rename_dirs': args.include_dirs, 'dry_run': args.dry_run}
    if args.input_dir is not None:
        rename_kwargs['input_dir'] = args.input_dir
    if args.output_dir is not None:
        rename_kwargs['output_dir'] = args.output_dir
    rename_manifest = bulk_rename(args.source_pattern, args.target_pattern, **rename_kwargs)
    if len(rename_manifest) > 0:
        print("Renamed %d files:" % len(rename_manifest))
        for input_file, output_file in rename_manifest:
            print("    %s  ->  %s" % (input_file, output_file))
    else:
        print("No files renamed - no files matched match pattern?")
