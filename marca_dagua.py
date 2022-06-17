# bibliotecas
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
  
# abrir imagens
marcadagua = Image.open("images/marcadagua.jpg")
imagem = Image.open("images/teste.jpg")
  
# tamanho marcadagua
size = (500, 400)
crop_image = marcadagua.copy()
crop_image.thumbnail(size)
  
# adicionando marcadagua
copied_image = imagem.copy()

# localização marcadagua
copied_image.paste(crop_image, (1300, 700))

# aplicando marcadagua
plt.imshow(copied_image)

# Salvando imagem com marcadagua
rgb_im = copied_image.convert('RGB')
rgb_im.save('images/marcadagua/imagem+marcadagua.jpg')
