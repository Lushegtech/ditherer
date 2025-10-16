from PIL import Image
import numpy as np

width, height = 512, 256

x = np.linspace(0, 1, width, dtype = np.float32)
grad = np.tile(x[None, :], (height, 1))

img = np.stack([grad**1.5, np.sqrt(grad), np.sin(grad * np.pi * 0.5)], axis=-1)

Image.fromarray((img * 255 + 0.5).astype(np.uint8), "RGB").save("examples/gradient.png")

print("Gradient saved to examples/gradient.png")