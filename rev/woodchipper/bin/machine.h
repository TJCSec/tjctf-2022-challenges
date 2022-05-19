#include <stdint.h>
#include <stdbool.h>

#define CS_SIZE 0x400
#define MEM_SIZE 0x4000

#define INS_OPC(ins)  ((ins & 0b0000000000011111) >> 0)   // opcode
#define INS_OPN(ins)  ((ins & 0b0000000001100000) >> 5)   // operand number
#define INS_OPT(ins)  ((ins & 0b0000011110000000) >> 7)   // operand types
#define INS_REG(ins)  ((ins & 0b0111100000000000) >> 11)  // register select

#define OPT_IMM(opt)  ((opt & 0b01) >> 0)   // imm operand (else register)
#define OPT_MEM(opt)  ((opt & 0b10) >> 1)   // dereference memory

#define REG_GET(reg)  (reg & 0b11)

typedef struct VMState {
  uint16_t pc;
  uint16_t *cs;
  uint16_t *mem;
  bool cmp;
  uint16_t reg[4];
} VMState;

typedef int (*Ins)(VMState* state, uint8_t opn, uint16_t **ops);

typedef struct InsNode {
  Ins func;
  struct InsNode *left;
  struct InsNode *right;
} InsNode;
