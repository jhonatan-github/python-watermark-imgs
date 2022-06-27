import cv2
import zipfile
import cv2
import numpy as np
import glob
import os
from numpy._distributor_init import filename

# Diretório das imagens originais
images_path = glob.glob("./images/*.*")

# Tratamento imagem (marca d'água)
def watermark_tratament(src, watermark, pos=(0, 0), scale=1):

    watermark = cv2.resize(watermark, (0, 0), fx=scale, fy=scale)
    h, w, _ = watermark.shape  # Tamanho da marca d'água 
    rows, cols, _ = src.shape  # Tamanho da imagem  
    y, x = pos[0], pos[0]  # Posição da imagem de primeiro plano/sobreposição
    
    # faz um loop em todos os pixels e aplica a equação de mesclagem
    for i in range(h):
        for j in range(w):
            if x + i >= rows or y + j >= cols:
                continue
            alpha = float(watermark[i][j][3] / 255.0) # lê o canal alfa
            src[x + i][y + j] = alpha * watermark[i][j][:3] + (1 - alpha) * src[x + i][y + j]
    return src

for img_path in images_path:
    
    def add_logowatermark(watermark_img,any,opacity,pos=(10,100),):
        
        # Seleciona uma imagem
        img = cv2.imread(img_path) 
               
        # Define uma porcentagem de escala de largura e altura
        percent_of_scaling = 100
        new_width = int(img.shape[1] * percent_of_scaling/100)
        new_height = int(img.shape[0] * percent_of_scaling/100)
        
        # Define dimensão padrão largura e altura
        new_dim = (new_width, new_height)
        
        # Aplica nova dimensão
        resized_img = cv2.resize(img, new_dim, interpolation=cv2.INTER_AREA)
        
        # Define tamanho das imagens, opacidade
        resized_img = cv2.resize(resized_img,(640,480),interpolation=cv2.INTER_AREA)
        opacity = opacity / 100
        
        # Diretório da imagem que contém a marca d'água e logotipo 
        watermark_img = cv2.imread('./images/marcadagua/marcadagua.png', -1)
        
        # Pega imagem redimensionda
        img_resized = resized_img.copy()
        
        # Mensagem que mostra o tamanho da nova imagem 
        print(img_resized.shape)
        
        # Tratamento para aplicação da marca d'água
        watermark = watermark_tratament(img_resized, watermark_img, pos)
        output = resized_img.copy()
        resized_img = cv2.addWeighted(watermark, opacity, output, 1 - opacity, 0, output)
        
        # Define o nome da imagem
        filename= os.path.basename(img_path)
        
        # Salva as imagens tratadas em um diretório 
        cv2.imwrite("./images_marcadagua/" + filename, resized_img)
        
    if __name__ == '__main__':
        add_logowatermark(any,any,100,(10,100))
    
    
    # Cria um arquivo zipado (.zip) com as imagens tratadas
    zf = zipfile.ZipFile("images.zip", "w")
for dirname, subdirs, files in os.walk("./images_marcadagua"):
    zf.write(dirname)
    for filename in files:
        zf.write(os.path.join(dirname, filename))
    zf.close()