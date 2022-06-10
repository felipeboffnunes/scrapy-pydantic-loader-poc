from copy import deepcopy
from typing import List, Dict, Type
from typing import Optional

from itemloaders import ItemLoader
from itemloaders.processors import TakeFirst, Compose, MapCompose, Identity
from pydantic import BaseModel
from pydantic.main import ModelMetaclass
from scrapy import Field


class AllOptional(ModelMetaclass):
    def __new__(mcs, name, bases, namespaces, **kwargs):
        annotations = namespaces.get("__annotations__", {})
        for base in bases:
            annotations.update(base.__annotations__)

        _annotations = deepcopy(annotations)
        for field in annotations:
            if not field.startswith("__"):
                if field.endswith("_"):
                    _annotations[field[:-1]] = _annotations.pop(field)
                else:
                    _annotations[field] = Optional[_annotations[field]]
        namespaces["__annotations__"] = _annotations
        return super().__new__(mcs, name, bases, namespaces, **kwargs)


class BaseItem(BaseModel, metaclass=AllOptional):

    class Config:
        @staticmethod
        def schema_extra(schema: Dict, model: Type['BaseModel']) -> None:
            if issubclass(model, BaseModel):
                return
            schema = model.schema_json()

    # def __new__(cls, *args, **kwargs):
    #     # Change type of all fields to Field()
    #     # This is needed because otherwise the fields are not loaded
    #     # correctly by ItemLoader
    #     for field in cls.__annotations__:
    #         if not field.startswith("__"):
    #             cls.__annotations__[field] = Field()


class Tag(BaseItem):
    idx: int
    tag: str


class Quote(BaseItem):
    idx_: str
    quote: str
    author: str
    author_url: str
    tags: List[Tag]


    # @validator("author")
    # def author_must_start_with_a(cls, value):
    #     if not value.startswith("A") and not value.startswith("a"):
    #         raise ValueError("must starts with 'A' letter")
    #     return value
    #
    # @validator("tags")
    # def only_two_tags_allowed(cls, value):
    #     if len(value) > 2:
    #         raise ValueError("only two tags allowed")
    #     return value


class QuoteLoader(ItemLoader):
    default_output_processor = TakeFirst()
    idx_out = Compose(TakeFirst(), lambda x: "Tony Works")
    tags_out = Identity()

    def load_item(self):
        return Quote(**super().load_item())


print(Quote.schema_json(indent=2))