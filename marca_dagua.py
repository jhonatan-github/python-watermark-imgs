import cv2
import zipfile
import cv2
import numpy as np
import glob
import os
from numpy._distributor_init import filename

# Função para redimensionar a imagem de forma proporcional
def img_resizing(img, aux, aux_img, width_img):
    
    # Realiza cálculo para saber quantos pixels a imagem deve diminuir regra de 3
    aux_heigth = aux_img-aux
    aux = (aux_heigth*100)/aux_img
    aux_width = (width_img*aux)/100
    aux_width = width_img - aux_width
    aux_heigth = aux_img - aux_heigth
    
    # Redimensiona a imagem seguindo o valor da altura e largura encontrados no cálculo anterior
    resized_img = cv2.resize(img, (int(aux_heigth), int(aux_width)), interpolation=cv2.INTER_AREA)
    
    return resized_img

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
        print(img_path)
        # Diretório da imagem que contém a marca d'água e logotipo 
        watermark_img = cv2.imread('./watermark.png', -1)
        # pega a imagem do catalogo 
        catalog = cv2.imread('fundo.jpg')
        # Pega a imagem de fundo para receber a imagem redimensionada
        fundo = catalog.copy()
        fundo = cv2.resize(fundo, (640,480), interpolation=cv2.INTER_AREA)
        
        # Pega as dimensões da marca d'água
        heigth_watermark, width_watermark, _ = watermark_img.shape
        
        # Pega as dimensões da imagem
        heigth_img, width_img, _ = img.shape
        
        # Verifica em qual padrão a imagem se identifica e chama a função que redimensiona a imagem
        if heigth_img>width_img and heigth_img>heigth_watermark:
            resized_img = img_resizing(img,heigth_watermark, heigth_img, width_img)
            
        elif heigth_img<width_img and width_img>heigth_watermark:
            resized_img = img_resizing(img,width_watermark, width_img, heigth_img)
            
        elif heigth_img == width_img and heigth_img>heigth_watermark:
            resized_img = img_resizing(img,heigth_watermark, width_img, heigth_img)
            
        else:
            # Deixa a imagem no tamanho normal
            resized_img = cv2.resize(img, (heigth_img, width_img), interpolation=cv2.INTER_AREA)
        
        # Seleciona a altura e largura da imagem de fundo
        altura_img, largura_img, _ = fundo.shape
        
        # Identifica o meio da imagem
        center_y = int(altura_img/2)
        center_x = int(largura_img/2)
        
        # Seleciona a altura e largura da imagem do Catalogo que foi redimensionada
        altura_img, largura_img, _ = resized_img.shape
        
        # Pega do meio da imagem de fundo e diminui metade da imagem do Catalogo para saber onde a imagem vai começar   
        top_y_img = center_y - int(altura_img/2)
        left_x_img = center_x - int(largura_img/2)
        
        # Soma o início com o tamanho da imagem para saber onde a imagem termina
        bottom_y_img = top_y_img + altura_img
        right_x_img = left_x_img + largura_img
        
        # Adiciona na imagem de fundo a imagem do catalogo
        fundo[top_y_img:bottom_y_img, left_x_img:right_x_img] = resized_img
        
        # Define a opacidade
        opacity = opacity / 100
        
        # Pega imagem redimensionada
        img_resized = fundo.copy()
        
        # Mensagem que mostra o tamanho da nova imagem 
        print(img_resized.shape)
        
        # Tratamento para aplicação da marca d'água
        watermark = watermark_tratament(img_resized, watermark_img, pos)
        output = fundo.copy()
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
