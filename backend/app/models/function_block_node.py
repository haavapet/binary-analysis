class FunctionBlockNode():
    def __init__(self: "FunctionBlockNode",
                 instructions: list,
                 fb_id: int,
                 start: int,
                 end: int) -> None:
        self.instructions = instructions
        self.id = fb_id
        self.called_function_blocks = []
        self.start = start
        self.end = end
