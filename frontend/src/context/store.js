import React, { createContext, useState } from "react";

const initialState = {
  page: 0,
  toastMessage: "",
  graphData: null,
  formValidated: false,
  /*formData: { TODO CHANGE TO THIS
    file: null,
    instructionLength: null,
    endiannes: "big",
    retOpcodeLength: null,
    callOpcodeLength: null,
    fileOffset: null,
    fileOffsetEnd: null,
    pcOffset: null,
    pcIncPerInstr: null,
    callCandidateRange: [null, null],
    retCandidateRange: [null, null],
    returnToFunctionPrologueDistance: null,
    nrCandidates: null,
  },*/
  formData: {
    file: null,
    instructionLength: 16,
    endiannes: "big",
    retOpcodeLength: 16,
    callOpcodeLength: 4,
    fileOffset: 0,
    fileOffsetEnd: 0x430,
    pcOffset: 0x200,
    pcIncPerInstr: 2,
    callCandidateRange: [3, 7],
    retCandidateRange: [0, 10],
    returnToFunctionPrologueDistance: 4,
    nrCandidates: 4,
  },
};

export const Context = createContext(null);

export const Store = ({ children }) => {
  const [state, setState] = useState(initialState);
  return <Context.Provider value={[state, setState]}>{children}</Context.Provider>;
};
