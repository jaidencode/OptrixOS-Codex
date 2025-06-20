CC = gcc
LD = ld
NASM = nasm
CFLAGS = -m32 -ffreestanding -O2 -Wall -Wextra
LDFLAGS = -m elf_i386
BUILD = build
ISO = OptrixOS.iso

all: $(BUILD)/kernel.bin

$(BUILD)/kernel.bin: $(BUILD)/boot.o $(BUILD)/kernel.o linker.ld
	$(LD) $(LDFLAGS) -T linker.ld -o $@ $(BUILD)/boot.o $(BUILD)/kernel.o

$(BUILD)/boot.o: src/boot.s | $(BUILD)
	$(NASM) -f elf32 $< -o $@

$(BUILD)/kernel.o: src/kernel.c | $(BUILD)
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
