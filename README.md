# OptrixOS-Codex

This repository contains a very small example OS that now boots using a custom bootloader and prints a message to the screen. It provides a starting point for experimenting with OS development. A basic VFS layer with minimal ext2, FAT32 and NTFS drivers is included for demonstration purposes.

The bootloader now prints simple debug messages during startup so you can observe each stage of the boot process. These messages show when the kernel and root filesystem are loaded and report any disk errors before halting.

## Building

1. Install `nasm` and `genisoimage`.
2. Run `python3 compile_tools.py` or simply `make` to build `OptrixOS.iso`.
3. Boot the ISO with QEMU:
   ```bash
   qemu-system-i386 -cdrom OptrixOS.iso
   ```

`compile_tools.py` now builds a 16MB disk image with two partitions.  The first
bootable partition contains the bootloader and kernel while the second is an
ext2 formatted partition holding a tiny root filesystem.  After booting the
kernel launches a simple command shell.

The intermediate image is removed after the ISO is created.
