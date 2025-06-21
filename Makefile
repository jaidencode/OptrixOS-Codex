AS=nasm
CC=gcc
LD=ld
CFLAGS=-m32 -ffreestanding -fno-pic -nostdlib -fno-builtin -fno-stack-protector -nostartfiles -nodefaultlibs

all: os.img

boot/boot.bin: boot/boot.asm
	$(AS) -f bin $< -o $@

boot/stage2.bin: boot/stage2.asm
	$(AS) -f bin $< -o $@

src/gdt.o: src/gdt.asm
	$(AS) -f elf $< -o $@

src/isr.o: src/isr.asm
	$(AS) -f elf $< -o $@

src/%.o: src/%.c
	$(CC) $(CFLAGS) -c $< -o $@

os.bin: src/gdt.o src/io.o src/kernel.o src/shell.o src/idt.o src/isr.o
	$(LD) -m elf_i386 -Ttext 0x10000 -o os.elf $^
	objcopy -O binary os.elf $@

os.img: boot/boot.bin boot/stage2.bin os.bin
	dd if=/dev/zero of=os.img bs=512 count=2880
	dd if=boot/boot.bin of=os.img conv=notrunc
	dd if=boot/stage2.bin of=os.img seek=1 conv=notrunc
	dd if=os.bin of=os.img seek=4 conv=notrunc

run: os.img
	qemu-system-i386 -fda os.img

clean:
	rm -f boot/*.bin src/*.o *.elf *.bin *.img
