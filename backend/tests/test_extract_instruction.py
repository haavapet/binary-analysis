from ..app.extract_instructions import extract_instruction


def test_extract_instruction() -> None:
    int_list = [0x37, 0x21, 0x16, 0x22]

    instructions = extract_instruction(bytes(int_list), "little", 32)
    assert instructions == [0x22162137]

    instructions = extract_instruction(bytes(int_list), "big", 32)
    assert instructions == [0x37211622]

    instructions = extract_instruction(bytes(int_list), "little", 16)
    assert instructions == [0x2137, 0x2216]

    instructions = extract_instruction(bytes(int_list), "big", 16)
    assert instructions == [0x3721, 0x1622]

    instructions = extract_instruction(bytes(int_list), "big", 8)
    assert instructions == [0x37, 0x21, 0x16, 0x22]

    instructions = extract_instruction(bytes(int_list), "big", 4)
    assert instructions == [0x3, 0x7, 0x2, 0x1, 0x1, 0x6, 0x2, 0x2]
