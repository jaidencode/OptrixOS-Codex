import os, shutil, subprocess
# --- CONFIGURATION ---
TOOLCHAIN_DIR = os.environ.get("TOOLCHAIN_DIR") or r"C:\\Users\\jaide\\Downloads\\i686-elf-tools-windows\\bin"
CC = os.environ.get("CC") or os.path.join(TOOLCHAIN_DIR, "i686-elf-gcc.exe")
LD = os.environ.get("LD") or os.path.join(TOOLCHAIN_DIR, "i686-elf-ld.exe")
OBJDUMP = os.environ.get("OBJDUMP") or os.path.join(TOOLCHAIN_DIR, "i686-elf-objdump.exe")
NASM = "nasm"

if not os.path.isfile(CC):
    CC = shutil.which("i686-linux-gnu-gcc") or "i686-linux-gnu-gcc"
if not os.path.isfile(LD):
    LD = shutil.which("i686-linux-gnu-ld") or "i686-linux-gnu-ld"
if not os.path.isfile(OBJDUMP):
    OBJDUMP = shutil.which("i686-linux-gnu-objdump") or "i686-linux-gnu-objdump"

if not shutil.which(CC):
    CC = "gcc"
if not shutil.which(LD):
    LD = "ld"
if not shutil.which(OBJDUMP):
    OBJDUMP = "objdump"

CDRTOOLS_DIR = os.environ.get("CDRTOOLS_DIR") or r"C:\\Program Files (x86)\\cdrtools"
MKISOFS_EXE = os.environ.get("MKISOFS") or os.path.join(CDRTOOLS_DIR, "mkisofs.exe")
if not os.path.isfile(MKISOFS_EXE):
    MKISOFS_EXE = shutil.which("mkisofs") or "mkisofs"

def run(cmd):
    print(' '.join(cmd))
    subprocess.check_call(cmd)


def compile_kernel():
    os.makedirs('build', exist_ok=True)
    run([NASM, '-f', 'elf32', 'src/boot.s', '-o', 'build/boot.o'])
    run([CC, '-m32', '-ffreestanding', '-O2', '-c', 'src/kernel.c', '-o', 'build/kernel.o'])
    run([CC, '-m32', '-ffreestanding', '-O2', '-c', 'src/string.c', '-o', 'build/string.o'])
    run([CC, '-m32', '-ffreestanding', '-O2', '-c', 'src/fs/vfs.c', '-o', 'build/vfs.o'])
    run([CC, '-m32', '-ffreestanding', '-O2', '-c', 'src/fs/ext2.c', '-o', 'build/ext2.o'])
    run([CC, '-m32', '-ffreestanding', '-O2', '-c', 'src/fs/fat32.c', '-o', 'build/fat32.o'])
    run([CC, '-m32', '-ffreestanding', '-O2', '-c', 'src/fs/ntfs.c', '-o', 'build/ntfs.o'])
    run([LD, '-m', 'elf_i386', '-T', 'linker.ld', '-o', 'build/kernel.bin',
         'build/boot.o', 'build/kernel.o', 'build/string.o', 'build/vfs.o',
         'build/ext2.o', 'build/fat32.o', 'build/ntfs.o'])

def make_iso():
    os.makedirs('build/isofiles/boot/grub', exist_ok=True)
    shutil.copy('build/kernel.bin', 'build/isofiles/boot/kernel.bin')
    cfg = 'build/isofiles/boot/grub/grub.cfg'
    with open(cfg, 'w') as f:
        f.write('set timeout=0\n')
        f.write('menuentry "OptrixOS" { multiboot /boot/kernel.bin }\n')

    core_img = 'build/isofiles/boot/grub/core.img'
    run(['grub-mkstandalone', '-O', 'i386-pc',
         '--modules=biosdisk iso9660 normal multiboot',
         '--locales=', '--fonts=', '--compress=xz',
         '-o', core_img,
         f'boot/grub/grub.cfg={cfg}'])

    bios_img = 'build/isofiles/boot/grub/bios.img'
    cdboot = '/usr/lib/grub/i386-pc/cdboot.img'
    with open(bios_img, 'wb') as out:
        for part in (cdboot, core_img):
            with open(part, 'rb') as p:
                out.write(p.read())

    run(['xorriso', '-as', 'mkisofs', '-R', '-b', 'boot/grub/bios.img',
         '-no-emul-boot', '-boot-load-size', '4', '-boot-info-table',
         '-o', 'OptrixOS.iso', 'build/isofiles'])

if __name__ == '__main__':
    compile_kernel()
    make_iso()
