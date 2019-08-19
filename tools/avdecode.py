# coding: utf-8
# Parsing which ts are pure audio in a given m3u8 network URI,
# which ts are audio and video, and which ts are pure video;
# ffprobe pw
# ffprobe %s  -v quiet -print_format json -show_format -show_streams

import sys, argparse
import ffmpeg, requests
import m3u8


class TsDecode:
    def get_ts_url(self, m3u8_url):
        '''
        Given a string with a m3u8 url, returns a ts url.
        '''
        ts_urls = []

        m3u8_obj = m3u8.load(m3u8_url)
        base_uri = m3u8_obj.base_uri
        ts_list = m3u8_obj.files

        for _ts in ts_list:
            ts_url = base_uri + _ts
            ts_urls.append(ts_url)
        return ts_urls

    def av_decode(self, url):
        '''
        Given a network stream, return a/v result
        '''
        stream_info = ffmpeg.probe(url)
        codec_type = [info['codec_type'] for info in stream_info['streams']]
        # print(codec_type)
        if 'video' in codec_type and 'audio' not in codec_type:
            print(url, '\t', 'pure video')
        elif 'video' not in codec_type and 'audio' in codec_type:
            print(url, '\t', 'pure audio')
        elif 'video' in codec_type and 'audio' in codec_type:
            print(url, '\t', 'audio and video')
        else:
            print('decoding  exception')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Parsing a network stream（hls）')
    parser.add_argument('--url', help='a network stream（hls）')
    args = parser.parse_args()

    if args.url is None:
        print("usage: ffmpegtools.py [-h] [--url URL]")
        print("missing 1 required positional argument: '--url'")
        sys.exit()

    tsdecode = TsDecode()
    ts_urls = tsdecode.get_ts_url(args.url)
    for ts_url in ts_urls:
        tsdecode.av_decode(ts_url)

