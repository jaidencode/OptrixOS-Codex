#ifndef IO_H
#define IO_H

void outb(unsigned short port, unsigned char val);
unsigned char inb(unsigned short port);
void clear_screen();
void print(const char* str);
void set_text_attr(unsigned char attr);

#endif
