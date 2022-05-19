.intel_syntax noprefix

.globl verifyPassword
.globl websLookupUser
.globl sha512_hash

/*
Webs rbx
  ->user 0x310
  ->username 0x280
  ->password 0x230

WebsUser
  ->password 0x8
*/
verifyPassword:
  push rbx
  mov rbx, rdi
  mov rax, QWORD PTR [rbx + 0x310]
  test rax, rax
  jnz verifyPassword.check
  mov rdi, QWORD PTR [rbx + 0x280]
  call websLookupUser
  mov QWORD PTR [rbx + 0x310], rax
  test rax, rax
  jnz verifyPassword.check
verifyPassword.fail:
  xor rax, rax
  jz verifyPassword.return
  call meme
verifyPassword.return:
  pop rbx
  ret
verifyPassword.check:
  mov rdi, QWORD PTR [rbx + 0x230]
  mov rax, QWORD PTR [rbx + 0x310]
  mov rsi, QWORD PTR [rax + 0x8]
  call check
  jz verifyPassword.return
  jnz verifyPassword.return
meme:
.byte 0xe8
/*
password rdi
hash rsi
*/
check:
  push rbp
  mov rbp, rsp
  sub rsp, 0x50
  mov QWORD PTR [rbp - 0x10], 0
  /* strlen */
  xor eax, eax
  xor ecx, ecx
  dec rcx
  repne scasb
  lea rdi, [rdi + rcx + 1]
  sub rax, rcx
  sub rax, 2
  mov rdx, rsp
  push rsi
  sub rsp, 8
  mov rsi, rax
  call sha512_hash
  add rsp, 8
  jz cmphash
  jnz cmphash
  .byte 0xe8
check.done:
  leave
  ret

/*
hex hash r8
bin hash r9
*/
cmphash:
  pop r8
  mov r9, rsp
  /*

  BUG IS HERE
  LOOP SHOULD NOT END WHEN BYTE PTR [r9] == 0
  IF THERE IS A 0 IN THE HASH THEN THIS ONLY COMPARES BEFORE THAT POSITION

  */
  xor eax, eax
  xor edx, edx
cmphash.l1do:
  mov dl, BYTE PTR [r8]
  call parsehex
  mov ax, dx
  inc r8
  mov dl, BYTE PTR [r8]
  call parsehex
  shl ax, 4
  or ax, dx
  inc r8
  mov dl, BYTE PTR [r8]
  call parsehex
  shl ax, 4
  or ax, dx
  inc r8
  mov dl, BYTE PTR [r8]
  call parsehex
  shl ax, 4
  or ax, dx
  inc r8
  cmp WORD PTR [r9], ax
  jz cmphash.l1cmp
  xor eax, eax
  jz cmphash.return
  .byte 0xe8
cmphash.l1cmp:
  add r9, 2
  cmp WORD PTR [r9], 0
  jnz cmphash.l1do
  mov eax, 1
cmphash.return:
  jz check.done
  jnz check.done
  .byte 0xe8

/*
digit dl
*/
parsehex:
  cmp dl, 0x30
  jb parsehex.fail
  cmp dl, 0x40
  jae parsehex.letter
  sub dl, 0x30
  ret
parsehex.letter:
  cmp dl, 0x61
  jb parsehex.fail
  cmp dl, 0x67
  jae parsehex.fail
  sub dl, 0x57
  ret
parsehex.fail:
  mov dl, 0xff
  ret
