# OptrixOS-Codex

This repository contains a very small example OS that now boots using a custom bootloader and prints a message to the screen. It provides a starting point for experimenting with OS development. A basic VFS layer with minimal ext2, FAT32 and NTFS drivers is included for demonstration purposes.

## Building

1. Install `nasm` and `genisoimage`.
2. Run `python3 compile_tools.py` or simply `make` to build `OptrixOS.iso`.
3. Boot the ISO with QEMU:
   ```bash
   qemu-system-i386 -cdrom OptrixOS.iso
   ```

`compile_tools.py` creates a 16MB virtual disk during the build and embeds it directly into `OptrixOS.iso`. The intermediate image is removed.
