# Chip instructions + general info

### Registers:
- x0 : Constant Zero
- x1 through x9: General Purpose
- p1/p2: ALU reserved registers (always stream output to ALU, direct wire)
- car: Carry boolean (0x0000 false, 0x0001 true)
- int: Interrupt ID
- ins: Instruction Index 
- ret: ALU Accumulator Register

ONLY x01-x09 CAN BE EDITED DIRECTLY

### Opcode List
Note: NIEE means it is not implemented in the editor
```
Opcodes         ASM   Function  
0x00(reg0)(reg1): ADD : Add reg1 to reg0 (reg0 += reg1)
0x01(reg0)(reg1): SUB : Subtract reg1 from reg0 (reg0 -= reg1)
0x02(reg0)(reg1): MUL : Multiply reg1 to reg0 (reg0 *= reg1)
0x03(reg0)(reg1): AND : Bitwise AND (reg0 = reg0 AND reg1)
0x04(reg0)(reg1): OR  : Bitwise OR (reg0 = reg0 OR reg1)
0x05(reg0)(reg1): XOR : Bitwise XOR (reg0 = reg0 XOR reg1)
0x06(reg0)(reg1): LFS : Bitwise LEFT SHIFT (reg0 = reg0 << reg1)
0x07(reg0)(reg1): RFS : Bitwise RIGHT SHIFT (reg0 = reg0 >> reg1)
0x08(reg0)      : FLP : Flip binary data in a register (1010 -> 0101)

0x10(reg)(addr) : LOAD: Load a 16 bit word to memory address ADDR
0x11(reg)(addr) : SET : Save a 16 bit word to memory address ADDR

(NIEE)
0x20(reg)       : VSR : Send register to end of video buffer
0x21(sadr)(eadr): VSM : Send memory range startaddr -> endaddr to the vbuf
0x22            : VCR : Video Clear Signal (clear graphics buffer)
0x23            : VUD : Video Push Buffer

(NIEE)
0x30            : EKI : Enable KINP
0x31            : DKI : Disable KINP

0x40(addr)      : JMP : Jump to address
0x41(1)(2)(addr): JIE : Jump to addr if register 1 and 2 are equal
0x42(1)(2)(addr): JNE : Jump to addr if register 1 and 2 are not equal
       (1)(addr): JIZ : Jump to addr if register 1 is zero (macro in comp)
          (addr): JIC : Jump to addr if carry is true

0x50(reg)(val)  : MOV : Move a value to a register (ex: MOV x01 i1000)
0x51(reg0)(reg1): CLN : Clone a register (reg0 = reg1)

(0x6-0x9 range reserved for extensions)

(NIEE)
0xA0(reg)       : ERP : Push register to EXPANSION-OUT
0xA1(addr)      : EMP : Push memory addr to EXP-OUT
0xA2(reg)       : EPR : Push EXP-IN to reg
0xA3(addr)      : EPM : Push EXP-IN to memory address

0xFC            : HLT : Halt execution until restart
0xFD            : NOP : No Operation
0xFF            : EOL : End of line (auto entered at comptime)
```
Card Opcode Header Chips
0x0 : ALU
0x1 : Memory Module
0x2: Graphics Manager
0x3: Input Manager
0x4: Register manage
0xA: Expansion Manager
0xF: Misc.

CPU Specs:
1 Khz main clock
16 Bit word size (2 bytes/word)