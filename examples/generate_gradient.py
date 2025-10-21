from PIL import Image
import numpy as np

width, height = 512, 256

x = np.linspace(0, 1, width, dtype = np.float32)
grad = np.tile(x[None, :], (height, 1))

red = grad ** 1.5
blue = np.sqrt(grad)
green = np.sin(grad * np.pi * 0.5)

img = np.stack([red, green, blue], axis=-1)

print(img.ndim)
print(img.shape)
print(img.dtype)

img_grad = Image.fromarray((img * 255 + 0.5).astype(np.uint8), "RGB")
img_grad.save("examples/gradient.png")

print("Your generated gradient has been saved to examples/gradient.png")