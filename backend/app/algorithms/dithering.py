from typing import List, Tuple, Any

from PIL.Image import Image as PILImage

def brace_to_255(rgb_value):

    if rgb_value < 0:
        return 0
    elif rgb_value > 255:
        return 255
    return rgb_value

def find_nearest_color(pixel, palette):

    red, green, blue = pixel

    nearest_color = None
    smallest_distance = float('inf')

    #Euclidean distance = sqrt((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2)

    for palette_red, palette_green, palette_blue in palette:

        distance = (
                (red - palette_red) ** 2 +
                (green - palette_green) ** 2 +
                (blue - palette_blue) ** 2
                ) ** 0.5

        if distance < smallest_distance:
            
            smallest_distance = distance
            nearest_neighbor = (palette_red, palette_green, palette_green)

    return nearest_color

#quantization
#error diffusion

def floyd_steinberg_dithering_algo(image, palette):

    image = image.convert('RGB')

    width, height = image.size

    pixels = [] #outer array
    for y in range(height):
        row = [] #inner array
        for x in range(width):
            pixels = image.getpixel((x,y))

            row.append(list(pixel))

        pixels.append(row)

    output_img = image.new('RGB', (width, height))

    for y in range(height):
        for x in range(width):

            old_pixel = tuple(pixel)

            new_pixel = find_nearest_color(old_pixel, palette)

            output_img.putpixel((x,y), new_pixel)

            e_red = old_pixel[0] - new_pixel[0]
            e_green = old_pixel[1] - new_pixel[1]
            e_blue = old_pixel[2] - new_pixel[2]

            #in-place update

            if x + 1 < width: 
                pixels[y][x+1][0] = brace_to_255(
                        pixels[y][x+1][0] + 
                        e_red * 7/16
                        )

                pixels[y][x+1][1] = brace_to_255(
                        pixels[y][x+1][1] + 
                        e_green * 7/16
                        )

                pixels[y][x+1][2] = brace_to_255(
                        pixels[y][x+1][2] + 
                        e_blue * 7/16
                        )

            if x - 1 >= 0 and y + 1 < height:
                pixels[y+1][x-1][0] = brace_to_255(
                        pixels[y+1][x-1][0] +
                        e_red * 3/16
                        )

                pixels[y+1][x-1][1] = brace_to_255(
                        pixels[y+1][x-1][1] +
                        e_green * 3/16
                )

                pixels[y+1][x-1][2] = brace_to_255(
                        pixels[y+1][x-1][2] +
                        e_blue * 3/16
                        )

            if y + 1 < height:                
                pixels[y+1][0] = brace_to_255(
                        pixels[y+1][0] +
                        e_red * 5/16
                        )

                pixels[y+1][1] = brace_to_255(
                        pixels[y+1][1] +
                        e_green * 5/16
                        )

                pixels[y+1][2] = brace_to_255(
                        pixels[y+1][2] +
                        e_blue * 5/16
                        )

            if x + 1 < width and y + 1 < height:
                pixels[y+1][x+1][0] = brace_to_255(
                        pixels[y+1][x+1][0] +
                        e_red * 1/16
                        )
                
                pixels[y+1][x+1][1] = brace_to_255(
                        pixels[y+1][x+1][1] +
                        e_green * 1/16
                        )

                pixels[y+1][x+1][2] = brace_to_255(
                        pixels[y+1][x+1][2] +
                        e_blue * 1/16
                        )
    return output_img

