# -*- coding: utf-8 -*-
import argparse
import logging
import random
import sys

def read_m3u(fp):
    logger = logging.getLogger(__name__)
    num_items = 0
    extinf = None
    for line in fp:
        if not line.strip() or line == '#EXTM3U':
            continue
        elif line.startswith('#EXTINF:'):
            extinf = line
        else:
            item = (extinf, line)
            num_items += 1
            logger.debug('Read M3U item %d: %r', num_items, item)
            yield item
            extinf = None
    logger.info('%d items read from M3U playlist', num_items)


def write_m3u(fp, playlist):
    logger = logging.getLogger(__name__)
    num_items = 0
    extinf = None
    fp.write('#EXTM3U\n')
    for item in playlist:
        for line in item:
            if line:
                fp.write(line)
        num_items += 1
        logger.debug('Wrote M3U item %d: %r', num_items, item)
    logger.info('%d items written to M3U playlist', num_items)


def shuffle_m3u(input_fp, output_fp, seed=None):
    random.seed(seed)
    playlist = list(read_m3u(input_fp))
    random.shuffle(playlist)
    write_m3u(output_fp, playlist)


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=argparse.FileType(mode='r'),
            help='The M3U playlist to randomize')
    parser.add_argument('-o', '--output-file',
            type=argparse.FileType(mode='w'), default=sys.stdout,
            help='The M3U output file to write to')
    parser.add_argument('-d', '--debug', action='store_true',
            help='Show debug messages')
    parser.add_argument('-s', '--seed', type=int, default=None,
            help='Use a specific seed for the randomness generator')
    pargs = parser.parse_args(args)

    logging.basicConfig(level=logging.DEBUG if pargs.debug else
            logging.INFO)

    return shuffle_m3u(pargs.input_file, pargs.output_file, seed=pargs.seed)
