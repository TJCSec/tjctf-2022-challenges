#include <stdio.h>
#include <string.h>

#define N 64

const char flag[] = "fxqftiuuus\x7fw`aaaaaaaaa'ao";

int main()
{
    char guess[N];

    puts("What's your flag?");

    fgets(guess, N, stdin);
    size_t len = strlen(guess) - 1;

    if (len != strlen(flag))
    {
        puts("L");
        return 1;
    }

    for (size_t i = 0; i < len; i++)
    {
        if ((guess[i] ^ flag[i]) != 0x12)
        {
            puts("L");
            return 1;
        }
    }
    puts("W");
}
