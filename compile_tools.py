import os
import shutil
import subprocess
import math
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(SCRIPT_DIR, 'OptrixOS')
BOOT_DIR = os.path.join(ROOT_DIR, 'boot')
ASM_DIR = os.path.join(ROOT_DIR, 'asm')
SRC_DIR = os.path.join(SCRIPT_DIR, 'src')
C_DIR = os.path.join(SRC_DIR, 'c')
H_DIR = os.path.join(SRC_DIR, 'h')
BUILD = os.path.join(SCRIPT_DIR, 'build')
ISO_NAME = os.path.join(SCRIPT_DIR, 'OptrixOS.iso')

# --- TOOLCHAIN CONFIGURATION ---
TOOLCHAIN_DIR = os.environ.get("TOOLCHAIN_DIR") or r"C:\\Users\\jaide\\Downloads\\i686-elf-tools-windows\\bin"
CC = os.environ.get("CC") or os.path.join(TOOLCHAIN_DIR, "i686-elf-gcc.exe")
LD = os.environ.get("LD") or os.path.join(TOOLCHAIN_DIR, "i686-elf-ld.exe")
OBJDUMP = os.environ.get("OBJDUMP") or os.path.join(TOOLCHAIN_DIR, "i686-elf-objdump.exe")
NASM = os.environ.get("NASM") or shutil.which("nasm") or "nasm"

if not os.path.isfile(CC):
    CC = shutil.which("i686-linux-gnu-gcc") or shutil.which("gcc") or "gcc"
if not os.path.isfile(LD):
    LD = shutil.which("i686-linux-gnu-ld") or shutil.which("ld") or "ld"
if not os.path.isfile(OBJDUMP):
    OBJDUMP = shutil.which("i686-linux-gnu-objdump") or shutil.which("objdump") or "objdump"

CDRTOOLS_DIR = os.environ.get("CDRTOOLS_DIR") or r"C:\\Program Files (x86)\\cdrtools"
MKISOFS = os.environ.get("MKISOFS") or os.path.join(CDRTOOLS_DIR, "mkisofs.exe")
if not os.path.isfile(MKISOFS):
    MKISOFS = shutil.which("mkisofs") or "mkisofs"
DD = shutil.which("dd") or shutil.which("dd.exe") or "dd"

def run(cmd):
    print(' '.join(str(x) for x in cmd))
    subprocess.check_call(cmd)

def copytree_overwrite(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

def assemble():
    os.makedirs(BUILD, exist_ok=True)
    stage2_bin = os.path.join(BUILD, 'stage2.bin')
    kernel_bin = os.path.join(BUILD, 'kernel.bin')
    boot_bin = os.path.join(BUILD, 'boot.bin')

    run([NASM, '-f', 'bin', os.path.join(BOOT_DIR, 'stage2.asm'), '-o', stage2_bin])
    stage2_sectors = math.ceil(os.path.getsize(stage2_bin) / 512)
    run([NASM, '-f', 'bin', os.path.join(ASM_DIR, 'kernel.asm'), '-o', kernel_bin])
    kernel_sectors = math.ceil(os.path.getsize(kernel_bin) / 512)
    run([NASM, '-f', 'bin',
         f'-DKERNEL_START_SECTOR={2 + stage2_sectors}',
         f'-DKERNEL_SECTORS={kernel_sectors}',
         os.path.join(BOOT_DIR, 'stage2.asm'), '-o', stage2_bin])
    run([NASM, '-f', 'bin', f'-DSTAGE2_SECTORS={stage2_sectors}',
         os.path.join(BOOT_DIR, 'boot.asm'), '-o', boot_bin])

    # Only build C sources if the directory exists
    if os.path.isdir(C_DIR):
        for src_file in os.listdir(C_DIR):
            if src_file.endswith('.c'):
                out_obj = os.path.join(BUILD, src_file.replace('.c', '.o'))
                run([CC, '-m32', '-ffreestanding', '-fno-pic', '-nostdlib', '-fno-builtin', '-fno-stack-protector',
                     '-c', os.path.join(C_DIR, src_file), '-o', out_obj])
    else:
        print(f"[WARN] C source directory '{C_DIR}' not found, skipping C compilation.")

    return stage2_sectors

def create_image(stage2_sectors):
    boot_bin = os.path.join(BUILD, 'boot.bin')
    stage2_bin = os.path.join(BUILD, 'stage2.bin')
    kernel_bin = os.path.join(BUILD, 'kernel.bin')
    img_path = os.path.join(BUILD, 'boot.img')
    run([DD, 'if=/dev/zero', f'of={img_path}', 'bs=512', 'count=2880'])
    run([DD, f'if={boot_bin}', f'of={img_path}', 'conv=notrunc'])
    run([DD, f'if={stage2_bin}', f'of={img_path}', 'seek=1', 'conv=notrunc'])
    run([DD, f'if={kernel_bin}', f'of={img_path}', f'seek={1 + stage2_sectors}', 'conv=notrunc'])
    return img_path

def create_iso(img_path):
    iso_root = os.path.join(BUILD, 'iso_root')
    os.makedirs(iso_root, exist_ok=True)
    shutil.copy(img_path, os.path.join(iso_root, 'boot.img'))
    copytree_overwrite(ROOT_DIR, os.path.join(iso_root, 'OptrixOS'))
    run([
        MKISOFS,
        '-quiet',
        '-V',
        'OPTRIXOS',
        '-input-charset',
        'iso8859-1',
        '-o',
        ISO_NAME,
        '-b',
        'boot.img',
        '-boot-info-table',
        iso_root,
    ])

def cleanup():
    if not os.path.isdir(BUILD):
        return
    for f in os.listdir(BUILD):
        path = os.path.join(BUILD, f)
        if os.path.isdir(path):
            shutil.rmtree(path, ignore_errors=True)
        else:
            os.remove(path)
    shutil.rmtree(BUILD, ignore_errors=True)

def build():
    stage2_sectors = assemble()
    img = create_image(stage2_sectors)
    create_iso(img)
    cleanup()
    print('ISO created at', ISO_NAME)

if __name__ == '__main__':
    build()
