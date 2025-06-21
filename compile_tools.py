import os
import shutil
import subprocess
import math

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(SCRIPT_DIR, 'OptrixOS')
BOOT_DIR = os.path.join(ROOT_DIR, 'boot')
ASM_DIR = os.path.join(ROOT_DIR, 'asm')
C_DIR = os.path.join(ROOT_DIR, 'c')
H_DIR = os.path.join(ROOT_DIR, 'h')
BUILD = os.path.join(SCRIPT_DIR, 'build')
ISO_NAME = os.path.join(SCRIPT_DIR, 'OptrixOS.iso')

NASM = shutil.which('nasm') or 'nasm'
MKISOFS = shutil.which('mkisofs') or 'mkisofs'

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
    run([NASM, '-f', 'bin', os.path.join(BOOT_DIR, 'stage2.asm'), '-o', stage2_bin])
    stage2_sectors = math.ceil(os.path.getsize(stage2_bin) / 512)

    kernel_bin = os.path.join(BUILD, 'kernel.bin')
    run([NASM, '-f', 'bin', os.path.join(ASM_DIR, 'kernel.asm'), '-o', kernel_bin])
    kernel_sectors = math.ceil(os.path.getsize(kernel_bin) / 512)

    # BIOS sector numbering starts at 1, so the kernel must be placed
    # after the boot sector (1) and stage2 (starting at sector 2).
    # stage2 occupies `stage2_sectors` sectors beginning at sector 2,
    # therefore the first kernel sector is 2 + stage2_sectors.
    run([NASM, '-f', 'bin',
         f'-DKERNEL_START_SECTOR={2 + stage2_sectors}',
         f'-DKERNEL_SECTORS={kernel_sectors}',
         os.path.join(BOOT_DIR, 'stage2.asm'), '-o', stage2_bin])

    boot_bin = os.path.join(BUILD, 'boot.bin')
    run([NASM, '-f', 'bin', f'-DSTAGE2_SECTORS={stage2_sectors}',
         os.path.join(BOOT_DIR, 'boot.asm'), '-o', boot_bin])
    return stage2_sectors


def create_image(stage2_sectors):
    boot_bin = os.path.join(BUILD, 'boot.bin')
    stage2_bin = os.path.join(BUILD, 'stage2.bin')
    kernel_bin = os.path.join(BUILD, 'kernel.bin')

    img_path = os.path.join(BUILD, 'boot.img')
    run(['dd', 'if=/dev/zero', f'of={img_path}', 'bs=512', 'count=2880'])
    run(['dd', f'if={boot_bin}', f'of={img_path}', 'conv=notrunc'])
    run(['dd', f'if={stage2_bin}', f'of={img_path}', 'seek=1', 'conv=notrunc'])
    run(['dd', f'if={kernel_bin}', f'of={img_path}', f'seek={1 + stage2_sectors}', 'conv=notrunc'])
    return img_path


def create_iso(img_path):
    iso_root = os.path.join(BUILD, 'iso_root')
    os.makedirs(iso_root, exist_ok=True)
    shutil.copy(img_path, os.path.join(iso_root, 'boot.img'))
    copytree_overwrite(ROOT_DIR, os.path.join(iso_root, 'OptrixOS'))
    run([MKISOFS, '-quiet', '-V', 'OPTRIXOS', '-input-charset', 'iso8859-1', '-o', ISO_NAME,
         '-b', 'boot.img', '-no-emul-boot', '-boot-load-size', '4', '-boot-info-table', iso_root])


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
