import os, shutil, subprocess, struct
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


def create_rootfs():
    os.makedirs('rootfs', exist_ok=True)
    if not os.listdir('rootfs'):
        with open(os.path.join('rootfs', 'hello.txt'), 'w') as f:
            f.write('Hello from disk')
    with open('rootfs.bin', 'wb') as out:
        files = os.listdir('rootfs')
        out.write(struct.pack('<I', len(files)))
        for name in files:
            path = os.path.join('rootfs', name)
            with open(path, 'rb') as f:
                data = f.read()
            name_b = name.encode('utf-8')
            out.write(struct.pack('<I', len(name_b)))
            out.write(name_b)
            out.write(struct.pack('<I', len(data)))
            out.write(data)


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

def compile_bootloader(kernel_sectors, rootfs_sectors, rootfs_size):
    args = [NASM, '-f', 'bin',
            f'-DKERNEL_SECTORS={kernel_sectors}',
            '-DKERNEL_LBA=1',
            f'-DROOTFS_SECTORS={rootfs_sectors}',
            f'-DROOTFS_SIZE={rootfs_size}',
            f'-DROOTFS_LBA={1 + kernel_sectors}',
            '-DROOTFS_LOAD_ADDR=0x200000',
            'src/bootloader.s', '-o', 'build/bootloader.bin']
    run(args)

def make_image():
    create_rootfs()
    ksize = os.path.getsize('build/kernel.bin')
    ksectors = (ksize + 511) // 512
    rsize = os.path.getsize('rootfs.bin')
    rsectors = (rsize + 511) // 512
    compile_bootloader(ksectors, rsectors, rsize)

    disk_size = 16 * 1024 * 1024  # 16MB virtual hard disk
    with open('OptrixOS.img', 'wb') as out:
        out.truncate(disk_size)
        out.seek(0)
        with open('build/bootloader.bin', 'rb') as inp:
            out.write(inp.read())
        out.seek(512)
        with open('build/kernel.bin', 'rb') as inp:
            out.write(inp.read())
        out.seek(512 + ksectors * 512)
        with open('rootfs.bin', 'rb') as inp:
            out.write(inp.read())

def make_iso():
    run([MKISOFS_EXE, '-quiet', '-o', 'OptrixOS.iso', '-b', 'OptrixOS.img',
         '-no-emul-boot', '-boot-load-size', '4', '-boot-info-table', '.'])
    os.remove('OptrixOS.img')

if __name__ == '__main__':
    compile_kernel()
    make_image()
    make_iso()
