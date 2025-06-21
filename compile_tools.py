import os
import shutil
import subprocess
import glob

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(SCRIPT_DIR, 'build')
BOOT_DIR = os.path.join(SCRIPT_DIR, 'OptrixOS', 'boot')
SRC_DIR = os.path.join(SCRIPT_DIR, 'OptrixOS', 'src')
ISO_NAME = os.path.join(SCRIPT_DIR, 'OptrixOS.iso')

# Toolchain config
TOOLCHAIN_DIR = os.environ.get("TOOLCHAIN_DIR") or r"C:\Users\jaide\Downloads\i686-elf-tools-windows\bin"
CC = os.environ.get("CC") or os.path.join(TOOLCHAIN_DIR, "i686-elf-gcc.exe")
LD = os.environ.get("LD") or os.path.join(TOOLCHAIN_DIR, "i686-elf-ld.exe")
OBJCOPY = os.environ.get("OBJCOPY") or os.path.join(TOOLCHAIN_DIR, "i686-elf-objcopy.exe")
NASM = "nasm"

if not os.path.isfile(CC): CC = shutil.which("i686-linux-gnu-gcc") or "i686-linux-gnu-gcc"
if not os.path.isfile(LD): LD = shutil.which("i686-linux-gnu-ld") or "i686-linux-gnu-ld"
if not os.path.isfile(OBJCOPY): OBJCOPY = shutil.which("i686-linux-gnu-objcopy") or "i686-linux-gnu-objcopy"
if not shutil.which(CC): CC = "gcc"
if not shutil.which(LD): LD = "ld"
if not shutil.which(OBJCOPY): OBJCOPY = "objcopy"

CDRTOOLS_DIR = os.environ.get("CDRTOOLS_DIR") or r"C:\Program Files (x86)\cdrtools"
MKISOFS_EXE = os.environ.get("MKISOFS") or os.path.join(CDRTOOLS_DIR, "mkisofs.exe")
if not os.path.isfile(MKISOFS_EXE): MKISOFS_EXE = shutil.which("mkisofs") or "mkisofs"

CFLAGS = [
    '-m32', '-ffreestanding', '-fno-pic', '-nostdlib', '-fno-stack-protector'
]

def run(cmd):
    print(' '.join([str(x) for x in cmd]))
    subprocess.check_call(cmd)

def copytree_overwrite(src, dst):
    # Python 3.8+ has dirs_exist_ok, but let's be universal
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

def build():
    os.makedirs(BUILD, exist_ok=True)
    run([NASM, '-f', 'bin', os.path.join(BOOT_DIR, 'boot.asm'), '-o', os.path.join(BUILD, 'boot.bin')])
    run([NASM, '-f', 'bin', os.path.join(BOOT_DIR, 'stage2.asm'), '-o', os.path.join(BUILD, 'stage2.bin')])
    run([NASM, '-f', 'elf', os.path.join(SRC_DIR, 'gdt.asm'), '-o', os.path.join(BUILD, 'gdt.o')])
    run([NASM, '-f', 'elf', os.path.join(SRC_DIR, 'isr.asm'), '-o', os.path.join(BUILD, 'isr.o')])

    for src in ['kernel.c', 'io.c', 'shell.c', 'idt.c', 'keyboard.c']:
        run([CC] + CFLAGS + ['-c', os.path.join(SRC_DIR, src), '-o', os.path.join(BUILD, f"{src[:-2]}.o")])

    run([LD, '-m', 'elf_i386', '-Ttext', '0x10000', '-o', os.path.join(BUILD, 'os.elf'),
         os.path.join(BUILD, 'gdt.o'), os.path.join(BUILD, 'io.o'), os.path.join(BUILD, 'kernel.o'),
         os.path.join(BUILD, 'shell.o'), os.path.join(BUILD, 'keyboard.o'), os.path.join(BUILD, 'idt.o'), os.path.join(BUILD, 'isr.o')])

    run([OBJCOPY, '-O', 'binary', os.path.join(BUILD, 'os.elf'), os.path.join(BUILD, 'os.bin')])

    # --- Create raw boot image (floppy) ---
    img_path = os.path.join(BUILD, 'boot.img')
    run(['dd', 'if=/dev/zero', f'of={img_path}', 'bs=512', 'count=2880'])
    run(['dd', f'if={os.path.join(BUILD, "boot.bin")}', f'of={img_path}', 'conv=notrunc'])
    run(['dd', f'if={os.path.join(BUILD, "stage2.bin")}', f'of={img_path}', 'seek=1', 'conv=notrunc'])
    run(['dd', f'if={os.path.join(BUILD, "os.bin")}', f'of={img_path}', 'seek=4', 'conv=notrunc'])

    # --- Prepare ISO staging area ---
    iso_root = os.path.join(BUILD, 'iso_root')
    os.makedirs(iso_root, exist_ok=True)

    # Place boot image at root for El Torito boot
    shutil.copy(img_path, os.path.join(iso_root, 'boot.img'))

    # Copy OptrixOS/boot and OptrixOS/src as directories (with all files/subdirs)
    BOOT_DST = os.path.join(iso_root, 'boot')
    SRC_DST = os.path.join(iso_root, 'src')
    copytree_overwrite(BOOT_DIR, BOOT_DST)
    copytree_overwrite(SRC_DIR, SRC_DST)

    # Optionally: copy the built kernel, or any additional files you want accessible in the ISO root
    shutil.copy(os.path.join(BUILD, 'os.bin'), os.path.join(iso_root, 'os.bin'))
    shutil.copy(os.path.join(BUILD, 'os.elf'), os.path.join(iso_root, 'os.elf'))

    # --- Create ISO with boot and all source folders included ---
    run([
        MKISOFS_EXE, '-quiet', '-V', 'OPTRIXOS', '-input-charset', 'iso8859-1', '-o', ISO_NAME,
        '-b', 'boot.img', '-no-emul-boot', '-boot-load-size', '4', '-boot-info-table', iso_root
    ])

    print('ISO created at', ISO_NAME)

    # --- Cleanup everything except the ISO ---
    for f in glob.glob(os.path.join(BUILD, '*')):
        if os.path.isdir(f):
            shutil.rmtree(f, ignore_errors=True)
        else:
            os.remove(f)
    shutil.rmtree(BUILD, ignore_errors=True)
    print('All build/temp files deleted, ISO remains:', ISO_NAME)

if __name__ == '__main__':
    build()
