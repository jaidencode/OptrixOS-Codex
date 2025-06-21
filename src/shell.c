#include "shell.h"
#include "fs/vfs.h"
#include "string.h"
#include <stddef.h>

extern void print_char(char c);
extern void print_string(const char *s);
extern void read_line(char *buf, size_t max);

static char current_path[64] = "root";
static char drive_letter = 'C';

static void set_path(const char *p) {
    size_t i = 0;
    while (p[i] && i < sizeof(current_path) - 1) {
        current_path[i] = p[i];
        i++;
    }
    current_path[i] = 0;
}

static void list_printer(const char *name) {
    print_string(name);
    print_char('\n');
}

void shell_run(void) {
    char line[80];
    for (;;) {
        print_char(drive_letter);
        print_string(":\\");
        print_string(current_path);
        print_string("> ");
        read_line(line, sizeof(line));

        if (strcmp(line, "help") == 0) {
            print_string("Commands: help, cd, ls, cat, write, format, halt\n");
        } else if (strncmp(line, "cd ", 3) == 0) {
            set_path(line + 3);
        } else if (strcmp(line, "ls") == 0) {
            vfs_list(list_printer);
        } else if (strncmp(line, "cat ", 4) == 0) {
            char buf[512];
            int r = vfs_read(line + 4, buf, sizeof(buf) - 1);
            if (r < 0) {
                print_string("File not found\n");
            } else {
                buf[r] = 0;
                print_string(buf);
                print_char('\n');
            }
        } else if (strncmp(line, "write ", 6) == 0) {
            char *rest = line + 6;
            char *sp = strchr(rest, ' ');
            if (sp) {
                *sp = 0;
                vfs_write(rest, sp + 1, strlen(sp + 1));
            }
        } else if (strcmp(line, "format") == 0) {
            vfs_format();
            print_string("Disk formatted\n");
        } else if (strcmp(line, "halt") == 0) {
            break;
        } else if (line[0]) {
            print_string("Unknown command\n");
        }
    }
    for (;;) {
        __asm__("hlt");
    }
}
