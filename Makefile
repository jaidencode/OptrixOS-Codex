CC = gcc
LD = ld
NASM = nasm
CFLAGS = -m32 -ffreestanding -O2 -Wall -Wextra
LDFLAGS = -m elf_i386
BUILD = build
IMG = OptrixOS.img
ISO = OptrixOS.iso

OBJS = $(BUILD)/boot.o $(BUILD)/kernel.o \
       $(BUILD)/string.o $(BUILD)/vfs.o $(BUILD)/ext2.o $(BUILD)/fat32.o $(BUILD)/ntfs.o

all: $(ISO)

$(BUILD)/kernel.bin: $(OBJS) linker.ld
	$(LD) $(LDFLAGS) -T linker.ld -o $@ $(OBJS)

$(BUILD)/bootloader.bin: $(BUILD)/kernel.bin | $(BUILD)
	$(eval SECTORS := $(shell expr \( $(shell stat -c %s $< ) + 511 \) / 512))
	$(NASM) -f bin -DKERNEL_SECTORS=$(SECTORS) src/bootloader.s -o $@

$(IMG): $(BUILD)/bootloader.bin $(BUILD)/kernel.bin
	dd if=/dev/zero of=$@ bs=1M count=16
	dd if=$(BUILD)/bootloader.bin of=$@ conv=notrunc
	dd if=$(BUILD)/kernel.bin of=$@ bs=512 seek=1 conv=notrunc

$(BUILD)/boot.o: src/boot.s | $(BUILD)
	$(NASM) -f elf32 $< -o $@

$(BUILD)/kernel.o: src/kernel.c | $(BUILD)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD)/string.o: src/string.c | $(BUILD)
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

$(ISO): $(IMG)
	genisoimage -quiet -o $@ -b $(IMG) -no-emul-boot -boot-load-size 4 -boot-info-table .

iso: $(ISO)
	
clean:
	rm -rf $(BUILD) $(IMG) $(ISO)

.PHONY: all iso clean
