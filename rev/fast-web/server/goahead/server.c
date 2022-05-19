#include "goahead.h"

#include <signal.h>
#include <stdio.h>

static int finished = 0;

static void sigHandler(int signo) {
  finished = 1;
}

static void usage() {
  fprintf(stderr, "\n%s Usage:\n\n"
    "  %s [options] documents [IP]:port conf.txt [conf.txt] ...\n\n"
    "    -l, --log logFile:level\n"
    "    -v, --verbose              # --log stdout:2\n\n",
    ME_TITLE, ME_NAME);
  exit(EXIT_FAILURE);
}

extern char verifyPassword(Webs *wp);

int main (int argc, char **argv, char **envp) {
  int argind;
  char *argp;
  for (argind = 1; argind < argc; argind++) {
    argp = argv[argind];
    if (*argp != '-') {
      break;
    } else if (smatch(argp, "--log") || smatch(argp, "-l")) {
      if (argind >= argc) usage();
      logSetPath(argv[++argind]);
    } else if (smatch(argp, "--verbose") || smatch(argp, "-v")) {
      logSetPath("stdout:2");
    }
  }

  if (argind + 2 >= argc) usage();
  char *documents = argv[argind++];
  char *listen = argv[argind++];

  signal(SIGTERM, sigHandler);
  signal(SIGINT, sigHandler);
  signal(SIGPIPE, SIG_IGN);

  websSetPasswordStoreVerify(verifyPassword);

  if (websOpen(documents, NULL) != 0) {
    exit(EXIT_FAILURE);
  }
  if (websListen(listen) < 0) {
    exit(EXIT_FAILURE);
  }
  while (argind < argc) {
    if (websLoad(argv[argind++]) < 0) {
      exit(EXIT_FAILURE);
    }
  }

  websServiceEvents(&finished);
  logmsg(1, "Exiting...");
  websClose();
  return 0;
}
