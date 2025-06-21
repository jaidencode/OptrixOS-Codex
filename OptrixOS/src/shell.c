#include "shell.h"
#include "io.h"

void shell() {
    print("DreamOS Shell v1\n> ");
    char input[80];
    int idx = 0;

    while (1) {
        char c = 0;
        asm volatile ("inb $0x60, %0" : "=a"(c));
        if (c & 0x80) continue; // key release
        if (c == 0x1C) { // Enter
            input[idx] = 0;
            print("\n");
            if (input[0] == 'h' && input[1] == 'i') print("Hello!\n");
            else if (input[0] == 'r' && input[1] == 'e' && input[2] == 'b' && input[3] == 'o' && input[4] == 'o' && input[5] == 't')
                asm volatile ("int $0x19");
            else print("> ");
            idx = 0;
        } else if (c == 0x0E && idx > 0) { // Backspace
            idx--;
        } else if (c >= 2 && c <= 40 && idx < 79) { // simple ASCII mapping
            char cc = "1234567890qwertyuiopasdfghjklzxcvbnm"[c-2];
            input[idx++] = cc;
            char out[2] = {cc,0};
            print(out);
        }
    }
}
