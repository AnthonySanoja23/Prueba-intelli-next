from __future__ import annotations
from typing import List, TypeVar, Generic, Sequence

from fastapi_pagination import Params
from fastapi_pagination.api import response
from fastapi_pagination.bases import AbstractPage, AbstractParams
from pydantic import BaseModel, conint
from pydantic import BaseModel
from fastapi_pagination.bases import RawParams
from typing import TypeVar, Generic
from pydantic import BaseModel

from fastapi_pagination.bases import RawParams, AbstractParams
from fastapi import Query


T = TypeVar("T")

class Params(BaseModel, AbstractParams):
    page: int = Query(1, ge=1, description="Page number")
    items: int = Query(50, ge=1, le=100, description="Page size")
    
    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.items,
            offset=self.items * (self.page - 1),
        )
    
    
class PageCustom(AbstractPage[T], Generic[T]):
    Page: conint(ge=1)
    totalPages: conint(ge=1)
    Items: conint(ge=1)
    totalItems: conint(ge=1)
    Players: Sequence[T]
    
    
    __params_type__ = Params  # Set params related to Page

    @classmethod
    def create(
            cls,
            items: Sequence[T],
            total: int,
            params: AbstractParams,
    )-> PageCustom[T]:
            return cls(
                Page=params.page,
                totalPages=cls.totalPages,
                Items=params.items,
                totalItems =total,
                Players=items,
                )


