import inspect

from fastapi import Form
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ValidationError
from pydantic.fields import ModelField

"""
Hacky solution until Pydantic supports Form(...) in its models, ref:
https://github.com/tiangolo/fastapi/issues/5588

Code from
https://github.com/tiangolo/fastapi/discussions/8971#discussioncomment-5155213

Wanted this to abstract away all the data posted to the API in a class, to reduce code clutter

If one decides to do it the normal way, one can remove this file, and the form_data_model.py file
But have to live with a really long function signature,
and no aliasing of variable (they are camelcased and long)
I felt this solution was cleaner overall

@app.post("/api", response_model=ResponseModel)
async def root(
    file: UploadFile = File(...),
    InstructionLength: int = Form(...)
    retOpcodeLength: int = Form(...)
    ...
    ...
    ,):

"""


class FormBaseModel(BaseModel):
    def __init_subclass__(cls, *args: list, **kwargs: dict) -> None:
        new_params = []

        for _, model_field in cls.__fields__.items():
            model_field: ModelField  # type: ignore
            new_params.append(
                inspect.Parameter(
                    model_field.alias,
                    inspect.Parameter.POSITIONAL_ONLY,
                    default=Form(...),
                    annotation=model_field.outer_type_,
                ),
            )
        async def _as_form(**data: list) -> "FormBaseModel":
            try:
                return cls(**data)
            except ValidationError as e:
                raise RequestValidationError(e.raw_errors)

        sig = inspect.signature(_as_form)
        sig = sig.replace(parameters=new_params)
        _as_form.__signature__ = sig  # type: ignore
        setattr(cls, "as_form", _as_form)

    @staticmethod
    def as_form(parameters: list = []) -> "FormBaseModel":
        raise NotImplementedError
