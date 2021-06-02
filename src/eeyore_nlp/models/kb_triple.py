from typing import Any, Dict


class KBTriple():
    def __init__(self,
                 rel: str,
                 subj: str,
                 obj: str):
        self.__rel = rel
        self.__subj = subj
        self.__obj = obj

    @property
    def rel(self) -> str:
        return self.__rel

    @property
    def subj(self) -> str:
        return self.__subj

    @property
    def obj(self) -> str:
        return self.__obj

    @property
    def cache(self) -> Dict[str, Any]:
        return self.__dict__

    def update_cache(self, items: Dict[str, Any]):
        self.__dict__.update(items)

    def __repr__(self) -> str:
        return \
            f'KBTriple(rel="{self.rel}", subj="{self.subj}", obj="{self.obj}")'
