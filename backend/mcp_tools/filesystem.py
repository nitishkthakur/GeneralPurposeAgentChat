"""Filesystem MCP tools for file operations."""

import os
from pathlib import Path
from typing import Optional

from langchain_core.tools import tool


@tool
def read_file(file_path: str) -> str:
    """Read the contents of a file.

    Args:
        file_path: The path to the file to read.

    Returns:
        The contents of the file as a string.
    """
    try:
        path = Path(file_path).resolve()
        if not path.exists():
            return f"Error: File '{file_path}' does not exist."
        if not path.is_file():
            return f"Error: '{file_path}' is not a file."
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except PermissionError:
        return f"Error: Permission denied to read '{file_path}'."
    except Exception as e:
        return f"Error reading file: {str(e)}"


@tool
def write_file(file_path: str, content: str) -> str:
    """Write content to a file. Creates the file if it doesn't exist.

    Args:
        file_path: The path to the file to write.
        content: The content to write to the file.

    Returns:
        A success message or error description.
    """
    try:
        path = Path(file_path).resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote to '{file_path}'."
    except PermissionError:
        return f"Error: Permission denied to write to '{file_path}'."
    except Exception as e:
        return f"Error writing file: {str(e)}"


@tool
def list_directory(directory_path: str) -> str:
    """List the contents of a directory.

    Args:
        directory_path: The path to the directory to list.

    Returns:
        A formatted list of files and directories.
    """
    try:
        path = Path(directory_path).resolve()
        if not path.exists():
            return f"Error: Directory '{directory_path}' does not exist."
        if not path.is_dir():
            return f"Error: '{directory_path}' is not a directory."

        entries = []
        for entry in sorted(path.iterdir()):
            entry_type = "[DIR]" if entry.is_dir() else "[FILE]"
            entries.append(f"{entry_type} {entry.name}")

        if not entries:
            return f"Directory '{directory_path}' is empty."

        return "\n".join(entries)
    except PermissionError:
        return f"Error: Permission denied to access '{directory_path}'."
    except Exception as e:
        return f"Error listing directory: {str(e)}"


@tool
def create_directory(directory_path: str) -> str:
    """Create a new directory and any necessary parent directories.

    Args:
        directory_path: The path of the directory to create.

    Returns:
        A success message or error description.
    """
    try:
        path = Path(directory_path).resolve()
        path.mkdir(parents=True, exist_ok=True)
        return f"Successfully created directory '{directory_path}'."
    except PermissionError:
        return f"Error: Permission denied to create '{directory_path}'."
    except Exception as e:
        return f"Error creating directory: {str(e)}"


@tool
def delete_file(file_path: str) -> str:
    """Delete a file.

    Args:
        file_path: The path to the file to delete.

    Returns:
        A success message or error description.
    """
    try:
        path = Path(file_path).resolve()
        if not path.exists():
            return f"Error: File '{file_path}' does not exist."
        if not path.is_file():
            return f"Error: '{file_path}' is not a file."
        path.unlink()
        return f"Successfully deleted '{file_path}'."
    except PermissionError:
        return f"Error: Permission denied to delete '{file_path}'."
    except Exception as e:
        return f"Error deleting file: {str(e)}"


@tool
def get_file_info(file_path: str) -> str:
    """Get information about a file or directory.

    Args:
        file_path: The path to the file or directory.

    Returns:
        Information about the file including size, type, and modification time.
    """
    try:
        path = Path(file_path).resolve()
        if not path.exists():
            return f"Error: '{file_path}' does not exist."

        stat = path.stat()
        file_type = "directory" if path.is_dir() else "file"
        size = stat.st_size
        modified = stat.st_mtime

        from datetime import datetime

        modified_str = datetime.fromtimestamp(modified).isoformat()

        return f"Type: {file_type}\nSize: {size} bytes\nLast Modified: {modified_str}\nPath: {path}"
    except PermissionError:
        return f"Error: Permission denied to access '{file_path}'."
    except Exception as e:
        return f"Error getting file info: {str(e)}"


# Export all filesystem tools
filesystem_tools = [
    read_file,
    write_file,
    list_directory,
    create_directory,
    delete_file,
    get_file_info,
]
