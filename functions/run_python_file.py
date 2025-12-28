import os
import subprocess
from sys import stdout


def run_python_file(working_directory, file_path, args=None):

    try:
        working_dir_abs = os.path.abspath(working_directory)

        absolute_file_path = os.path.normpath(
            os.path.join(working_dir_abs, file_path))

        is_file_within_scope = os.path.commonpath(
            [working_dir_abs, absolute_file_path]) == working_dir_abs

        if not is_file_within_scope:
            raise RuntimeError(
                f'Cannot execute "{file_path}" as it is outside the permitted working directory')

        if not os.path.isfile(absolute_file_path):
            raise RuntimeError(
                f'"{file_path}" does not exist or is not a regular file')

        if not file_path.endswith(".py"):
            raise RuntimeError(f'"{file_path}" is not a Python file')

        command = ["python", absolute_file_path]

        if args is not None:
            command.extend(args)

        result = subprocess.run(
            command, cwd=working_dir_abs, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)

        output_text = ""
        if result.returncode != 0:
            output_text = f'Process exited with code {result.returncode}\n'

        if result.stdout is None and result.stderr is None:
            output_text = f"No output produced"

        else:
            if result.stdout is not None:
                output_text += f'STDOUT: {result.stdout}'

            if result.stderr is not None:
                output_text += f'STDERR: {result.stderr}'

        return output_text
    except Exception as e:
        return f"Error: executing Python file: {e}"
