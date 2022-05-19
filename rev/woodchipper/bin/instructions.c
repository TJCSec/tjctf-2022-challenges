#include "machine.h"
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/syscall.h>

// special stuff
#define S_exit 0
#define S_read 1
#define S_write 2
#define S_open 3
#define S_close 4

int add(VMState *state, uint8_t opn, uint16_t **ops) {
  if (opn != 2) return -2;
  *ops[0] += *ops[1];
  return -1;
}

int sub(VMState *state, uint8_t opn, uint16_t **ops) {
  if (opn != 2) return -2;
  *ops[0] -= *ops[1];
  return -1;
}

int mul(VMState *state, uint8_t opn, uint16_t **ops) {
  if (opn != 2) return -2;
  *ops[0] *= *ops[1];
  return -1;
}

int idiv(VMState *state, uint8_t opn, uint16_t **ops) {
  if (opn != 2) return -2;
  *ops[0] /= *ops[1];
  return -1;
}

int shl(VMState *state, uint8_t opn, uint16_t **ops) {
  if (opn != 2) return -2;
  *ops[0] <<= *ops[1];
  return -1;
}

int shr(VMState *state, uint8_t opn, uint16_t **ops) {
  if (opn != 2) return -2;
  *ops[0] >>= *ops[1];
  return -1;
}

int rol(VMState *state, uint8_t opn, uint16_t **ops) {
  if (opn != 2) return -2;
  uint16_t val = *ops[0];
  uint16_t shift = *ops[1] % 16;
  if (shift == 0) return -1;
  *ops[0] = (val << shift) | (val >> (16 - shift));
  return -1;
}

int ror(VMState *state, uint8_t opn, uint16_t **ops) {
  if (opn != 2) return -2;
  uint16_t val = *ops[0];
  uint16_t shift = *ops[1] % 16;
  if (shift == 0) return -1;
  *ops[0] = (val >> shift) | (val << (16 - shift));
  return -1;
}

int and(VMState *state, uint8_t opn, uint16_t **ops) {
  if (opn != 2) return -2;
  *ops[0] &= *ops[1];
  return -1;
}

int or(VMState *state, uint8_t opn, uint16_t **ops) {
  if (opn != 2) return -2;
  *ops[0] |= *ops[1];
  return -1;
}

int xor(VMState *state, uint8_t opn, uint16_t **ops) {
  if (opn != 2) return -2;
  *ops[0] ^= *ops[1];
  return -1;
}

int not(VMState *state, uint8_t opn, uint16_t **ops) {
  if (opn != 1) return -2;
  *ops[0] = ~(*ops[0]);
  return -1;
}

int clt(VMState *state, uint8_t opn, uint16_t **ops) {
  if (opn != 2) return -2;
  state->cmp = (*ops[0] < *ops[1]);
  return -1;
}

int cle(VMState *state, uint8_t opn, uint16_t **ops) {
  if (opn != 2) return -2;
  state->cmp = (*ops[0] <= *ops[1]);
  return -1;
}

int cgt(VMState *state, uint8_t opn, uint16_t **ops) {
  if (opn != 2) return -2;
  state->cmp = (*ops[0] > *ops[1]);
  return -1;
}

int cge(VMState *state, uint8_t opn, uint16_t **ops) {
  if (opn != 2) return -2;
  state->cmp = (*ops[0] >= *ops[1]);
  return -1;
}

int cet(VMState *state, uint8_t opn, uint16_t **ops) {
  if (opn != 2) return -2;
  state->cmp = (*ops[0] == *ops[1]);
  return -1;
}

int jmp(VMState *state, uint8_t opn, uint16_t **ops) {
  if (opn != 1) return -2;
  state->pc = *ops[0];
  return -1;
}

int jpt(VMState *state, uint8_t opn, uint16_t **ops) {
  if (opn != 1) return -2;
  if (state->cmp) state->pc = *ops[0];
  return -1;
}

int jpf(VMState *state, uint8_t opn, uint16_t **ops) {
  if (opn != 1) return -2;
  if (!state->cmp) state->pc = *ops[0];
  return -1;
}

int mov(VMState *state, uint8_t opn, uint16_t **ops) {
  if (opn != 2) return -2;
  *ops[0] = *ops[1];
  return -1;
}

int cal(VMState *state, uint8_t opn, uint16_t **ops) {
  if (opn != 1) return -2;
  *++state->cs = state->pc;
  state->pc = *ops[0];
  return -1;
}

int ret(VMState *state, uint8_t opn, uint16_t **ops) {
  if (opn != 0) return -2;
  state->pc = *state->cs--;
  return -1;
}

int sys(VMState *state, uint8_t opn, uint16_t **ops) {
  if (opn != 1) return -2;
  switch (*ops[0]) {
    case S_exit:
      return (int) state->reg[1];
    case S_read:
      state->reg[0] = (uint16_t) syscall(SYS_read, state->reg[1], &state->mem[state->reg[2]], state->reg[3]);
      break;
    case S_write:
      state->reg[0] = (uint16_t) syscall(SYS_write, state->reg[1], &state->mem[state->reg[2]], state->reg[3]);
      break;
    case S_open:
      state->reg[0] = (uint16_t) syscall(SYS_open, &state->mem[state->reg[1]], state->reg[2], state->reg[3]);
      break;
    case S_close:
      state->reg[0] = (uint16_t) syscall(SYS_close, state->reg[1]);
      break;
    default:
      return -2;
  }
  return -1;
}

InsNode *init_tree() {
  // this is unbelievably cursed; I should probably learn how to not do this

  #define null_node NULL
  #define ALLOC_NODE(NAME) InsNode *NAME = calloc(1, sizeof(InsNode)); if (NAME == NULL) { perror("calloc"); exit(EXIT_FAILURE); }
  #define MAKE_NODE(INST) ALLOC_NODE(INST##_node); INST##_node->func = INST;
  #define LINK_NODE(NEW, LEFT, RIGHT) ALLOC_NODE(NEW##_node); NEW##_node->left = LEFT##_node; NEW##_node->right = RIGHT##_node;

  MAKE_NODE(add) MAKE_NODE(sub) MAKE_NODE(mul) MAKE_NODE(idiv)
  MAKE_NODE(shl) MAKE_NODE(shr) MAKE_NODE(rol) MAKE_NODE(ror)
  MAKE_NODE(and) MAKE_NODE(or)  MAKE_NODE(xor) MAKE_NODE(not)
  MAKE_NODE(clt) MAKE_NODE(cle) MAKE_NODE(cgt) MAKE_NODE(cge)
  MAKE_NODE(cet) MAKE_NODE(jmp) MAKE_NODE(jpt) MAKE_NODE(jpf)
  MAKE_NODE(mov) MAKE_NODE(sys) MAKE_NODE(cal) MAKE_NODE(ret)

  LINK_NODE(addsub, add, sub) LINK_NODE(muldiv, mul, idiv)
  LINK_NODE(shlshr, shl, shr) LINK_NODE(rolror, rol, ror)
  LINK_NODE(andor, and, or)   LINK_NODE(xornot, xor, not)
  LINK_NODE(cltcle, clt, cle) LINK_NODE(cgtcge, cgt, cge)
  LINK_NODE(cetjmp, cet, jmp) LINK_NODE(jptjpf, jpt, jpf)
  LINK_NODE(movsys, mov, sys) LINK_NODE(calret, cal, ret)

  LINK_NODE(arith, addsub, muldiv)
  LINK_NODE(shift, shlshr, rolror)
  LINK_NODE(bitwise, andor, xornot)
  LINK_NODE(compare, cltcle, cgtcge)
  LINK_NODE(jump, cetjmp, jptjpf)
  LINK_NODE(special, movsys, calret)

  LINK_NODE(num, arith, shift)
  LINK_NODE(bit, bitwise, null)
  LINK_NODE(branch, compare, jump)
  LINK_NODE(misc, special, null)

  LINK_NODE(left, num, bit) LINK_NODE(right, branch, misc)
  LINK_NODE(root, left, right)

  return root_node;
}
