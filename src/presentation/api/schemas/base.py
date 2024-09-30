import inspect
from typing import Type, Any

from fastapi import Form
from pydantic import BaseModel, PrivateAttr
from pydantic.v1.fields import Undefined


class AsForm(BaseModel):
    @classmethod
    def as_form(cls: Type[BaseModel]):
        new_parameters = []

        for field_name, model_field in cls.model_fields.items():
            field_info = model_field
            field_type = model_field.annotation

            if model_field.default is Undefined:
                form_field = Form(...)
            else:
                form_field = Form(default=model_field.default)

            new_parameters.append(
                inspect.Parameter(
                    field_name,
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    default=form_field,
                    annotation=field_type,
                )
            )

        async def as_form_func(**data):
            return cls(**data)

        as_form_func.__signature__ = inspect.signature(as_form_func).replace(parameters=new_parameters)

        return as_form_func
