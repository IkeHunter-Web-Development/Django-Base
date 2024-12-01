"""
File management utilities.
"""

from pathlib import Path
from typing import Optional
import uuid

from app.settings import MEDIA_ROOT


def get_media_path(
    nested_path="",
    filename: Optional[str] = None,
    fileprefix: Optional[str] = None,
    fileext: Optional[str] = None,
    create_path=True,
):
    """
    Get full directory path for media files.

    If filename is none, and fileprefix is provided, will create a unique filename
    with the given prefix.

    Parameters
    ----------
        - nested_path (str): Directory inside media root
        - filename (str): Name of the file inside directory
        - fileprefix (str): Used to generate unique filename in absence of filename.
        - fileext (str): File extension without dot, must be provided when using prefix.
        - create_path (bool): Automatically create nested directory structure if needed.
    """

    path = Path(MEDIA_ROOT, nested_path)

    if create_path:
        path.mkdir(parents=True, exist_ok=True)

    if filename:
        path = Path(path, filename)
    elif fileprefix:
        assert (
            fileext is not None
        ), "If using a file prefix, a file extension must also be provided."
        assert not fileext.startswith("."), "File extension must not start with a dot."

        filename = f"{fileprefix}-{uuid.uuid4()}.{fileext}"
        path = Path(path, filename)

    return str(path)
