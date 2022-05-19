#define _GNU_SOURCE

#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>

void main() {
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  setbuf(stderr, NULL);

  puts("the New England special!");

  unsigned char *buf = mmap(NULL, 0x1000, PROT_EXEC | PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANON, -1, 0);
  int len = read(STDIN_FILENO, buf, 0x1000);
  for (int i = 0; i < len; i++) {
    if (buf[i] < '0' || buf[i] > '~') {
      puts("yuck!");
      return;
    }
  }

  puts("yummy!");
  strfry(buf);
  goto *buf;
}
