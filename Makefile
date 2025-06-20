CC = gcc
LD = ld
NASM = nasm
CFLAGS = -m32 -ffreestanding -O2 -Wall -Wextra
LDFLAGS = -m elf_i386
BUILD = build
IMG = OptrixOS.img

OBJS = $(BUILD)/boot.o $(BUILD)/kernel.o \
       $(BUILD)/string.o $(BUILD)/vfs.o $(BUILD)/ext2.o $(BUILD)/fat32.o $(BUILD)/ntfs.o

all: $(IMG)

$(BUILD)/kernel.bin: $(OBJS) linker.ld
        $(LD) $(LDFLAGS) -T linker.ld -o $@ $(OBJS)

$(BUILD)/bootloader.bin: $(BUILD)/kernel.bin | $(BUILD)
        $(eval SECTORS := $(shell expr \( $(shell stat -c %s $< ) + 511 \) / 512))
        $(NASM) -f bin -DKERNEL_SECTORS=$(SECTORS) src/bootloader.s -o $@

$(IMG): $(BUILD)/bootloader.bin $(BUILD)/kernel.bin
        cat $(BUILD)/bootloader.bin $(BUILD)/kernel.bin > $@

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

iso: $(IMG)
        @echo "ISO target is no longer used. Built $(IMG) instead."
	
clean:
        rm -rf $(BUILD) $(IMG)

.PHONY: all iso clean
