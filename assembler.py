import struct

tape = b''
with open('test.s16', 'r') as f:
    data = f.read()

ins = [line.split() for line in data.strip().splitlines()]
print(ins)

def parseregister(reg) -> int:
    if reg != "x0" and reg.startswith("x"):
        stripped = reg.removeprefix("x")
        return int(stripped)
    elif reg == "p1":
        return 10
    elif reg == "p2":
        return 11
    elif reg == "car":
        return 12
    elif reg == "int":
        return 13
    elif reg == "ins":
        return 14
    elif reg == "ret":
        return 15
    else:
        raise ValueError(f"Register {reg} does not exist")


def parseline(ls) -> bytes:
    match ls[0]:        
        # Zero Range
        case 'ADD':
            lns = [0x00]
            lns.append(parseregister(ls[1]))
            lns.append(parseregister(ls[2]))
            lns.append(255)
            return struct.pack(">BBBB", lns[0], lns[1], lns[2], lns[3])

        case 'SUB':
            lns = [0x01]
            lns.append(parseregister(ls[1]))
            lns.append(parseregister(ls[2]))
            lns.append(255)
            return struct.pack(">BBBB", lns[0], lns[1], lns[2], lns[3])

        case 'MUL':
            lns = [0x02]
            lns.append(parseregister(ls[1]))
            lns.append(parseregister(ls[2]))
            lns.append(255)
            return struct.pack(">BBBB", lns[0], lns[1], lns[2], lns[3])
  
        case 'AND':
            lns = [0x03]
            lns.append(parseregister(ls[1]))
            lns.append(parseregister(ls[2]))
            lns.append(255)
            return struct.pack(">BBBB", lns[0], lns[1], lns[2], lns[3])  
  
        case 'OR':
            lns = [0x04]
            lns.append(parseregister(ls[1]))
            lns.append(parseregister(ls[2]))
            lns.append(255)
            return struct.pack(">BBBB", lns[0], lns[1], lns[2], lns[3])  
  
        case 'XOR':
            lns = [0x05]
            lns.append(parseregister(ls[1]))
            lns.append(parseregister(ls[2]))
            lns.append(255)
            return struct.pack(">BBBB", lns[0], lns[1], lns[2], lns[3])  
        
        case 'LFS':
            lns = [0x06]
            lns.append(parseregister(ls[1]))
            lns.append(parseregister(ls[2]))
            lns.append(255)
            return struct.pack(">BBBB", lns[0], lns[1], lns[2], lns[3])
            
        case 'RFS':
            lns = [0x07]
            lns.append(parseregister(ls[1]))
            lns.append(parseregister(ls[2]))
            lns.append(255)
            return struct.pack(">BBBB", lns[0], lns[1], lns[2], lns[3])
            
        case 'FLP':
            lns = [0x08]
            lns.append(parseregister(ls[1]))
            lns.append(255)
            return struct.pack(">BBBB", lns[0], lns[1], lns[2])
            
        # One Range
        case 'LOAD':
            lns = [0x10]
            lns.append(parseregister(ls[1]))
            lns.append(int(ls[2], 16))
            lns.append(255)
            return struct.pack(">BBHB", lns[0], lns[1], lns[2], lns[3])
            
        case 'SET':
            lns = [0x11]
            lns.append(parseregister(ls[1]))
            lns.append(int(ls[2], 16))
            lns.append(255)
            return struct.pack(">BBHB", lns[0], lns[1], lns[2], lns[3])
            
        # Two Range
        case 'VSR':
            lns = [0x20]
            lns.append(parseregister(ls[1]))
            lns.append(255)
            return struct.pack(">BBB", lns[0], lns[1], lns[2])
            
        case 'VSM':
            lns = [0x20]
            lns.append(int(ls[1], 16))
            lns.append(int(ls[2], 16))
            lns.append(255)
            return struct.pack(">BHHB", lns[0], lns[1], lns[2], lns[3])
            
        case 'VUD':
            return struct.pack(">BB", 0x23, 255)
            
        # Four Range
        case 'JMP':
            lns = [0x40]
            lns.append(int(ls[1], 16))
            lns.append(255)
            return struct.pack(">BHB", lns[0], lns[1], lns[2])
        
        # Five Range
        case 'MOV':
            lns = [0x50]
            lns.append(parseregister(ls[1]))
            lns.append(int(ls[2], 16))
            lns.append(255)
            return struct.pack(">BBHB", lns[0], lns[1], lns[2], lns[3])
        
        case 'CLN':
            lns = [0x51]
            lns.append(parseregister(ls[1]))
            lns.append(parseregister(ls[2]))
            lns.append(255)
            return struct.pack(">BBHB", lns[0], lns[1], lns[2], lns[3])
        
        # Fth Range
        case 'HLT':
            return struct.pack(">BB", 0xFC, 255)
            
        case 'NOP':
            return struct.pack(">BB", 0xFD, 255)
        
    raise ValueError(f"Invalid instruction {ls[0]}")

for line in ins:
    tape += parseline(line)

print(tape)

with open("out.bin", 'wb') as f:
    f.write(tape)
