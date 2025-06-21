#include "kernel.h"
#include "io.h"
#include "shell.h"
#include "isr.h"

extern void gdt_install();

void kmain() {
    gdt_install();
    isr_install();
    set_text_attr(0x1F);
    clear_screen();
    print("DreamOS Kernel Ready\n");
    shell();
    for (;;);
}
