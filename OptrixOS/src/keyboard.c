#include "keyboard.h"
#include "io.h"

static int shift = 0;

static const char sc_ascii[] = {
    0,27,'1','2','3','4','5','6','7','8','9','0','-','=',8,
    '\t','q','w','e','r','t','y','u','i','o','p','[',']','\n',0,
    'a','s','d','f','g','h','j','k','l',';','\'', '`',0,'\\',
    'z','x','c','v','b','n','m',',','.','/',0,'*',0,' ',0,
};

static const char sc_ascii_shift[] = {
    0,27,'!','@','#','$','%','^','&','*','(',')','_','+',8,
    '\t','Q','W','E','R','T','Y','U','I','O','P','{','}','\n',0,
    'A','S','D','F','G','H','J','K','L',':','"','~',0,'|',
    'Z','X','C','V','B','N','M','<','>','?',0,'*',0,' ',0,
};

char keyboard_getch() {
    unsigned char c = inb(0x60);
    if(c & 0x80) {
        if(c == 0xAA || c == 0xB6)
            shift = 0;
        return 0;
    } else {
        if(c == 0x2A || c == 0x36) { shift = 1; return 0; }
        if(c == 0x1C) return '\n';
        if(c == 0x0E) return 8; // backspace
        if(c >= sizeof(sc_ascii)) return 0;
        return shift ? sc_ascii_shift[c] : sc_ascii[c];
    }
}
