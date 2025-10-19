from PIL import Image
import argparse

PALETTE = [(0, 0, 0), (255, 255, 255)]

def nearest_color(pixel):

    red, green, blue = pixel
    best = None
    best_dist = 100 ** 9
    
    for pred, pgreen, pblue in PALETTE:
        distance = (red - pred) ** 2 + (green - pgreen) ** 2 + (blue - pblue) ** 2
        if distance < best_dist:
            best_dist = distance
            best = (pred, pgreen, pblue)
    
    return best

def clamp255(x):
    
    if x < 0:
        return 0
    elif x > 255:
        return 255
    else:
        return x

def floyd_steinberg_b_w(image):

    image = image.convert("RGB")
    width, height = image.size

    work = [[list(image.getpixel((x,y))) for x in range(width)] for y in range(height)]

    output = Image.new("RGB", (width, height))

    for y in range(height):
        for x in range(width):

            old = [int(round(color)) for color in work[y][x]]
            new = nearest_color(old)
            output.putpixel((x,y), new)

            error = [old[0] - new[0], old[1] - new[1], old[2] - new[2]]

            def give_frac(x2, y2, share):
                
                if 0 <= x2 < width and 0 <= y2 < height:
                    red, green, blue = work[y2][x2]
                    
                    red_error_frac = red + error[0] * share
                    green_error_frac = green + error[1] * share
                    blue_error_frac = blue + error[2] * share

                    work[y2][x2] = [
                        clamp255(red_error_frac), 
                        clamp255(green_error_frac),
                        clamp255(blue_error_frac),
                    ] 

            give_frac(x+1, y, 7/16)
            give_frac(x-1, y + 1, 3/16)
            give_frac(x, y+1, 5/16)
            give_frac(x+1, y+1, 1/16)

    return output

def main():
    ap = argparse.ArgumentParser(description="Black and White Floyd–Steinberg dither")
    ap.add_argument("input", help="examples/gradient.png")
    ap.add_argument("output", help="out_bw.png")
    args = ap.parse_args()

    img = Image.open(args.input)
    out = floyd_steinberg_b_w(img)
    out.save(args.output)
    
    print(f"The dithered image was saved as {args.output}")

if __name__ == "__main__":
    main()
