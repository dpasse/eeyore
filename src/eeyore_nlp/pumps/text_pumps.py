import os
from typing import Generator, List, Optional
import requests
from .abs import AbsTextPump


class FilePump(AbsTextPump):
    def __init__(self, file_paths: List[str]):
        if file_paths is None:
            raise ValueError()

        self.__file_paths = file_paths

    def execute(self) -> Generator[str, None, None]:
        for path in self.__file_paths:
            with open(path, 'r') as data:
                text = data.read()

            yield text


class DirectoryPump(FilePump):
    def __init__(self,
                 directory_paths: List[str],
                 valid_endings: Optional[List[str]] = None):
        if directory_paths is None:
            raise ValueError()

        file_paths = []
        valid_endings = valid_endings \
            if valid_endings is not None else []

        for path in directory_paths:
            file_paths.extend(
                [
                    os.path.join(path, file)
                    for file in os.listdir(path)
                    if os.path.splitext(file)[-1] in valid_endings
                ]
            )

        super().__init__(file_paths)


class WebPump(AbsTextPump):
    def __init__(self, urls: List[str]):
        if urls is None:
            raise ValueError()

        self.__urls = urls

    def execute(self) -> Generator[str, None, None]:
        for url in self.__urls:
            response = requests.get(url)

            assert response.status_code == 200
            yield response.text
