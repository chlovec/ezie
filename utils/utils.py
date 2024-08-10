from dataclasses import dataclass
from typing import List


def remove_last_comma(s: str) -> str:
    if s.endswith(','):
        return s[:-1]
    return s


@dataclass
class FileData:
    file_path: str
    file_content: List[str]
