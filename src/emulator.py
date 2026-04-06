import array
import asyncio
import functools

print = functools.partial(print, flush=True)


def emulate(bin: bytes, hertz: int = 1000):
    async def run_emu():
        nonlocal bin
        lenmap = {
            0x08: 1,
            0x10: 3,
            0x11: 3,
            0x20: 1,
            0x21: 4,
            0x22: 0,
            0x23: 0,
            0x40: 2,
            0x41: 4,
            0x42: 4,
            0x50: 3,
            0x51: 2,
        }

        for i in range(0x0, 0x07):
            lenmap[i] = 2

        for i in range(0xFC, 256):
            lenmap[i] = 0

        instructions = []
        registers = array.array("H", [0] * 16)
        registers[9] = 1
        ram = array.array("H", [0] * 32768)
        vram = array.array("B", [0] * 64)

        while len(bin) > 0:
            i = bin[0]
            length = lenmap[i] + 2
            instructions.append(bin[:length])
            bin = bin[length:]

        idx = 0
        iters = 0
        endexec = False
        print(f"---BEGIN EXEC {hertz}HZ---")

        while not endexec and idx < len(instructions):
            op_code = int.from_bytes(instructions[idx][:1], byteorder="big")

            match op_code:
                case 0x00:
                    r1i, r2i = instructions[idx][1], instructions[idx][2]
                    r1, r2 = registers[r1i], registers[r2i]
                    registers[11], registers[12] = r1, r2
                    registers[15] = (r1 + r2) & 0xFFFF
                    registers[r1i] = registers[15]
                    print(f"@0x{idx:04x} : x{r1i}({r1}) += x{r2i}({r2})")

                case 0x01:
                    r1i, r2i = instructions[idx][1], instructions[idx][2]
                    r1, r2 = registers[r1i], registers[r2i]
                    registers[11], registers[12] = r1, r2
                    registers[15] = (r1 - r2) & 0xFFFF
                    registers[r1i] = registers[15]
                    print(f"@0x{idx:04x} : x{r1i}({r1}) -= x{r2i}({r2})")

                case 0x02:
                    r1i, r2i = instructions[idx][1], instructions[idx][2]
                    r1, r2 = registers[r1i], registers[r2i]
                    registers[11], registers[12] = r1, r2
                    registers[15] = (r1 * r2) & 0xFFFF
                    registers[r1i] = registers[15]
                    print(f"@0x{idx:04x} : x{r1i}({r1}) *= x{r2i}({r2})")

                case 0x03:
                    r1i, r2i = instructions[idx][1], instructions[idx][2]
                    r1, r2 = registers[r1i], registers[r2i]
                    registers[11], registers[12] = r1, r2
                    registers[15] = r1 & r2
                    registers[r1i] = registers[15]
                    print(f"@0x{idx:04x} : x{r1i}({r1}) &= x{r2i}({r2})")

                case 0x04:
                    r1i, r2i = instructions[idx][1], instructions[idx][2]
                    r1, r2 = registers[r1i], registers[r2i]
                    registers[11], registers[12] = r1, r2
                    registers[15] = r1 | r2
                    registers[r1i] = registers[15]
                    print(f"@0x{idx:04x} : x{r1i}({r1}) |= x{r2i}({r2})")

                case 0x05:
                    r1i, r2i = instructions[idx][1], instructions[idx][2]
                    r1, r2 = registers[r1i], registers[r2i]
                    registers[11], registers[12] = r1, r2
                    registers[15] = r1 ^ r2
                    registers[r1i] = registers[15]
                    print(f"@0x{idx:04x} : x{r1i}({r1}) ^= x{r2i}({r2})")

                case 0x06:
                    r1i, r2i = instructions[idx][1], instructions[idx][2]
                    r1, r2 = registers[r1i], registers[r2i]
                    registers[11], registers[12] = r1, r2
                    registers[15] = (r1 << r2) & 0xFFFF
                    registers[r1i] = registers[15]
                    print(f"@0x{idx:04x} : x{r1i}({r1}) <<= x{r2i}({r2})")

                case 0x07:
                    r1i, r2i = instructions[idx][1], instructions[idx][2]
                    r1, r2 = registers[r1i], registers[r2i]
                    registers[11], registers[12] = r1, r2
                    registers[15] = r1 >> r2
                    registers[r1i] = registers[15]
                    print(f"@0x{idx:04x} : x{r1i}({r1}) >>= x{r2i}({r2})")

                case 0x08:
                    r1i = instructions[idx][1]
                    r1 = registers[r1i]
                    registers[15] = (~r1) & 0xFFFF
                    registers[r1i] = registers[15]
                    print(f"@0x{idx:04x} : x{r1i}({r1})~~")

                case 0x40:
                    addr = int.from_bytes(instructions[idx][1:3], byteorder="big")
                    print(f"@0x{idx:04x} : JMP 0x{addr - 1:04x}")
                    idx = addr - 2

                case 0x41:
                    addr = int.from_bytes(instructions[idx][1:3], byteorder="big")
                    r1i = instructions[idx][3]
                    r2i = instructions[idx][4]
                    print(
                        f"@0x{idx:04x} : JIE 0x{addr - 1:04x} (IF {registers[r1i] == registers[r2i]})"
                    )
                    if registers[r1i] == registers[r2i]:
                        idx = addr - 2

                case 0x42:
                    addr = int.from_bytes(instructions[idx][1:3], byteorder="big")
                    r1i = instructions[idx][3]
                    r2i = instructions[idx][4]
                    print(
                        f"@0x{idx:04x} : JNE 0x{addr - 1:04x} (IF {registers[r1i] != registers[r2i]})"
                    )
                    if registers[r1i] != registers[r2i]:
                        idx = addr - 2

                case 0x50:
                    register = instructions[idx][1]
                    val = int.from_bytes(instructions[idx][2:4], byteorder="big")
                    registers[register] = val
                    print(f"@0x{idx:04x} : x{register} = {val}")

                case 0x51:
                    r1i = instructions[idx][1]
                    r2i = instructions[idx][2]
                    r2 = registers[r2i]
                    registers[r1i] = r2
                    print(f"@0x{idx:04x} : x{r1i} = {r2}")

                case 0xFC:
                    print(f"@0x{idx:04x} : HALT")
                    endexec = True

                case 0xFD:
                    print(f"@0x{idx:04x} : NOP")

                case _:
                    print(f"@0x{idx:04x} : EXCEPTION, INVALID OPERATION")
                    endexec = True

            print("@REGIST", registers.tolist())

            iters += 1
            idx += 1

            if iters % 5 == 0:
                await asyncio.sleep(0.1)

        print(f"---END EXEC {iters} CYCLES---")

    asyncio.create_task(run_emu())


if __name__ == "__main__":
    with open("out.bin", "rb") as f:
        data = f.read()
        emulate(data, 1000)
