import sys
import shutil
import os.path
import pathlib

from termcolor_util import red, yellow

from .program_arguments import ProgramArguments


def push_files_to_template(projects_folder: str,
                           args: ProgramArguments) -> None:

    if not args.parameter or len(args.parameter) < 2:
        print(red("Invalid number of parameters sent to push. Send at least project + 1 file"))
        sys.exit(1)

    project_name = args.parameter[0]

    for file_name in args.parameter[1:]:
        recursively_push_file(projects_folder, project_name, file_name)


def recursively_push_file(projects_folder: str,
                          project_name: str,
                          file_name: str) -> None:
    print(yellow("Pushing"),
          yellow(file_name, bold=True),
          yellow("to"),
          yellow(project_name, bold=True))

    target_file_name = os.path.join(projects_folder, project_name, file_name)
    if os.path.isdir(file_name):
        pathlib.Path(target_file_name).mkdir(parents=True, exist_ok=True)
        for nested_file_name in os.listdir(file_name):
            recursively_push_file(projects_folder=projects_folder,
                                  project_name=project_name,
                                  file_name=os.path.join(file_name, nested_file_name))
        return

    shutil.copy(file_name, target_file_name)
