import React, { createContext, useState } from "react";

const initialState = {
  page: 0,
  toastMessage: "",
  graphData: null,
  formValidated: false,
  formData: {
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
    unknownCodeEntry: false,
  },
};

export const Context = createContext(null);

export const Store = ({ children }) => {
  const [state, setState] = useState(initialState);
  return <Context.Provider value={[state, setState]}>{children}</Context.Provider>;
};
