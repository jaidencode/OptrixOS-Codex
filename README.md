# OptrixOS-Codex

This repository contains a very small example OS that now boots using a custom bootloader and prints a message to the screen. It provides a starting point for experimenting with OS development. A basic VFS layer with minimal ext2, FAT32 and NTFS drivers is included for demonstration purposes.

## Building

1. Install `nasm`.
2. Run `python3 compile_tools.py` or simply `make` to build `OptrixOS.img`.
3. Test the image with an emulator such as QEMU:
   ```bash
   qemu-system-i386 -drive format=raw,file=OptrixOS.img
   ```

The `compile_tools.py` script sets up toolchain defaults and builds the kernel and bootable image without relying on GRUB.
