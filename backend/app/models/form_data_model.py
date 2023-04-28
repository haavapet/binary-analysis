from fastapi import UploadFile
from pydantic import Field

from ..utils.form_base_model import FormBaseModel


class FormDataModel(FormBaseModel):
    """ Form input for the API

    Attributes:
        instr_len (int): (class attribute) Length of instruction in bits
        instance_attribute (str): The instance attribute
    """
    instr_len: int = Field(alias="instructionLength")
    ret_len: int = Field(alias="retOpcodeLength")
    call_len: int = Field(alias="callOpcodeLength")
    file_offset: int = Field(alias="fileOffset")
    file_offset_end: int = Field(alias="fileOffsetEnd")
    pc_offset: int = Field(alias="pcOffset")
    pc_inc: int = Field(alias="pcIncPerInstr")
    endiannes: str = Field(alias="endiannes")
    nr_cand: int = Field(alias="nrCandidates")
    call_search_range: list[int] = Field(alias="callCandidateRange")
    ret_search_range: list[int] = Field(alias="retCandidateRange")
    ret_func_dist: int = Field(alias="returnToFunctionPrologueDistance")
    file: UploadFile = Field(alias="file")


    @property
    def binary_data(self) -> bytes:
        return self.file.file.read()[self.file_offset:self.file_offset_end]
