# made by me
# screw you theres magic numbers read the isc

import array
import time


def emulate(bin: bytes):
    # The length is the amount of *BYTES* (not bits or words) between the instruction and the EOL flag
    lenmap = {
        0x08: 1,  # Flip
        0x10: 3,  # Load
        0x11: 3,  # Set
        0x20: 1,  # VSR
        0x21: 4,  # VSM
        0x22: 0,  # VCR
        0x23: 0,  # VUD
        0x40: 2,  # JMP
        0x41: 4,  # JIE
        0x42: 4,  # JNE
        0x50: 3,  # MOV
        0x51: 2,  # CLN
    }

    # for non-flip ALU operations
    for i in range(0x0, 0x07):
        lenmap[i] = 2

    # for F-instructions
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
    endexec = False
    hertz = 1000
    interval = 1 / hertz
    print(f"---BEGIN EXEC {hertz}HZ---")
    while not endexec:
        start = time.time()
        match int.from_bytes(instructions[idx][:1], byteorder="big"):
            # ADD
            case 0x00:
                r1i = instructions[idx][1]
                r2i = instructions[idx][2]
                r1 = registers[r1i]
                r2 = registers[r2i]
                registers[11] = r1  # access to p1
                registers[12] = r2  # access to p2
                registers[15] = (r1 + r2) & 0xFFFF  # setting ret
                registers[r1i] = registers[15]
                print(f"@0x{idx:04x} : x{r1i}({r1}) += x{r2i}({r2})")

            # SUB
            case 0x01:
                r1i = instructions[idx][1]
                r2i = instructions[idx][2]
                r1 = registers[r1i]
                r2 = registers[r2i]
                registers[11] = r1  # access to p1
                registers[12] = r2  # access to p2
                registers[15] = r1 - r2  # setting ret
                registers[r1i] = registers[15]
                print(f"@0x{idx:04x} : x{r1i}({r1}) -= x{r2i}({r2})")

            # MUL
            case 0x02:
                r1i = instructions[idx][1]
                r2i = instructions[idx][2]
                r1 = registers[r1i]
                r2 = registers[r2i]
                registers[11] = r1  # access to p1
                registers[12] = r2  # access to p2
                registers[15] = r1 * r2  # setting ret
                registers[r1i] = registers[15]
                print(f"@0x{idx:04x} : x{r1i}({r1}) *= x{r2i}({r2})")

            # AND
            case 0x03:
                r1i = instructions[idx][1]
                r2i = instructions[idx][2]
                r1 = registers[r1i]
                r2 = registers[r2i]
                registers[11] = r1  # access to p1
                registers[12] = r2  # access to p2
                registers[15] = r1 & r2  # setting ret
                registers[r1i] = registers[15]
                print(f"@0x{idx:04x} : x{r1i}({r1}) &= x{r2i}({r2})")

            # OR
            case 0x04:
                r1i = instructions[idx][1]
                r2i = instructions[idx][2]
                r1 = registers[r1i]
                r2 = registers[r2i]
                registers[11] = r1  # access to p1
                registers[12] = r2  # access to p2
                registers[15] = r1 | r2  # setting ret
                registers[r1i] = registers[15]
                print(f"@0x{idx:04x} : x{r1i}({r1}) |= x{r2i}({r2})")

            # XOR
            case 0x05:
                r1i = instructions[idx][1]
                r2i = instructions[idx][2]
                r1 = registers[r1i]
                r2 = registers[r2i]
                registers[11] = r1  # access to p1
                registers[12] = r2  # access to p2
                registers[15] = r1 ^ r2  # setting ret
                registers[r1i] = registers[15]
                print(f"@0x{idx:04x} : x{r1i}({r1}) ^= x{r2i}({r2})")

            # LFS
            case 0x06:
                r1i = instructions[idx][1]
                r2i = instructions[idx][2]
                r1 = registers[r1i]
                r2 = registers[r2i]
                registers[11] = r1  # access to p1
                registers[12] = r2  # access to p2
                registers[15] = r1 << r2  # setting ret
                registers[r1i] = registers[15]
                print(f"@0x{idx:04x} : x{r1i}({r1}) <<= x{r2i}({r2})")

            # RFS
            case 0x07:
                r1i = instructions[idx][1]
                r2i = instructions[idx][2]
                r1 = registers[r1i]
                r2 = registers[r2i]
                registers[11] = r1  # access to p1
                registers[12] = r2  # access to p2
                registers[15] = r1 >> r2  # setting ret
                registers[r1i] = registers[15]
                print(f"@0x{idx:04x} : x{r1i}({r1}) >>= x{r2i}({r2})")

            # FLP
            case 0x08:
                r1i = instructions[idx][1]
                r1 = registers[r1i]
                registers[15] = ~r1
                registers[r1i] = registers[15]
                print(f"@0x{idx:04x} : x{r1i}({r1})~~")

            # JMP
            case 0x40:
                addr = int.from_bytes(instructions[idx][1:3], byteorder="big")
                print(f"@0x{idx:04x} : JMP 0x{addr - 1:04x}")
                idx = addr - 2

            # JIE
            case 0x41:
                addr = int.from_bytes(instructions[idx][1:3], byteorder="big")
                r1i = instructions[idx][3]
                r2i = instructions[idx][4]
                print(
                    f"@0x{idx:04x} : JIE 0x{addr - 1:04x} (IF {registers[r1i] == registers[r2i]})"
                )
                if registers[r1i] == registers[r2i]:
                    idx = addr - 2

            # JNE
            case 0x42:
                addr = int.from_bytes(instructions[idx][1:3], byteorder="big")
                r1i = instructions[idx][3]
                r2i = instructions[idx][4]
                print(
                    f"@0x{idx:04x} : JNE 0x{addr - 1:04x} (IF {registers[r1i] != registers[r2i]})"
                )
                if registers[r1i] != registers[r2i]:
                    idx = addr - 2

            # MOV
            case 0x50:
                register = instructions[idx][1]
                val = int.from_bytes(instructions[idx][2:4], byteorder="big")
                registers[register] = val
                print(f"@0x{idx:04x} : x{register} = {val}")

            # CLN
            case 0x51:
                r1i = instructions[idx][1]
                r2i = instructions[idx][2]
                r2 = registers[r2i]
                registers[r1i] = r2
                print(f"@0x{idx:04x} : x{r1i} = {r2}")

            # HLT
            case 0xFC:
                print(f"@0x{idx:04x} : HALT")
                endexec = True

            # NOP
            case 0xFD:
                print(f"@0x{idx:04x} : NOP")

            case _:
                print(f"@0x{idx:04x} : EXCEPTION, INVALID OPERATION")
                endexec = True

        print("@REGIST", registers.tolist())

        elapsed = time.time() - start
        if elapsed < interval:
            time.sleep(interval - elapsed)

        idx += 1
    print("---END EXEC---")
