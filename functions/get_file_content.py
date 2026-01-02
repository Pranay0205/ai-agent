import os

from config import MAX_CHARS
from google.genai import types


def get_file_content(working_directory, file_path) -> str:

    try:
        working_dir_abs = os.path.abspath(working_directory)

        absolute_file_path = os.path.normpath(
            os.path.join(working_dir_abs, file_path))

        is_file_within_scope = os.path.commonpath(
            [working_dir_abs, absolute_file_path]) == working_dir_abs

        if not is_file_within_scope:
            raise RuntimeError(
                f'Cannot list "{file_path}" as it is outside the permitted working directory')

        if not os.path.isfile(absolute_file_path):
            raise RuntimeError(
                f'File not found or is not a regular file: "{file_path}"')

        with open(absolute_file_path, "r") as f:
            file_content = f.read(MAX_CHARS)

            if f.read(1):
                file_content += f' [...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return file_content

    except RuntimeError as err:
        return f"Error: {err}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the text content of a file at the specified path relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to file to retrieve content from, relative to the working directory",
            ),
        },
        required=["file_path"]
    ),

)
