#include "shell.h"
#include "io.h"
#include "keyboard.h"
#include <stdint.h>

static char cwd[64] = "/";

static void print_prompt() {
    print("$(");
    print(cwd);
    print(")> ");
}

void shell() {
    print("DreamOS Shell v1\n");
    print_prompt();
    char input[80];
    int idx = 0;

    while (1) {
        char c = keyboard_getch();
        if(!c) continue;
        if(c == '\n') {
            input[idx] = 0;
            print("\n");
            if(input[0]=='h' && input[1]=='i' && input[2]==0) {
                print("Hello!\n");
            } else if(input[0]=='r' && input[1]=='e' && input[2]=='b' && input[3]=='o' && input[4]=='o' && input[5]=='t' && input[6]==0) {
                asm volatile("int $0x19");
            } else if(input[0]=='c' && input[1]=='d' && input[2]==' '){
                int j=3,k=0; while(input[j] && k<63){ cwd[k++]=input[j++]; }
                cwd[k]=0; if(k==0){ cwd[0]='/'; cwd[1]=0; }
            } else {
                print("Unknown command\n");
            }
            idx = 0;
            print_prompt();
        } else if(c == 8 && idx>0) {
            idx--;
        } else if(c >= 32 && idx < 79) {
            input[idx++] = c;
            char out[2] = {c,0};
            print(out);
        }
    }
}
