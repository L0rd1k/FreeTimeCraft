#include "FlowCapture.h"

FlowCapture::FlowCapture(const char *filename)
{
    av_register_all(); // register all codecs and file formats
    SDL_Init(SDL_INIT_VIDEO);
    avformat_network_init();
    this->filename = filename;
    mainExecutor();
}

int FlowCapture::mainExecutor()
{
    openFileReader();
    retrieveStreamInfo();
    getFileInformation();
    if (findFirstVideoStream())
    {
        std::cout << "Stream was found!" << std::endl;
        if (findDecoderAndOpenCodec())
        {
            if (dataStorage() == -1)
                return -1;
            if (dataRead() == -1)
                return -1;
        }
    }
}

int FlowCapture::dataRead()
{
    sws_ctx = sws_getContext(
        pCodecCtx->width,
        pCodecCtx->height,
        pCodecCtx->pix_fmt,
        pCodecCtx->width,
        pCodecCtx->height,
        PIX_FMT_RGB24,
        SWS_BILINEAR,
        NULL,
        NULL,
        NULL);
    videoStreamIndex = 0;
    while (av_read_frame(av_format_context, &packet) >= 0)
    {
        if (packet.stream_index == videoStream)
        {
            avcodec_decode_video2(pCodecCtx, pFrame, &frameFinished, &packet);
            if (frameFinished) // if we have next frame
            {
                sws_scale(sws_ctx, (uint8_t const *const *)pFrame->data,
                          pFrame->linesize, 0, pCodecCtx->height,
                          pFrameRGB->data, pFrameRGB->linesize);
                if (++videoStreamIndex <= 5)
                {
                    saveFrame(pFrameRGB, pCodecCtx->width, pCodecCtx->height, videoStreamIndex);
                }
            }
        }
        av_free_packet(&packet);
    }
}

void FlowCapture::saveFrame(AVFrame *pFrame, int width, int height, int iFrame)
{
    char sizeFileName[32];
    int y;

    sprintf(sizeFileName, "frame%d.ppm", iFrame);
    FILE *pFile = fopen(sizeFileName, "wb");
    if (pFile == NULL)
        return;
    fprintf(pFile, "P6\n%d %d\n255\n", width, height);
    for (y = 0; y < height; y++)
        fwrite(pFrame->data[0] + y * pFrame->linesize[0], 1, width * 3, pFile);
    fclose(pFile);
}

int FlowCapture::dataStorage()
{
    pFrame = av_frame_alloc();
    pFrameRGB = av_frame_alloc();
    if (pFrameRGB == NULL)
    {
        std::cout << "Failed to allocate RGB frame!" << std::endl;
        return -1;
    }

    screen = SDL_CreateWindow( // [2]
        "SDL Video Player",
        SDL_WINDOWPOS_UNDEFINED,
        SDL_WINDOWPOS_UNDEFINED,
        pCodecCtx->width / 2,
        pCodecCtx->height / 2,
        SDL_WINDOW_OPENGL | SDL_WINDOW_ALLOW_HIGHDPI);

    if(!screen) {
        std::cout << "SDL:Can't set video mode!" << std::endl; 
        return -1;
    }

    int numBytes;
    numBytes = avpicture_get_size(PIX_FMT_RGB24, pCodecCtx->width, pCodecCtx->height);
    buffer = (uint8_t *)av_malloc(numBytes * sizeof(uint8_t));
    std::cout << "Number of bytes: " << numBytes << std::endl;
    avpicture_fill((AVPicture *)pFrameRGB, buffer, PIX_FMT_RGB24, pCodecCtx->width, pCodecCtx->height);
}

bool FlowCapture::findDecoderAndOpenCodec()
{
    pCodec = avcodec_find_decoder(pCodecCtx->codec_id);
    if (pCodec == NULL)
    {
        std::cout << "Unsupported coded!" << std::endl;
        return false;
    }
    pCodecCtx = avcodec_alloc_context3(pCodec);
    if (avcodec_copy_context(pCodecCtx, av_format_context->streams[videoStreamIndex]->codec) != 0)
    {
        std::cout << "Couldn't copy codec context!" << std::endl;
        return false;
    }
    if (avcodec_open2(pCodecCtx, pCodec, nullptr) < 0)
    {
        std::cout << "Can't open codec!" << std::endl;
        return false;
    }
    return true;
}

bool FlowCapture::openFileReader()
{
    av_format_context = avformat_alloc_context();
    if (avformat_open_input(&av_format_context, filename, NULL, NULL) != 0)
    {
        std::cerr << "Error: Can't open input file (AVFormatContext wasn't created)!\n";
        return false;
    }
}

bool FlowCapture::retrieveStreamInfo()
{
    if (avformat_find_stream_info(av_format_context, NULL) < 0)
    {
        std::cerr << "Error: Can't find stream info!\n";
        return false;
    }
}

void FlowCapture::getFileInformation()
{
    av_dump_format(av_format_context, 0, filename, 0);
}

bool FlowCapture::findFirstVideoStream()
{
    for (videoStreamIndex = 0; videoStreamIndex < av_format_context->nb_streams; videoStreamIndex++)
    {
        if (av_format_context->streams[videoStreamIndex]->codec->codec_type == AVMEDIA_TYPE_VIDEO)
        {
            videoStream = videoStreamIndex;
            break;
        }
    }
    if (videoStream == -1)
    {
        std::cerr << "Error: Unable to find valid video stream\n";
        return false;
    }
    pCodecCtx = av_format_context->streams[videoStream]->codec;
    return true;
}

FlowCapture::~FlowCapture()
{
    av_free(buffer);
    av_free(pFrameRGB);
    av_free(pFrame);

    avcodec_close(pCodecCtx);
    avcodec_close(pCodecCtxOrig);
    avformat_close_input(&av_format_context);
}
