# OptrixOS-Codex

This repository demonstrates a very small example operating system.  The bootloader loads a tiny kernel that clears the screen to a blue background with white text and displays a short message.

## Directory layout

- `OptrixOS/boot` – first and second stage bootloaders (`boot.asm`, `stage2.asm`)
- `OptrixOS/asm` – assembly sources for the kernel (`kernel.asm`)
- `OptrixOS/c` – C sources (empty by default)
- `OptrixOS/h` – header files (empty by default)

## Building

1. Install `nasm` and `mkisofs` (sometimes provided by the `genisoimage` package).
2. Run `python3 compile_tools.py` to produce `OptrixOS.iso`.
3. Boot the ISO with QEMU:
   ```bash
   qemu-system-i386 -cdrom OptrixOS.iso
   ```
