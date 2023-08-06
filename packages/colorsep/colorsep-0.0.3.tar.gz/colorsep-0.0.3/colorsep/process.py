#!/usr/bin/env python
import click
import copy
import png
from scipy.spatial import distance


WHITE_PIXEL = (255, 255, 255, 255)
BLANK_PIXEL = (0, 0, 0, 0)

pixel_to_file_handle_dict = {}
pixel_rows_list_dict = {}
row_buffers_dict = {}


@click.command()
@click.option("--input", help="input png")
@click.option("--output-base", help="base name of output pngs")
@click.option("--alpha-threshold", default=255, help="on/off threshold for alpha")
@click.option("--num-colors", help="use to set number of output colors")
@click.option("--base-white", is_flag=True, help="should all color be underlaid with white?")
@click.option("--near-pixel-threshold", default=0, help="tolerance for nearest-color computation")
def process_png(input, output_base, alpha_threshold, num_colors, base_white, near_pixel_threshold):

    print("input: {}".format(input))
    print("output_base: {}\n".format(output_base))

    # read png
    png_reader_obj = png.Reader(input)
    png_details = png_reader_obj.read()

    # assemble useful data
    image_width = png_details[0]
    num_colors = int(num_colors)
    alpha_threshold = int(alpha_threshold)
    png_bit_depth = extract_bitdepth(png_details)
    pixel_width = extract_pixel_width_in_num_integers(png_details)
    palette_pixel_list = extract_palette(png_details, num_colors, base_white)

    print("bit depth: {}".format(png_bit_depth))
    print("pixel width: {}".format(pixel_width))
    print("palette pixels: {}".format(palette_pixel_list))
    print("alpha threshold: {}".format(alpha_threshold))

    # init files, data structures
    init_output_filehandles(output_base, palette_pixel_list)
    init_pixel_rows_list_dict(palette_pixel_list)
    init_row_buffers(palette_pixel_list)

    # iterate over pixels and write to row lists
    # print("here")
    png_reader_obj = png.Reader(input)
    png_details = png_reader_obj.read()
    for pixel_ndx, pixel_tuple in enumerate(pixel_tuple_generator(png_details)):

        r, g, b, a = pixel_tuple
        col_ndx = pixel_ndx % image_width

        # if alpha less than the threshold, just write a blank pixel
        if a < alpha_threshold:
            for palette_pixel in palette_pixel_list:
                add_pixel_to_row_buffer(BLANK_PIXEL, palette_pixel)
            add_pixel_to_row_buffer(BLANK_PIXEL, 'combined')

        else:

            # if the color matches one on the palette list, write it to the
            # appropriate row buffer and write blanks to all other row
            # buffers
            pixel = cached_match_pixel_to_pixel_list((r, g, b, 255),
                                                     palette_pixel_list,
                                                     max_distance=near_pixel_threshold)
            if pixel:

                for palette_pixel in palette_pixel_list:

                    # if the current palette pixel is white and base_white is true, add
                    # a white pixel to the white pixel row buffer
                    if pixel_is_white(palette_pixel) and base_white:
                        add_pixel_to_row_buffer(WHITE_PIXEL, palette_pixel)

                        continue

                    # if the current palette pixel is a match for the pixel being tested,
                    # add the pixel to the row buffer associated with that color
                    if palette_pixel == pixel:
                        add_pixel_to_row_buffer(pixel, palette_pixel)

                        continue


                    add_pixel_to_row_buffer(BLANK_PIXEL, palette_pixel)

                add_pixel_to_row_buffer(pixel, 'combined')

            # if the color doesn't match one on the palette list, write
            # blank pixels to all buffers
            else:
                for palette_pixel in palette_pixel_list:
                    add_pixel_to_row_buffer(BLANK_PIXEL, palette_pixel)
                add_pixel_to_row_buffer(BLANK_PIXEL, 'combined')

        if col_ndx == image_width-1:
            flush_row_buffers()

    # write pngs
    for palette_pixel in palette_pixel_list:
        png_writer_obj = png.Writer(png_details[0], png_details[1], **png_details[3])
        png_writer_obj.write(get_output_filehandle(palette_pixel), get_rows_list(palette_pixel))

    png_writer_obj = png.Writer(png_details[0], png_details[1], **png_details[3])
    png_writer_obj.write(get_output_filehandle('combined'), get_rows_list('combined'))

    close_output_files()


def match_pixel_to_pixel_list(pixel, pixel_list, max_distance=0):
    if max_distance == 0:
        if pixel_in_pixel_list(pixel, pixel_list):
            return pixel

    min_dist = None
    min_pixel = None
    alphaless_pixel = tuple(list(pixel)[0:3])

    for test_pixel in pixel_list:
        alphaless_test_pixel = tuple(list(test_pixel)[0:3])
        dist = distance.euclidean(alphaless_pixel, alphaless_test_pixel)
        if min_dist is None or dist < min_dist:
            min_dist = dist
            min_pixel = test_pixel

    if min_dist <= max_distance:
        return min_pixel

    return None

pixel_match_cache = {}
def cached_match_pixel_to_pixel_list(pixel, pixel_list, max_distance=0):
    global pixel_match_cache
    if pixel in pixel_match_cache:
        return pixel_match_cache[pixel]
    ret = match_pixel_to_pixel_list(pixel, pixel_list, max_distance)
    pixel_match_cache[pixel] = ret
    return ret


def pixel_in_pixel_list(pixel, pixel_list):
    return bool(pixel in pixel_list)


def pixel_is_white(pixel):
    return bool(pixel == WHITE_PIXEL)


def clear_all_pixel_row_buffers(palette_pixel_list):
    init_row_buffers(palette_pixel_list)


def get_pixel_row_buffer(palette_pixel):
    return row_buffers_dict[palette_pixel]


def add_pixel_to_row_buffer(pixel_to_add, palette_pixel):
    global row_buffers_dict
    row_buffers_dict[palette_pixel] += list(pixel_to_add)


def init_pixel_rows_list_dict(palette_pixel_list):
    global pixel_rows_list_dict
    print('initializing pixel rows list dict')
    for pixel in palette_pixel_list:
        pixel_rows_list_dict[pixel] = []
    pixel_rows_list_dict['combined'] = []


def flush_row_buffers():
    global pixel_rows_list_dict
    for palette_pixel in pixel_rows_list_dict.keys():
        pixel_rows_list_dict[palette_pixel].append(copy.copy(row_buffers_dict[palette_pixel]))
    clear_all_pixel_row_buffers(list(pixel_rows_list_dict.keys()))


def get_rows_list(palette_pixel):
    return pixel_rows_list_dict[palette_pixel]


def init_row_buffers(palette_pixel_list):
    global row_buffers_dict
    # print('initializing row buffers')
    for pixel in palette_pixel_list:
        row_buffers_dict[pixel] = []
    row_buffers_dict['combined'] = []


def init_output_filehandles(output_base, pixel_list):
    global pixel_to_file_handle_dict

    print('initializing output filehandles')

    for pixel in pixel_list:
        r, g, b, a = pixel
        fn = '{}_{}-{}-{}.png'.format(output_base, r, g, b)
        pixel_to_file_handle_dict[pixel] = open(fn, 'wb')

    pixel_to_file_handle_dict['combined'] = open('{}_combined.png'.format(output_base), 'wb')


def close_output_files():
    for fh in pixel_to_file_handle_dict.values():
        fh.close()


def get_output_filehandle(pixel):
    return pixel_to_file_handle_dict[pixel]


def extract_bitdepth(png):
    return png[3]['bitdepth']


def extract_pixel_width_in_num_integers(png):
    return 4 if png[3]['alpha'] else 3


def pixel_tuple_generator(png):
    pixel_width = extract_pixel_width_in_num_integers(png)
    buf = []
    for row in png[2]:
        # print("row")
        for p_int in row:
            # print("int")
            buf.append(p_int)
            if len(buf) == pixel_width:
                #print("buf: {}".format(buf))
                yield tuple(buf)
                buf = []


def extract_palette(png, num_colors, base_white):
    unique_pixel_color_dict = {}
    image_width = png[0]
    image_height = png[1]
    for pixel_ndx, pixel_tuple in enumerate(pixel_tuple_generator(png)):
        r, g, b, a = pixel_tuple
        if (r, g, b, 255) not in unique_pixel_color_dict:
            unique_pixel_color_dict[(r, g, b, 255)] = 0
        unique_pixel_color_dict[(r, g, b, 255)] += 1

    unique_pixels = list(unique_pixel_color_dict.keys())
    unique_pixels.sort(key=lambda x: unique_pixel_color_dict[x], reverse=True)
    ret = unique_pixels[0:num_colors]

    if base_white and (255, 255, 255, 255) not in ret:
        ret.append((255, 255, 255, 255))

    # make sure white and opaque is always first
    ret.sort(reverse=True)

    return ret


if __name__ == '__main__':
    process_png()

