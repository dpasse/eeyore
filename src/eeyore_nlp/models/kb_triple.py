from typing import Optional


class KBTriple():
    def __init__(self,
                 rel: str,
                 subj: str,
                 obj: str,
                 subj_entity: Optional[str] = None,
                 obj_entity: Optional[str] = None,
                 rel_entity: Optional[str] = None):
        self.__rel = rel
        self.__subj = subj
        self.__obj = obj
        self.__subj_entity = subj_entity
        self.__obj_entity = obj_entity
        self.__rel_entity = rel_entity

    @property
    def rel(self) -> str:
        return self.__rel

    @property
    def rel_entity(self) -> str:
        return self.__rel_entity

    @property
    def subj(self) -> str:
        return self.__subj

    @property
    def subj_entity(self) -> Optional[str]:
        return self.__subj_entity

    @property
    def obj(self) -> str:
        return self.__obj

    @property
    def obj_entity(self) -> Optional[str]:
        return self.__obj_entity

    def __repr__(self) -> str:
        return \
            f'KBTriple(rel="{self.rel}", subj="{self.subj}", obj="{self.obj}")'
