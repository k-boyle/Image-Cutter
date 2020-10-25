#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image, GifImagePlugin
import sys


def get_right_corner(left_corner_x, left_corner_y, width, height, max_width, max_height):
    righ_corner_x = min (left_corner_x + width, max_width)
    right_corner_y = min (left_corner_y + height, max_height)
    return (righ_corner_x, right_corner_y)


def chunk_frame(frame, hor_chunks, ver_chunks):
    width, height = frame.size
    chunk_width = int (width / hor_chunks)
    chunk_height = int (height / ver_chunks)

    chunks = []
    for x in range (hor_chunks):
        for y in range (ver_chunks):
            left_corner_x = x * chunk_width
            left_corner_y = y * chunk_height
            right_corner_x, right_corner_y = get_right_corner (left_corner_x, left_corner_y, chunk_width, chunk_height, width, height)

            print (f'processing chunk: ({x}, {y}) from ({left_corner_x}, {left_corner_y}) to ({right_corner_x}, {right_corner_y})')

            chunk = frame.crop((left_corner_x, left_corner_y, right_corner_x, right_corner_y))
            chunks.append (chunk)

    return chunks


args = sys.argv

if len (args) != 4:
    raise Exception ('usage: ./image_cutter.py image horizontal_chunks vertical_chunks')

image = Image.open(args[1])
hor_chunks = int (args[2])
ver_chunks = int (args[3])

number_of_frames = image.n_frames
print (f'number of frames: {number_of_frames}')

chunked_frames = []
for i in range (0, number_of_frames):
    print (f'processing frame: {i}')

    image.seek(i)
    chunked_frame = chunk_frame (image, hor_chunks, ver_chunks)
    chunked_frames.append (chunked_frame)

images = zip (*chunked_frames)
image_format = args[1][-3:]

image_index = 0
for frames in images:
    first_frame = frames[0]
    # bug with Pillow removing duplicate frames, this is hack for 2 frame images
    first_frame.putpixel ((0, 0), 0)
    first_frame.save (f'{image_index}.{image_format}', save_all=True, append_images=frames[1:], optimize=False, loop=0)
    image_index += 1
