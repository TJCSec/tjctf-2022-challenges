#include "machine.h"
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

extern InsNode *init_tree();
InsNode *tree;

void init() {
  setbuf(stdout, NULL);
  setbuf(stderr, NULL);
  tree = init_tree();
}

Ins get_ins(uint8_t x) {
  InsNode *p = tree;
  for (int i = 0; i < 5; i++) {
    if (p == NULL) return NULL;
    if ((x >> i) & 1) {
      p = p->right;
    } else {
      p = p->left;
    }
  }
  return p->func;
}

int run_vm(VMState *state) {
  Ins func;
  uint16_t ins;
  uint8_t opn, opt, reg;
  uint16_t imm[2];
  uint16_t *ops[2];
  int ret;

  while (1) {
    if (state->pc >= MEM_SIZE) return -1;
    ins = state->mem[state->pc++];
    if ((func = get_ins(INS_OPC(ins))) == NULL) return -1;
    if ((opn = INS_OPN(ins)) > 2) return -1;
    opt = INS_OPT(ins);
    reg = INS_REG(ins);
    for (int i = 0; i < opn; i++) {
      if (OPT_IMM(opt)) {
        // imm
        if (state->pc >= MEM_SIZE) return -1;
        imm[i] = state->mem[state->pc++];
        ops[i] = &imm[i];
      } else {
        // reg
        ops[i] = &state->reg[REG_GET(reg)];
      }
      if (OPT_MEM(opt)) {
        // mem
        if (*ops[i] >= MEM_SIZE) return -1;
        ops[i] = &state->mem[*ops[i]];
      }
      reg >>= 2;
      opt >>= 2;
    }
    ret = func(state, opn, ops);
    if (ret >= 0) return ret;
    if (ret != -1) return -1;
  }
}

int main(int argc, char *argv[]) {
  init();

  if (argc < 2) {
    fprintf(stderr, "no code!\n");
    exit(EXIT_FAILURE);
  }

  VMState *state = calloc(1, sizeof(VMState));
  state->cs = calloc(CS_SIZE, sizeof(uint16_t));
  state->mem = calloc(MEM_SIZE, sizeof(uint16_t));
  if (state->cs == NULL || state->mem == NULL) {
    perror("calloc");
    exit(EXIT_FAILURE);
  }

  // underflow guard
  *state->cs = 0xffff;

  FILE *f = fopen(argv[1], "r");
  if (f == NULL) {
    perror("fopen");
    exit(EXIT_FAILURE);
  }

  fread(state->mem, MEM_SIZE, sizeof(uint16_t), f);
  fclose(f);

  int ret = run_vm(state);
  return ret;
}
