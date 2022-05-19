/*
 * SHA-512 hash in C and x86 assembly
 *
 * Copyright (c) 2021 Project Nayuki. (MIT License)
 * https://www.nayuki.io/page/fast-sha2-hashes-in-x86-assembly
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of
 * this software and associated documentation files (the "Software"), to deal in
 * the Software without restriction, including without limitation the rights to
 * use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 * the Software, and to permit persons to whom the Software is furnished to do so,
 * subject to the following conditions:
 * - The above copyright notice and this permission notice shall be included in
 *   all copies or substantial portions of the Software.
 * - The Software is provided "as is", without warranty of any kind, express or
 *   implied, including but not limited to the warranties of merchantability,
 *   fitness for a particular purpose and noninfringement. In no event shall the
 *   authors or copyright holders be liable for any claim, damages or other
 *   liability, whether in an action of contract, tort or otherwise, arising from,
 *   out of or in connection with the Software or the use or other dealings in the
 *   Software.
 */

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>


/* Function prototypes */

#define BLOCK_LEN 128  // In bytes
#define STATE_LEN 8  // In words

static bool self_check(void);
void sha512_hash(const uint8_t message[], size_t len, uint64_t hash[static STATE_LEN]);

// Link this program with an external C or x86 compression function
extern void sha512_compress(const uint8_t block[static BLOCK_LEN], uint64_t state[static STATE_LEN]);

/* Full message hasher */

void sha512_hash(const uint8_t message[], size_t len, uint64_t hash[static STATE_LEN]) {
	hash[0] = UINT64_C(0x6A09E667F3BCC908);
	hash[1] = UINT64_C(0xBB67AE8584CAA73B);
	hash[2] = UINT64_C(0x3C6EF372FE94F82B);
	hash[3] = UINT64_C(0xA54FF53A5F1D36F1);
	hash[4] = UINT64_C(0x510E527FADE682D1);
	hash[5] = UINT64_C(0x9B05688C2B3E6C1F);
	hash[6] = UINT64_C(0x1F83D9ABFB41BD6B);
	hash[7] = UINT64_C(0x5BE0CD19137E2179);

	#define LENGTH_SIZE 16  // In bytes

	size_t off;
	for (off = 0; len - off >= BLOCK_LEN; off += BLOCK_LEN)
		sha512_compress(&message[off], hash);

	uint8_t block[BLOCK_LEN] = {0};
	size_t rem = len - off;
	if (rem > 0)
		memcpy(block, &message[off], rem);

	block[rem] = 0x80;
	rem++;
	if (BLOCK_LEN - rem < LENGTH_SIZE) {
		sha512_compress(block, hash);
		memset(block, 0, sizeof(block));
	}

	block[BLOCK_LEN - 1] = (uint8_t)((len & 0x1FU) << 3);
	len >>= 5;
	for (int i = 1; i < LENGTH_SIZE; i++, len >>= 8)
		block[BLOCK_LEN - 1 - i] = (uint8_t)(len & 0xFFU);
	sha512_compress(block, hash);
}
