# Compiler for Om Mallick Language(.oml)

# Video Resources used to build this Compiler:
# https://youtu.be/GsCWivTeFpY?si=hOEN7wlnLP_9o7nz
# https://youtube.com/playlist?list=PLRAdsfhKI4OWNOSfS7EUu5GRAVmze1t2y&si=EXtVh60gwWM1n2BK
# https://youtube.com/playlist?list=PLUDlas_Zy_qC7c5tCgTMYq2idyyT241qs&si=6pg7TCfs5TkscMia

# Windows 11 64 Bit
# x86-64 Architecture & Instruction Set
# Intel Syntax
# Microsoft x64 Calling Convention

# Add Error Handling Functionality In Synatax Analysis And Other Stages

# Importing Modules
import sys
import os

# Read Arguments
program_filepath = sys.argv[1]
print("[CMD] Parsing")

# Parsing - Tokenize Program

# List For Lines In A Program
program_lines = []
# Read File Lines
with open(program_filepath,"r") as program_file:
    # Strip Lines Of Whitespaces and Convert Into A List
    program_lines = [line.strip() for line in program_file.readlines()]
    
# List For Tokens In A Program
program = []
for line in program_lines:
    # Split Lines Into Tokens
    parts = line.split(" ")
    opcode = parts[0]

    # Check For Empty Line
    if opcode == "":
        continue

    # Store Opcode Token
    program.append(opcode)

    # Handle Each Opcode
    if opcode == "PUSH":
        # Expecting A Number
        try:
            number= int(parts[1])
        # Error Handling
        except:
            # Add Error Handling
            pass
        # Append Into List Of Tokens
        program.append(number)
    elif opcode == "PRINT":
        # Parse String Literal
        # Join String Literal Which Is Split Up And Remove The Quotation Marks And Append Into List Of Tokes
        string_literal=' '.join(parts[1:])[1:-1]
        program.append(string_literal)
    elif opcode =="JUMP.EQ.0":
        # Read Label
        label = parts[1]
        # Append Into List Of Tokens
        program.append(label)
    elif opcode == "JUMP.GT.0": 
        # Read Label
        label= parts[1]
        # Append Into List Of Tokens
        program.append(label)
    # Error Handling
    else:
        # Add Error Handling
        pass


# Book Keep String Literals - For Printing
string_literals = []
for ip in range(len(program)):
	if program[ip] == "PRINT":
		string_literal = program[ip+1]
		program[ip+1] =  len(string_literals)
		string_literals.append(string_literal)


# Create An Assembly Program

# File Path For Assembly Program
asm_filepath = program_filepath[:-4] +".asm"
# File For Assembly Program
out = open(asm_filepath, "w")

# Instructions For Assembler (NASM)
# 64 Bit Program
# Relative Addressing
out.write("""; -- header --
bits 64
default rel
""")

# Computer Program's Memory
# Stack
# Heap
# BSS (Uninitialised Data)
# Data (Initialised Data)
# Text (Assembly Logic)

out.write("""; -- variables --
section .bss
read_number resq 1 ; 64-bits integer = 8 bytes
""")

out.write("""; -- constants --
section .data
read_format db "%d", 0 ; the format string for scanf
""")
for i,string_literal in enumerate(string_literals):
    out.write(f"string_literal_{i} db \"{string_literal}\", 0\n")

# Start Program In Main Function
# Exit Function To Properly Exit The Assembly Program
# Printf And Scanf for I/O (GCC as Linker)
# Main Is Emtry Point To Program
# Shadow Space After Main Label (Considering Microsoft Calling Convention)
# Push Base Pointer To Stack
# Set Base Pointer To Current Pointer
# Subtract 32 From The Stack Pointer
out.write("""; -- Entry point --
section .text
global main
extern ExitProcess
extern printf
extern scanf
          
main:
\tPUSH rbp
\tMOV rbp,rsp
\tSUB rsp,32
""")


# Instruction Pointer
ip = 0
# Loop To Parse Through The Whole Program
while ip<len(program):
    opcode = program[ip]
    ip += 1
    
    # Opcode Is Label
    if opcode.endswith(":"):
        # Label In Assembly
        out.write(f"; Label ---\n")
        out.write(f"{opcode}\n")
    # Opcode Is Push
    elif opcode == "PUSH":
        # Retrive Number From List Of Tokens And Increment Instruction Pointer
        number = program[ip]
        ip += 1
        # Push Number In Assembly
        out.write(f"; -- PUSH ---\n")
        out.write(f"\tPUSH {number}\n")
    # Opcode Is Pop
    elif opcode == "POP":
        # Pop In Assembly
        out.write(f"; -- POP ---\n")
        out.write(f"\tPOP\n")
    # Opcode Is Add
    elif opcode == "ADD":
        # Add In Assembly
        out.write(f"; -- ADD ---\n")
        out.write(f"\tPOP rax\n")
        out.write(f"\tADD qword [rsp], rax\n")
        # out.write(f"\tPOP rbx\n")
        # out.write(f"\tADD rbx, rax\n")
        # out.write(f"\tPUSH rbx\n")
    # Opcode Is Sub
    elif opcode == "SUB":
        # Sub In Assembly
        out.write(f"; -- SUB---\n")
        out.write(f"\tPOP rax\n")
        out.write(f"\tSUB qword [rsp], rax\n")
        # out.write(f"\tPOP rbx\n")
        # out.write(f"\tSUB rbx, rax\n")
        # out.write(f"\tPUSH rbx\n")
    # Opcode Is Print
    elif opcode == "PRINT":
        # Print In Assembly
        string_literal_index = program[ip]
        ip +=1
        out.write(f"; -- PRINT ---\n")
        out.write(f"\tLEA rcx, string_literal_{string_literal_index}\n")
        out.write(f"\tXOR eax, eax\n")
        out.write(f"\tCALL printf\n")
    # Opcode Is Read
    elif opcode == "READ":
        # Read In Assembly
        out.write(f"; -- READ ---\n")
        out.write(f"\tLEA rcx, read_format\n")
        out.write(f"\tLEA rdx, read_format\n")
        out.write(f"\tXOR eax, eax\n")
        out.write(f"\tCALL scanf\n")
        out.write(f"\tPUSH qword [read_number]\n")
    # Opcode Is Jump.Eq.0
    elif opcode == "JUMP.EQ.0":
        # Jump.Eq.0 In Assembly
        label = program[ip]
        ip += 1

        out.write(f"; -- JUMP.EQ.0 ---\n")
        # Compare The 8 Bytes At The Top Of The Stack With 0
        out.write(f"\tCMP qword [rsp], 0\n")
        # Jump When Equal To, To The Given Label
        out.write(f"\tJE {label}\n")
    # Opcode Is Jump.Gt.0
    elif opcode == "JUMP.GT.0":
        # Jump.Gt.0 In Assembly
        label = program[ip]
        ip += 1

        out.write(f"; -- JUMP.GT.0 ---\n")
        # Compare The 8 Bytes At The Top Of The Stack With 0
        out.write(f"\tCMP qword [rsp], 0\n")
        # Jump When Greater Than, To The Given Label
        out.write(f"\tJG {label}\n")  
    # Opcode Is Halt
    elif opcode == "HALT":
        # Halt In Assembly
        out.write(f"; -- HALT ---\n")
        # Jump To Exit Label
        out.write(f"\tJMP EXIT_LABEL\n") 
    # Error Handling
    else:
        # Add Error Handling
        pass

# Exit Label
out.write("EXIT_LABEL:\n")
# Set Rax Register To 0 (Part Of Microsoft Calling Convention)
out.write(f"\tXOR rax, rax\n")
# Call ExitProcess Windows API Version
out.write(f"\tCALL ExitProcess\n")
# Close The File
out.close()

# Assemble (NASM)
print("[CMD] Assembling")
os.system(f"nasm -f elf64 {asm_filepath} -o {asm_filepath[:-3]+'o'}")

# Link (GCC)
print("[CMD] Linking")
os.system(f"gcc -o {asm_filepath[:-4] + '.exe'} {asm_filepath[:-3]+'o'}")

# Running The Program
print("[CMD] Running")
os.system(f"./{asm_filepath[:-4] + '.exe'}")