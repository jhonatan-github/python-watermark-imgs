Watermark Imagens
Este script em Python é usado para aplicar uma marca d'água em uma coleção de imagens. Ele redimensiona as imagens de acordo com as dimensões da marca d'água e as combina com uma imagem de fundo de catálogo para criar uma nova imagem que inclui a marca d'água.

Pré-requisitos
Python 3.x
OpenCV (cv2) - Você pode instalá-lo usando pip install opencv-python
Biblioteca NumPy (numpy) - Você pode instalá-la usando pip install numpy
Como Usar
Certifique-se de que as imagens originais estão no diretório ./images/.

Execute o script watermarking.py usando o Python.

O script aplicará a marca d'água nas imagens, redimensionando-as de acordo com as dimensões da marca d'água e combinando-as com a imagem de fundo do catálogo.

As imagens tratadas serão salvas temporariamente no diretório ./temp/.

Um arquivo compactado images.zip será criado, contendo todas as imagens tratadas.

O diretório temporário ./temp/ será removido após a criação do arquivo compactado.

Personalização
Você pode personalizar o posicionamento, tamanho e opacidade da marca d'água no script:

pos: A posição (x, y) onde a marca d'água será aplicada na imagem.
scale: Fator de escala para ajustar o tamanho da marca d'água.
opacity: Opacidade da marca d'água (em porcentagem).
Você também pode personalizar os diretórios das imagens de marca d'água e de fundo do catálogo de acordo com as suas necessidades.

Notas
Certifique-se de ter as imagens originais no diretório ./images/ e que os arquivos de marca d'água e de fundo do catálogo estão nos caminhos especificados no código.
O script redimensionará as imagens originais para que a maior dimensão da imagem original seja igual à maior dimensão da marca d'água. Isso pode resultar em perda de qualidade ou distorção, dependendo das dimensões originais.
A opacidade da marca d'água afeta o nível de transparência da marca d'água. Um valor maior resultará em uma marca d'água mais visível, enquanto um valor menor a tornará mais transparente.
