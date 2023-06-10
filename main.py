import os
import sys

from data.SourceFile import SourceFile
from data.UMLFile import UMLFile
from utils.ModuleParser import get_module_info
from utils.PlantEncoder import encode
from utils.VariableParser import add_variable_information


def generate_uml(directory: str) -> str:
    """
    Generates a valid PlantUML string for all files in the given directory and its subdirectories.

    :param directory: The directory to process.
    :return: A valid PlantUML string.
    """
    known_modules: list[str] = []
    source_files: list[SourceFile] = []
    for root, _, files in os.walk(directory):
        for file in files:
            if '.py' in file:
                file_path: str = os.path.join(root, file.split('.')[0])
                if 'venv' not in file_path and \
                        '/.' not in file_path and \
                        '__' not in file_path:
                    known_modules.append('.'.join(file_path[(len(directory) + 1):].split(os.sep)))

    for root, _, files in os.walk(directory):
        for file in files:
            if '.py' in file:
                file_path: str = os.path.join(root, file)
                if 'venv' not in file_path and \
                        '/.' not in file_path and \
                        '__' not in file_path:
                    source_files.append(
                        add_variable_information(
                            file_path,
                            get_module_info(file_path, known_modules)
                        )
                    )
    return str(UMLFile(source_files))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please provide a path to your project!', file=sys.stderr)
        sys.exit(1)
    uml: str = generate_uml(sys.argv[1])
    if len(sys.argv) > 2:
        print(encode(uml, sys.argv[2]))
    else:
        print(uml)
