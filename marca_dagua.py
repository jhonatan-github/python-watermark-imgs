import cv2
import zipfile
import cv2
import numpy as np
import glob
import os
from numpy._distributor_init import filename

# Diretório das imagens 
images_path = glob.glob("./images/*.*")

    
for img_path in images_path:
    
    # Selecina uma imagem
    img = cv2.imread(img_path)
    
    # Seleciona a logo do catalogo
    catalog = cv2.imread('./images/logo_marcadagua/catalog.png')
    
    # Seleciona a logo para marca d'água
    watermark = cv2.imread("./images/logo_marcadagua/logo_marcadagua.png")

    # Define uma porcentagem de escala
    percent_of_scaling = 100
    new_width = int(img.shape[1] * percent_of_scaling/100)
    new_height = int(img.shape[0] * percent_of_scaling/100)
    
    # Define dimensão padrão
    new_dim = (new_width, new_height)
    
    # Aplica nova dimensão
    resized_img = cv2.resize(img, new_dim, interpolation=cv2.INTER_AREA)
    resized_cat = cv2.resize(catalog, new_dim, interpolation=cv2.INTER_AREA)
    resized_wm = cv2.resize(watermark, new_dim, interpolation=cv2.INTER_AREA)
    
    # Redefine tamanho das imagens
    catalog = cv2.resize(resized_cat,(250,100), interpolation=cv2.INTER_AREA)
    resized_img = cv2.resize(resized_img,(640,480),interpolation=cv2.INTER_AREA)
    resized_wm = cv2.resize(resized_wm, (640,480), interpolation=cv2.INTER_AREA)
    
    # Seleciona a altura e largura da imagem defundo
    h_img, w_img, _ = resized_img.shape
    
    # Valor do meio da imagem
    center_y = int(h_img/2)
    center_x = int(w_img/2)
    
    # Seleciona a altura e largura da marca d'água
    h_wm, w_wm, _ = resized_wm.shape
    
    # Pega do meio da imagem e diminui metade da marca d'água
    top_y = center_y - int(h_wm/2)
    left_x = center_x - int(w_wm/2)
    
    # Soma o início com o tamanho da imagem
    bottom_y = top_y + h_wm
    right_x = left_x + w_wm

    # Pega a altura da imagem e diminui o tamanho da logo
    hc = h_img - 100
    
    # Define onde a logo termina
    bc = h_img
    
    # Início da imagem
    lc = 0
    
    # Final da imagem
    rc = 250
    
    # Lugar onde a marca d'água vai ficar
    roi = resized_img[top_y:bottom_y, left_x:right_x]
    
    # Mescla as duas imagens
    result = cv2.addWeighted(roi, 0.7, resized_wm, 0.1, 0)
    
    # lugar onde a logo do catalogo vai ficar
    resized_img[top_y:bottom_y, left_x:right_x] = result
    roi1 = resized_img[hc:bc,lc:rc]
    
    # mescla as duas imagens
    catalog = cv2.addWeighted(roi1, 1, catalog, 1, 0)
    resized_img[hc:bc,lc:rc] = catalog
    print(top_y)
    print(bottom_y)
    print(left_x)
    print(right_x)
   
    # define o nome da imagem
    filename= os.path.basename(img_path)
    
    # salva as imagens
    cv2.imwrite("images_marcadagua/" + filename, resized_img)
    
    # cria um arquivo .zip com as imagens com a marca d'água e logotipo aplicadas
    zf = zipfile.ZipFile("images.zip", "w")
for dirname, subdirs, files in os.walk("images_marcadagua"):
    zf.write(dirname)
    for filename in files:
        zf.write(os.path.join(dirname, filename))
    zf.close()