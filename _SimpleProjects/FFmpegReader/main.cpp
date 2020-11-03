#include "VideoReader/FlowCapture.h"

#include <iostream>

extern "C" {
    #include <libavcodec/avcodec.h>
    #include <libavcodec/version.h>
    #include <libavformat/avformat.h>
    #include <libavutil/old_pix_fmts.h>
    #include <libavutil/pixfmt.h>
    #include <libswscale/swscale.h>
    #include <libavdevice/avdevice.h>
}



int main(int, char**) {
    // FlowCapture _flow_cap("rtsp://121.23.46.168:554/video_1");
    FlowCapture _flow_cap("rtsp://121.23.46.111/onvif/media/PRF08.wxp");
    
    SDL_Init(SDL_INIT_VIDEO);
    SDL_Window *window = SDL_CreateWindow(
        "SDL2Test",
        SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
        640, 480, 0);
    SDL_Renderer *renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_SOFTWARE);
    SDL_SetRenderDrawColor(renderer, 0, 0, 0, SDL_ALPHA_OPAQUE);
    SDL_RenderClear(renderer);
    SDL_RenderPresent(renderer);
    SDL_Delay(3000);
    SDL_DestroyWindow(window);
    SDL_Quit();
    return 0;
}
