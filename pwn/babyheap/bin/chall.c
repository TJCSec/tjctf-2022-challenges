#include <errno.h>
#include <seccomp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/random.h>
#include <sys/mman.h>
#include <unistd.h>

#define NUM_SLOTS 16
#define MAX_SIZE 0x2000

char *menu =
"MENU:\n"
"1: malloc\n"
"2: free\n"
"3: view\n"
"4: exit\n"
"choice? ";

typedef struct slot_t {
  size_t size;
  char *buf;
} Slot;

Slot *slots[NUM_SLOTS];

int input(char *s, int size) {
  int rv = read(STDIN_FILENO, s, size);
  if (rv < 0) exit(EXIT_FAILURE);
  return rv;
}

int printn(char *s, int size) {
  int rv = write(STDOUT_FILENO, s, size);
  if (rv < 0) exit(EXIT_FAILURE);
  return rv;
}

int print(char *s) {
  return printn(s, strlen(s));
}

void __attribute__((constructor)) init() {
  scmp_filter_ctx ctx;
  if ((ctx = seccomp_init(SCMP_ACT_KILL)) == NULL) {
    exit(EXIT_FAILURE);
  }
  int ret = 0;
  ret |= seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);
  ret |= seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
  ret |= seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
  ret |= seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(brk), 0);
  ret |= seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(mmap), 0);
  ret |= seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(munmap), 0);
  ret |= seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(madvise), 0);
  ret |= seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
  ret |= seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);
  ret |= seccomp_load(ctx);
  seccomp_release(ctx);
  if (ret) {
    exit(EXIT_FAILURE);
  }
}

int get_number(unsigned long long *num) {
  char buf[32] = {0};
  input(buf, sizeof(buf));
  char *endptr;
  unsigned long long x = strtoull(buf, &endptr, 10);
  if (errno == ERANGE || buf == endptr) {
    return -1;
  }
  *num = x;
  return 0;
}

void do_malloc() {
  unsigned long long idx = 0;
  unsigned long long size = 0;
  print("idx? ");
  if (get_number(&idx) != 0 || idx > NUM_SLOTS) {
    print("???\n");
    return;
  }
  print("size? ");
  if (get_number(&size) != 0 || size > MAX_SIZE) {
    print("too big!\n");
    return;
  }
  slots[idx] = malloc(sizeof(Slot));
  slots[idx]->buf = malloc(size);
  print("content? ");
  slots[idx]->size = input(slots[idx]->buf, size);
}

void do_free() {
  unsigned long long idx = 0;
  print("idx? ");
  if (get_number(&idx) != 0 || idx > NUM_SLOTS || slots[idx] == NULL) {
    print("???\n");
    return;
  }
  free(slots[idx]->buf);
  free(slots[idx]);
}

void do_view() {
  unsigned long long idx = 0;
  print("idx? ");
  if (get_number(&idx) != 0 || idx > NUM_SLOTS || slots[idx] == NULL) {
    print("???\n");
    return;
  }
  printn(slots[idx]->buf, slots[idx]->size);
}

void main() {
  unsigned long long choice;
  while (1) {
    print(menu);
    if (get_number(&choice) != 0) {
      print("wat\n");
    } else {
      switch (choice) {
        case 1:
          do_malloc();
          break;
        case 2:
          do_free();
          break;
        case 3:
          do_view();
          break;
        case 4:
          return;
        default:
          print("wat\n");
      }
    }
    print("\n");
  }
}
