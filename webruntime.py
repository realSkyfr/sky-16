import functools

import assembler
import emulator

print = functools.partial(print, flush=True)


def exec():
    with open("code.s16", "r") as f:
        code = f.read()
    asm = assembler.assemble(code)
    emulator.emulate(asm, 1000)


if __name__ == "__main__":
    exec()
