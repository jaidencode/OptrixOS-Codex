#include "kernel.h"
#include "io.h"
#include "shell.h"
#include "isr.h"

extern void gdt_install();

void kmain() {
    gdt_install();
    isr_install();
    clear_screen();
    print("DreamOS Kernel Ready\n");
    shell();
    for (;;);
}
