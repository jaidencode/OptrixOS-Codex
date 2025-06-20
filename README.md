# OptrixOS-Codex

This repository contains a very small example OS that boots via GRUB and prints a message to the screen. It provides a starting point for experimenting with OS development. A basic VFS layer with minimal ext2, FAT32 and NTFS drivers is included for demonstration purposes.

## Building

1. Install `nasm`, `grub-pc-bin` and `xorriso`.
2. Run `python3 compile_tools.py` or simply `make iso` to build `OptrixOS.iso`.
   ISO creation now uses `grub-mkstandalone` together with `xorriso`.
3. Test the ISO with an emulator such as QEMU:
   ```bash
   qemu-system-i386 -cdrom OptrixOS.iso
   ```

The `compile_tools.py` script sets up toolchain defaults and builds the kernel and ISO using `grub-mkstandalone` and `xorriso`.
