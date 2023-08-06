import collections
import os
import re
import shutil


def bulk_rename(input_pattern, output_pattern, input_dir=None, output_dir=None, rename_dirs=False, dry_run=False):
    if input_dir is None:
        input_dir = os.getcwd()
    if output_dir is None:
        output_dir = input_dir
    if not os.path.isdir(input_dir):
        raise ValueError("Provided input directory does not exist.")
    if not os.path.isdir(output_dir):
        raise ValueError("Provided output directory does not exist.")
    match_pattern = re.compile(r'^%s$' % input_pattern)
    # generate the list of files to be moved
    file_move_list = []
    for file_name in os.listdir(input_dir):
        full_input_path = os.path.join(input_dir, file_name)
        if os.path.isdir(full_input_path) and not rename_dirs:
            # skip directories if we haven't been given the rename_dirs flag
            continue
        if not match_pattern.fullmatch(file_name):
            # file doesn't match the input pattern - skip it
            continue
        new_file_name = re.sub(match_pattern, output_pattern, file_name)
        full_output_path = os.path.join(output_dir, new_file_name)
        file_move_list.append((full_input_path, full_output_path))
    # analyze the output paths so that we can do some safety checks before moving files
    output_counts = collections.defaultdict(int)
    output_targets_exist = collections.defaultdict(bool)
    for _, output_file in file_move_list:
        output_counts[output_file] += 1
        if os.path.exists(output_file):
            output_targets_exist[output_file] = True
    # make sure we don't have any duplicate output paths
    if sum(output_counts.values()) != len(output_counts):
        _error_str_lines = ["Multiple source files to be renamed to the same output filename:"]
        for input_file, output_file in file_move_list:
            if output_counts[output_file] > 1:
                _error_str_lines.append("    %s  ->  %s" % (input_file, output_file))
        _error_str_lines.append("Please adjust your replacement pattern to make renames unique in order to continue.")
        raise ValueError(os.linesep.join(_error_str_lines))
    # make sure none of the targets already exist - we don't want to overwrite existing files
    if True in output_targets_exist:
        _error_str_lines = ["One or more output paths already exist and would be overwritten:"]
        for output_file in output_targets_exist.keys():
            if output_targets_exist[output_file]:
                _error_str_lines.append("    %s" % output_file)
        _error_str_lines.append("Please adjust your replacement pattern or move files around in order to continue.")
        raise ValueError(os.linesep.join(_error_str_lines))
    # we have our list of move targets and there are no duplicates - do the move if we aren't in a dry run
    for source_path, target_path in file_move_list:
        if not dry_run:
            shutil.move(source_path, target_path)
    return file_move_list
