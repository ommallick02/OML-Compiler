# OML Compiler

A small stack-based compiler written in Python for **OML** (Om Mallick Language), a toy programming language of my own design. `Compiler.py` takes a `.oml` source file, tokenizes it, emits x86-64 NASM assembly, and drives NASM + GCC to assemble/link it into a runnable executable.

This project aims to develop a compiler for a simple programming language, providing hands-on experience in understanding the compilation process, from parsing code to generating executable files. It was a learning project to understand what a compiler actually does end to end, rather than a production-grade or fully error-handled tool. It's not great, but it works for the sample programs it was built and tested against.

## How it works

The compiler is developed in Python and involves four stages:

1. **Tokenization** — the input code is parsed into a list of tokens, identifying labels, instructions, numbers, strings, and whitespace.
2. **Assembly generation** — the list of tokens is converted into x86-64 assembly (Intel syntax), defining the necessary sections and directives and handling conditional jumps and string literals, following the Windows 11 platform.
3. **Assembling** — the generated assembly file is assembled into an object file using NASM.
4. **Linking** — the object file is linked using GCC, pulling in the necessary libraries, to produce a runnable executable.

## Implementation details

- The compiler is implemented in Python, targeting a 64-bit Windows 11 machine with an Intel CPU.
- External functions from the C standard library (e.g., `printf`, `scanf`) and the Windows API (`ExitProcess`) are utilized.
- String literals are handled by creating constants in the data section.
- User input is facilitated using the `scanf` function.
- The compilation process involves parsing, code generation, assembly, and linking.

## Language

OML programs are a flat list of instructions, one per line. The language is stack-based: most instructions push to or pop from an implicit stack.

| Instruction | Description |
|---|---|
| `PUSH <n>` | Push integer `n` onto the stack |
| `POP` | Pop the top of the stack |
| `ADD` | Pop the top value, add it to the new top |
| `SUB` | Pop the top value, subtract it from the new top |
| `PRINT "text"` | Print a string literal |
| `READ` | Read an integer from stdin (via `scanf`) and push it |
| `JUMP.EQ.0 <label>` | Jump to `<label>` if the top of the stack is `0` |
| `JUMP.GT.0 <label>` | Jump to `<label>` if the top of the stack is `> 0` |
| `HALT` | Exit the program |
| `label:` | Define a jump target |

### Additional functionality

- The compiler supports instructions like `PUSH`, `PRINT`, `JUMP` (including conditional jumps), `ADD`, and `SUB`.
- Arithmetic operations are performed using assembly registers.
- Conditional jumps are implemented using comparison instructions.
- The `READ` instruction is optionally implemented to allow user input, utilizing the `scanf` function.

## Usage

```bash
python Compiler.py path/to/program.oml
```

This produces `program.asm`, assembles and links it, and runs the resulting executable.

## Testing and running the compiler

Sample programs written in OML are used for testing. The compiler takes the source code file as input and produces the corresponding executable. The generated executables can be run to verify the functionality of the compiler.

## Requirements

- Python 3
- [NASM](https://www.nasm.us/)
- GCC

## Known limitations

- Error handling is mostly stubbed out (see the `# Add Error Handling` markers in the source) — malformed OML programs will generally fail silently or crash rather than reporting a useful error.
- The assemble step currently invokes NASM with the `elf64` output format, which targets Linux, while the assembly it generates assumes the Windows x64 calling convention and calls the Windows `ExitProcess` API. In practice this was built and exercised on a specific local Windows/NASM/GCC setup; the assemble/link commands may need adjusting (e.g. `-f win64`) to run cleanly elsewhere.
- No optimization passes — generated assembly is a direct, unoptimized translation of the token stream.

## Conclusion

This project demonstrates the construction of a basic compiler for a simple programming language. By following these steps and understanding the underlying concepts, it was a useful way to get hands-on insight into compiler design and implementation.

## References

- [Compiler Programming Tutorial (YouTube playlist)](https://www.youtube.com/playlist?list=PLpM-Dvs8t0VbMZA7wW9aR3EtBqe2kinu4)
- [x86-64 Assembly Tutorial](https://sonictk.github.io/asm_tutorial/)
- [x86-64 Assembly Programming (YouTube playlist)](https://www.youtube.com/playlist?list=PLRAdsfhKI4OWNOSfS7EUu5GRAVmze1t2y)
- [Building a compiler from scratch (YouTube)](https://youtu.be/GsCWivTeFpY?si=hOEN7wlnLP_9o7nz)
- [Additional compiler-construction playlist](https://youtube.com/playlist?list=PLUDlas_Zy_qC7c5tCgTMYq2idyyT241qs&si=6pg7TCfs5TkscMia)
