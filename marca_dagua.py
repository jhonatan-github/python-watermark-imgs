import zipfile
import cv2
import numpy as np
import glob
import os
import shutil

from numpy._distributor_init import filename

# Diretório das imagens originais
images_path = glob.glob("./images/*.*")

# Cria um diretório para salvar as imagens tratadas
dir = './temp'       
os.makedirs(dir)

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
        
        # Diretório da marca d'água
        watermark_img = cv2.imread('./images/marcadagua/watermark.png', -1)
        print(watermark_img.shape)
        
        # Pega a imagem do catalogo 
        catalog = cv2.imread('./images/marcadagua/fundo.jpg')
        
        # Cria uma imagem de fundo transparente para receber a imagem redimensionada
        fundo = catalog.copy()
        fundo = fundo[0:480,0:320]
        fundo = cv2.resize(fundo, (640,480), interpolation=cv2.INTER_AREA)
        
        # teste, redimensiona para que a imagem seja maior ou menor que o fundo
        img = cv2.resize(img,(1000, 300),interpolation=cv2.INTER_AREA)
        
        # Pega as dimensões da marca d'água
        heigth_watermark, width_watermark, _ = watermark_img.shape
        
        # Pega as dimensões da imagem
        heigth_img, width_img, _ = img.shape
        
        # Verifica em qual padrão a imagem se encaixa, exemplo: a imagem é um retangulo
        if heigth_img > heigth_watermark and width_img > width_watermark:
            # Aplica nova dimensão na imagem
            resized_img = cv2.resize(img, (width_watermark, heigth_watermark), interpolation=cv2.INTER_AREA)
            
        elif heigth_img<=heigth_watermark and width_img>width_watermark:
            # Aplica nova dimensão na imagem
            resized_img = cv2.resize(img, (width_watermark, heigth_img), interpolation=cv2.INTER_AREA)
            
        elif heigth_img>heigth_watermark and width_img<=width_watermark:
            # Aplica nova dimensão na imagem
            resized_img = cv2.resize(img, (width_img,heigth_watermark), interpolation=cv2.INTER_AREA)
           
        else:
            # Aplica nova dimensão na imagem
            resized_img = cv2.resize(img, (width_img, heigth_img), interpolation=cv2.INTER_AREA)


            
        
        # Seleciona a altura e largura da imagem de fundo
        altura_img, largura_img, _ = fundo.shape
        
        # Identifica o meio da imagem
        center_y = int(altura_img/2)
        center_x = int(largura_img/2)
        
        # Seleciona a altura e largura da imagem do Catalogo
        altura_img, largura_img, _ = resized_img.shape
        
        # Pega do meio da imagem de fundo e diminui metade da imagem do Catalogo para saber onde a imagem vai começar   
        top_y_img = center_y - int(altura_img/2)
        left_x_img = center_x - int(largura_img/2)
        
        # Soma o início com o tamanho da imagem
        bottom_y_img = top_y_img + altura_img
        right_x_img = left_x_img + largura_img
        
        # Adiciona a imagem do catalogo com a dimensão correta na imagem de fundo
        roi = fundo[top_y_img:bottom_y_img, left_x_img:right_x_img]
        resized_img = cv2.addWeighted(resized_img,1,roi,0,0, resized_img)
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
        print(str(watermark.shape)+"=="+str(output.shape))
        resized_img = cv2.addWeighted(watermark, opacity, output, 1 - opacity, 0, output)
        
        # Defini o mesmo nome da imagem orginal 
        filename= os.path.basename(img_path)
        
        # Salva as imagens tratadas em um diretório temporário
        cv2.imwrite("./temp/" + filename, resized_img)
        
    if __name__ == '__main__':
        add_logowatermark(any,any,100,(10,100))
    
    # Cria um arquivo compactado (.zip) com as imagens tratadas
    zf = zipfile.ZipFile("images.zip", "w")
for dirname, subdirs, files in os.walk("./temp/"):
    zf.write(dirname)
    for filename in files:
        zf.write(os.path.join(dirname, filename))
    zf.close()
    
    # Remove diretório temporário
    shutil.rmtree('./temp/')