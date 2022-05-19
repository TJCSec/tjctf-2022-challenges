#include <emscripten.h>
#include <SDL.h>
#include <iostream>

#include "out.cpp"

using namespace std;

const int width = 32;
const int height = 32;
const int channels = 4;

int currentColor[3];
int brushSize = 10;

Uint8 *pixels;

SDL_Event event;
SDL_Renderer *renderer;
SDL_Window *window;
SDL_Surface *surface;

bool leftMouseButtonDown = false;

extern "C" void EMSCRIPTEN_KEEPALIVE setBrushSize(int radius)
{
    brushSize = radius;
}

extern "C" void EMSCRIPTEN_KEEPALIVE clearCanvas()
{
    memset(pixels, 255, sizeof(Uint8) * width * height * channels);
}

extern "C" void EMSCRIPTEN_KEEPALIVE toggleLeftMouseButtonUp()
{
    leftMouseButtonDown = 0;
}

extern "C" void EMSCRIPTEN_KEEPALIVE toggleLeftMouseButtonDown()
{
    leftMouseButtonDown = 1;
}

extern "C" void EMSCRIPTEN_KEEPALIVE setColor(int r, int g, int b)
{
    currentColor[0] = r;
    currentColor[1] = g;
    currentColor[2] = b;
}

extern "C" void EMSCRIPTEN_KEEPALIVE draw(int mouseX, int mouseY)
{
    if (mouseX < 0 || mouseX >= width || mouseY < 0 || mouseY >= height)
        return;

    if (leftMouseButtonDown)
    {
        for (int i = -brushSize / 2; i <= brushSize / 2; i++)
        {
            for (int j = -brushSize / 2; j <= brushSize / 2; j++)
            {
                int currY = mouseY + i;
                int currX = mouseX + j;

                if (currX < 0 || currX >= width || currY < 0 || currY >= height)
                    continue;

                pixels[4 * (currY * width + currX)] = currentColor[2];
                pixels[4 * (currY * width + currX) + 1] = currentColor[1];
                pixels[4 * (currY * width + currX) + 2] = currentColor[0];
                pixels[4 * (currY * width + currX) + 3] = 255;
            }
        }
        if (checkFlag(pixels, width, height))
        {
            cout << "i spy with my little eye: a flag" << endl;
        }
    }
}

void loop()
{
    if (SDL_MUSTLOCK(surface))
        SDL_LockSurface(surface);

    Uint8 *sPixels = (Uint8 *)surface->pixels;
    memcpy(sPixels, pixels, sizeof(Uint8) * width * height * channels);

    if (SDL_MUSTLOCK(surface))
        SDL_UnlockSurface(surface);

    SDL_Texture *texture = SDL_CreateTextureFromSurface(renderer, surface);

    SDL_RenderClear(renderer);
    SDL_RenderCopy(renderer, texture, NULL, NULL);
    SDL_RenderPresent(renderer);
    SDL_DestroyTexture(texture);
}

int main()
{
    SDL_Init(SDL_INIT_VIDEO);
    SDL_CreateWindowAndRenderer(width, height, 0, &window, &renderer);
    surface = SDL_CreateRGBSurface(0, width, height, 32, 0, 0, 0, 0);

    pixels = new Uint8[width * height * channels];
    clearCanvas();
    emscripten_set_main_loop(loop, 0, true);
}
