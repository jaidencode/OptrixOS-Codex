CC = gcc
LD = ld
NASM = nasm
CFLAGS = -m32 -ffreestanding -O2 -Wall -Wextra
LDFLAGS = -m elf_i386
BUILD = build
ISO = OptrixOS.iso

OBJS = $(BUILD)/boot.o $(BUILD)/kernel.o \
       $(BUILD)/vfs.o $(BUILD)/ext2.o $(BUILD)/fat32.o $(BUILD)/ntfs.o

all: $(BUILD)/kernel.bin

$(BUILD)/kernel.bin: $(OBJS) linker.ld
	$(LD) $(LDFLAGS) -T linker.ld -o $@ $(OBJS)

$(BUILD)/boot.o: src/boot.s | $(BUILD)
	$(NASM) -f elf32 $< -o $@

$(BUILD)/kernel.o: src/kernel.c | $(BUILD)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD)/vfs.o: src/fs/vfs.c | $(BUILD)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD)/ext2.o: src/fs/ext2.c | $(BUILD)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD)/fat32.o: src/fs/fat32.c | $(BUILD)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD)/ntfs.o: src/fs/ntfs.c | $(BUILD)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD):
	mkdir -p $(BUILD)

iso: all
	mkdir -p $(BUILD)/isofiles/boot/grub
	cp $(BUILD)/kernel.bin $(BUILD)/isofiles/boot/kernel.bin
	echo 'set timeout=0' > $(BUILD)/isofiles/boot/grub/grub.cfg
	echo 'menuentry "OptrixOS" { multiboot /boot/kernel.bin }' >> $(BUILD)/isofiles/boot/grub/grub.cfg
	grub-mkrescue -o $(ISO) $(BUILD)/isofiles 2>/dev/null

clean:
	rm -rf $(BUILD) $(ISO)

.PHONY: all iso clean
