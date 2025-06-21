import os, subprocess

BUILD = 'build'

BOOT_DIR = 'OptrixOS/boot'
SRC_DIR = 'OptrixOS/src'

CC = 'gcc'
LD = 'ld'
NASM = 'nasm'

CFLAGS = ['-m32', '-ffreestanding', '-fno-pic', '-nostdlib', '-fno-builtin',
          '-fno-stack-protector']


def run(cmd):
    print(' '.join(cmd))
    subprocess.check_call(cmd)


def build():
    os.makedirs(BUILD, exist_ok=True)
    run([NASM, '-f', 'bin', os.path.join(BOOT_DIR, 'boot.asm'), '-o', f'{BUILD}/boot.bin'])
    run([NASM, '-f', 'bin', os.path.join(BOOT_DIR, 'stage2.asm'), '-o', f'{BUILD}/stage2.bin'])
    run([NASM, '-f', 'elf', os.path.join(SRC_DIR, 'gdt.asm'), '-o', f'{BUILD}/gdt.o'])
    run([NASM, '-f', 'elf', os.path.join(SRC_DIR, 'isr.asm'), '-o', f'{BUILD}/isr.o'])

    for src in ['kernel.c', 'io.c', 'shell.c', 'idt.c']:
        run([CC] + CFLAGS + ['-c', os.path.join(SRC_DIR, src), '-o', f'{BUILD}/{src[:-2]}.o'])

    run([LD, '-m', 'elf_i386', '-Ttext', '0x10000', '-o', f'{BUILD}/os.elf',
         f'{BUILD}/gdt.o', f'{BUILD}/io.o', f'{BUILD}/kernel.o', f'{BUILD}/shell.o', f'{BUILD}/idt.o', f'{BUILD}/isr.o'])
    run(['objcopy', '-O', 'binary', f'{BUILD}/os.elf', f'{BUILD}/os.bin'])

    run(['dd', 'if=/dev/zero', f'of={BUILD}/os.img', 'bs=512', 'count=2880'])
    run(['dd', f'if={BUILD}/boot.bin', f'of={BUILD}/os.img', 'conv=notrunc'])
    run(['dd', f'if={BUILD}/stage2.bin', f'of={BUILD}/os.img', 'seek=1', 'conv=notrunc'])
    run(['dd', f'if={BUILD}/os.bin', f'of={BUILD}/os.img', 'seek=4', 'conv=notrunc'])
    print('Image created at', f'{BUILD}/os.img')


if __name__ == '__main__':
    build()
