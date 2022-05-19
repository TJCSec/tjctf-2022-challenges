#include <openssl/sha.h>
#include <signal.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/prctl.h>
#include <sys/sysinfo.h>
#include <sys/time.h>
#include <sys/wait.h>
#include <unistd.h>

#define CHAR_START ' '
#define CHAR_END '~'
#define STAT_INT 5

#define min(a,b)             \
({                           \
    __typeof__ (a) _a = (a); \
    __typeof__ (b) _b = (b); \
    _a < _b ? _a : _b;       \
})

char hash[SHA512_DIGEST_LENGTH] = {0};
volatile uint64_t hashes = 0;

void show_status(int sig) {
  // take these with a grain of salt
  fprintf(stderr, "[ %d ] %f MH/s\n", getpid(), (double) hashes / (STAT_INT * 1000000));
  hashes = 0;
}

void set_status_timer() {
  struct itimerval timer;

  timer.it_interval.tv_usec = 0;
  timer.it_interval.tv_sec = STAT_INT;
  timer.it_value.tv_usec = 0;
  timer.it_value.tv_sec = STAT_INT;

  signal(SIGALRM, show_status);
  setitimer(ITIMER_REAL, &timer, NULL);
}

void bash_recur(char *s, char *p, size_t len, size_t rem, char start, char end) {
  // duplicated code for 1% more performance :slight_smile:
  if (rem == 1) {
    // this is the last character to bash, so we're going to compute hashes
    for (char c = start; c <= end; c++) {
      *p = c;
      SHA512(s, len, hash);
      hashes++;
      // if hash matches target, we're done
      if (((uint32_t *) hash)[1] == 0xb8e80000) {
        fprintf(stderr, "FOUND: \"%.*s\"\n", (int) len, s);
        printf("%.*s", (int) len, s);
        fflush(stdout);
        _exit(EXIT_SUCCESS);
      }
    }
  } else {
    // we have more characters to bash, so we're going to recurse
    for (char c = start; c <= end; c++) {
      *p = c;
      bash_recur(s, p + 1, len, rem - 1, CHAR_START, CHAR_END);
    }
  }
}

void bash(char *buf, size_t len, int procs) {
  char perproc = ((CHAR_END - CHAR_START) / procs) + 1;
  pid_t pid = 0;
  pid_t child_pgid = 0;

  // create processes
  for (int i = 0; i < procs; i++) {
    // process will try this range of characters as the first one
    char start = (char) (i * perproc) + CHAR_START;
    char end = min(start - 1 + perproc, CHAR_END);
    pid = fork();

    if (pid == 0) {
      prctl(PR_SET_PDEATHSIG, SIGTERM);
      if (len > 3) {
        set_status_timer();
      }
      // do bashing
      bash_recur(buf, buf, len, len, start, end);
      // if we are still here, then bashing did not find a solution
      _exit(EXIT_FAILURE);
    }

    if (!child_pgid) {
      child_pgid = pid;
    }
    setpgid(pid, child_pgid);
  }

  // wait for children to finish bashing
  int wstatus = 0;
  while ((pid = waitpid(-child_pgid, &wstatus, 0)) > 0) {
    if (WIFEXITED(wstatus)) {
      if (WEXITSTATUS(wstatus) == EXIT_SUCCESS) {
        // done!
        exit(EXIT_SUCCESS);
      }
    }
  }
}

int main(void) {
  char buf[64];
  int procs = get_nprocs();

  fprintf(stderr, "Using %d processes\n", procs);
  for (size_t len = 1; len <= sizeof(buf); len++) {
    fprintf(stderr, "Trying length: %zu\n", len);
    bash(buf, len, procs);
  }
}
