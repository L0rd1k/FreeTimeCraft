#ifndef FLOWCAPTURE_H
#define FLOWCAPTURE_H

#include <iostream>
#include <string>
#include "SDL.h"
#include "SDL_thread.h"

extern "C" {
    #include <libavcodec/avcodec.h>
    #include <libavcodec/version.h>
    #include <libavformat/avformat.h>
    #include <libavutil/old_pix_fmts.h>
    #include <libavutil/pixfmt.h>
    #include <libswscale/swscale.h>
}


class FlowCapture {
public:
    FlowCapture();
    FlowCapture(const char* filename);
    virtual ~FlowCapture();
private:
    bool openFileReader(); // open video file
    bool retrieveStreamInfo();
    void getFileInformation();
    bool findFirstVideoStream();
    bool findDecoderAndOpenCodec();
    int dataStorage();
    int dataRead();
    void saveFrame(AVFrame *pFrame, int width, int height, int iFrame);
    int mainExecutor();

private:
    AVFormatContext *av_format_context = nullptr;
    const char* filename;
    int videoStreamIndex;
    int videoStream = -1;
    AVCodecContext *pCodecCtxOrig = NULL;
    AVCodecContext *pCodecCtx = NULL;
    AVCodec *pCodec = NULL;
    AVFrame *pFrame = NULL;
    AVFrame *pFrameRGB = NULL;
private:
    struct SwsContext *sws_ctx = NULL;
    int frameFinished;
    AVPacket packet;
    uint8_t *buffer = NULL;
private:
    SDL_Window *screen = NULL;
};

#endif /* FLOWCAPTURE_H */