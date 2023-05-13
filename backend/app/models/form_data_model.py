from fastapi import UploadFile
from pydantic import Field

from ..utils.form_base_model import FormBaseModel


class FormDataModel(FormBaseModel):
    """ Form input for the API

    Attributes:
        instr_len (int): (class attribute) Length of instruction in bits
        ret_len (int): (class attribute) Length of instruction ret opcode in bits
        call_len (int): (class attribute) Length of instruction call opcode in bits
        file_offset (int): (class attribute) Byte position of code section start in binary
        file_offset_end (int): (class attribute) Byte position of code section end in binary
        pc_offset (int): (class attribute) position of first instruction in virtual memory
        pc_inc (int): (class attribute) How much pc increases between each instruction
        endiannes (str): (class attribute) "big" or "little"
        nr_cand (int): (class attribute) How many graph candidates to return
        call_search_range (list): (class attribute) (x, y) -> call is known
                                                    to be between the x and y most
                                                    popular instructions
        ret_search_range (list): (class attribute) (x, y) -> ret is known
                                                    to be between the x and y most
                                                    popular instructions
        ret_func_dist (int): (class attribute) Distance from function prologue to prvious ret
        unknownCodeEntry (bool): (class attribute) Search the binary for the most optimal
                                                   fileOffset and fileOffsetEnd,
                                                   drastically increases runtime
        includeInstructions (bool): (class attribute) Include instructions in result object.
                                                      Recommended False for big binaries
                                                      if rendering graph
        isRelativeAddressing (bool): (class attribute) Relative or absolute addressing
                                                       for call operands
        file (UploadFile): (class attribute) Binary file to be analysed
        binary_data (bytes): (class attribute) Bytes of code section of binary file
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
    unknown_code_entry: bool = Field(alias="unknownCodeEntry")
    include_instruction: bool = Field(alias="includeInstructions")
    is_relative_addressing: bool = Field(alias="isRelativeAddressing")
    file: UploadFile = Field(alias="file")


    @property
    def binary_data(self) -> bytes:
        return self.file.file.read()
