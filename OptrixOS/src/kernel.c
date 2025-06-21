#include "kernel.h"
#include "io.h"
#include "shell.h"

void kmain() {
    clear_screen();
    print("DreamOS Kernel Ready\n");
    shell();
    for (;;);
}
