from PIL import Image
import numpy as np

width, height = 256, 128

x = np.linspace(0, 1, width, dtype=np.float32)
grad = np.tile(x[None, :], (height, 1))

img = np.stack([grad, grad**0.5, grad**2], axis=-1)
