import os
from google.genai import types


def get_files_info(working_directory, directory=".") -> str:

    try:
        working_dir_abs = os.path.abspath(working_directory)

        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        valid_target_dir = os.path.commonpath(
            [working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            raise RuntimeError(
                f'Cannot list "{directory}" as it is outside the permitted working directory')

        if not directory:
            raise RuntimeError(
                f'"{directory}" is not a directory')

        files_info = []
        with os.scandir(target_dir) as entries:
            for entry in entries:
                file_name = entry.name
                file_size = entry.stat().st_size
                is_dir = entry.is_dir()
                files_info.append(
                    f"- {file_name}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(files_info)

    except RuntimeError as err:
        return (f"Error: {err}\n")


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
