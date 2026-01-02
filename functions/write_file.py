import os
from google.genai import types


def write_file(working_directory, file_path, content) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)

        target_file_path = os.path.normpath(
            os.path.join(working_directory_abs, file_path))

        valid_target_file = os.path.commonpath(
            [working_directory_abs, target_file_path]) == working_directory_abs

        if not valid_target_file:
            raise RuntimeError(
                f'Cannot write to "{file_path}" as it is outside the permitted working directory')

        if os.path.isdir(target_file_path):
            raise RuntimeError(
                f'Cannot write to "{file_path}" as it is a directory')

        os.makedirs(os.path.dirname(target_file_path), exist_ok=True)

        with open(target_file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except RuntimeError as e:
        return f'Error: {e}'

    except Exception as e:
        return f'Error: {e}'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file in the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)
