import os
import subprocess


def run_python_file(working_directory, file_path, args=None):

    try:
        working_directory_abs = os.path.abspath(working_directory)

        absolute_file_path = os.path.normpath(
            os.path.join(working_directory, file_path))

        is_file_within_scope = os.path.commonpath(
            [absolute_file_path, working_directory_abs]) == working_directory_abs

        if not is_file_within_scope:
            raise RuntimeError(
                f'Cannot execute "{file_path}" as it is outside the permitted working directory')

        if not os.path.isfile(absolute_file_path):
            raise RuntimeError(
                f'"{file_path}" does not exist or is not a regular file')

        if not file_path.endswith(".py"):
            raise RuntimeError(f'"{file_path}" is not a Python file')

        command = ["python", absolute_file_path]

        command.extend([args])

        result = subprocess.run(
            command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)

        if result.stderr is not None:
            raise RuntimeError(f'Command failed to run due to {result.stderr}')

        output_text = ""
        if result.check_returncode() == 0:
            output_text = f"STDOUT: {result.STDOUT}"
        else:
            output_text = f'Process exited with code {result.check_returncode()}'

    except RuntimeError as e:

        return f"Error: {e}"
