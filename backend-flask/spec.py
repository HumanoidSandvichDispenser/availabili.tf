import pydantic.v1
from spectree import SpecTree
from pydantic.alias_generators import to_camel
from spectree.plugins.flask_plugin import FlaskPlugin

# Naming convention:
# https://github.com/0b01001001/spectree/issues/300
# https://github.com/0b01001001/spectree/pull/302
def naming_strategy(model):
    return model.__name__

# https://github.com/0b01001001/spectree/issues/304#issuecomment-1519961668
def nested_naming_strategy(_, child):
    return child

spec = SpecTree(
    "flask",
    annotations=True,
    naming_strategy=naming_strategy,
    nested_naming_strategy=nested_naming_strategy
)

class BaseModel(pydantic.v1.BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True

