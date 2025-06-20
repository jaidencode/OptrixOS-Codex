# OptrixOS-Codex

This repository contains a very small example OS that now boots using a custom bootloader and prints a message to the screen. It provides a starting point for experimenting with OS development. A basic VFS layer with minimal ext2, FAT32 and NTFS drivers is included for demonstration purposes.

## Building

1. Install `nasm` and `genisoimage`.
2. Run `python3 compile_tools.py` or simply `make` to build `OptrixOS.iso`.
3. Test the ISO with an emulator such as QEMU:
   ```bash
   qemu-system-i386 -cdrom OptrixOS.iso
   ```

The `compile_tools.py` script builds the kernel, creates `OptrixOS.img` and then packages it as a bootable ISO.
