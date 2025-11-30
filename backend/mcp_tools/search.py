"""Search MCP tools for searching files and content."""

import os
import re
from pathlib import Path
from typing import Optional

from langchain_core.tools import tool


@tool
def search_files(
    directory: str, pattern: str, max_results: int = 50
) -> str:
    """Search for files matching a pattern in a directory.

    Args:
        directory: The directory to search in.
        pattern: The glob pattern to match files (e.g., '*.py', '**/*.txt').
        max_results: Maximum number of results to return (default 50).

    Returns:
        A list of matching file paths.
    """
    try:
        path = Path(directory).resolve()
        if not path.exists():
            return f"Error: Directory '{directory}' does not exist."
        if not path.is_dir():
            return f"Error: '{directory}' is not a directory."

        matches = []
        for match in path.glob(pattern):
            matches.append(str(match))
            if len(matches) >= max_results:
                break

        if not matches:
            return f"No files matching '{pattern}' found in '{directory}'."

        result = f"Found {len(matches)} file(s):\n"
        result += "\n".join(matches)
        if len(matches) >= max_results:
            result += f"\n\n(Results limited to {max_results})"

        return result
    except Exception as e:
        return f"Error searching files: {str(e)}"


@tool
def search_in_file(file_path: str, search_text: str, case_sensitive: bool = False) -> str:
    """Search for text within a file and return matching lines.

    Args:
        file_path: The path to the file to search in.
        search_text: The text to search for.
        case_sensitive: Whether the search should be case-sensitive (default False).

    Returns:
        Matching lines with line numbers.
    """
    try:
        path = Path(file_path).resolve()
        if not path.exists():
            return f"Error: File '{file_path}' does not exist."
        if not path.is_file():
            return f"Error: '{file_path}' is not a file."

        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        matches = []
        for i, line in enumerate(lines, 1):
            if case_sensitive:
                if search_text in line:
                    matches.append(f"Line {i}: {line.rstrip()}")
            else:
                if search_text.lower() in line.lower():
                    matches.append(f"Line {i}: {line.rstrip()}")

        if not matches:
            return f"No matches for '{search_text}' found in '{file_path}'."

        return f"Found {len(matches)} match(es):\n" + "\n".join(matches)
    except Exception as e:
        return f"Error searching in file: {str(e)}"


@tool
def search_in_directory(
    directory: str,
    search_text: str,
    file_pattern: str = "*",
    case_sensitive: bool = False,
    max_results: int = 100,
) -> str:
    """Search for text across all files in a directory.

    Args:
        directory: The directory to search in.
        search_text: The text to search for.
        file_pattern: Glob pattern for files to search (default '*').
        case_sensitive: Whether the search should be case-sensitive (default False).
        max_results: Maximum number of matching lines to return (default 100).

    Returns:
        Matching lines with file paths and line numbers.
    """
    try:
        path = Path(directory).resolve()
        if not path.exists():
            return f"Error: Directory '{directory}' does not exist."
        if not path.is_dir():
            return f"Error: '{directory}' is not a directory."

        matches = []
        files_searched = 0

        for file_path in path.rglob(file_pattern):
            if not file_path.is_file():
                continue

            files_searched += 1

            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    for i, line in enumerate(f, 1):
                        if len(matches) >= max_results:
                            break

                        if case_sensitive:
                            if search_text in line:
                                matches.append(f"{file_path}:{i}: {line.rstrip()}")
                        else:
                            if search_text.lower() in line.lower():
                                matches.append(f"{file_path}:{i}: {line.rstrip()}")

                if len(matches) >= max_results:
                    break
            except (PermissionError, IsADirectoryError):
                continue

        if not matches:
            return f"No matches for '{search_text}' found in '{directory}' (searched {files_searched} files)."

        result = f"Found {len(matches)} match(es) in {files_searched} files:\n"
        result += "\n".join(matches)
        if len(matches) >= max_results:
            result += f"\n\n(Results limited to {max_results})"

        return result
    except Exception as e:
        return f"Error searching directory: {str(e)}"


@tool
def regex_search(file_path: str, pattern: str) -> str:
    """Search for a regular expression pattern in a file.

    Args:
        file_path: The path to the file to search in.
        pattern: The regular expression pattern to search for.

    Returns:
        Matching lines with line numbers.
    """
    try:
        path = Path(file_path).resolve()
        if not path.exists():
            return f"Error: File '{file_path}' does not exist."
        if not path.is_file():
            return f"Error: '{file_path}' is not a file."

        try:
            regex = re.compile(pattern)
        except re.error as e:
            return f"Error: Invalid regex pattern: {str(e)}"

        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        matches = []
        for i, line in enumerate(lines, 1):
            if regex.search(line):
                matches.append(f"Line {i}: {line.rstrip()}")

        if not matches:
            return f"No matches for pattern '{pattern}' found in '{file_path}'."

        return f"Found {len(matches)} match(es):\n" + "\n".join(matches)
    except Exception as e:
        return f"Error with regex search: {str(e)}"


# Export all search tools
search_tools = [
    search_files,
    search_in_file,
    search_in_directory,
    regex_search,
]
