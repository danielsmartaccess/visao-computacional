import cv2
import numpy as np
import pytesseract
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Configuração do Tesseract
pytesseract.pytesseract.tesseract_cmd = os.getenv('TESSERACT_PATH')

def mostrar_imagem(imagem, titulo="Imagem"):
    """
    Mostra uma imagem em uma janela.
    """
    # Redimensionar para um tamanho máximo de 800x800 mantendo a proporção
    altura, largura = imagem.shape[:2]
    max_dim = 800
    if altura > max_dim or largura > max_dim:
        if altura > largura:
            nova_altura = max_dim
            nova_largura = int(largura * (max_dim / altura))
        else:
            nova_largura = max_dim
            nova_altura = int(altura * (max_dim / largura))
        imagem = cv2.resize(imagem, (nova_largura, nova_altura))
    
    cv2.imshow(titulo, imagem)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def preprocessar_imagem(imagem_path):
    """
    Realiza o pré-processamento da imagem para melhorar o OCR.
    """
    # Carregar imagem
    img = cv2.imread(str(imagem_path))
    if img is None:
        raise Exception(f"Não foi possível carregar a imagem: {imagem_path}")

    # Mostrar imagem original
    mostrar_imagem(img, "Imagem Original")

    # Converter para escala de cinza
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Aumentar contraste usando equalização de histograma
    img_gray = cv2.equalizeHist(img_gray)
    mostrar_imagem(img_gray, "Escala de Cinza com Contraste Melhorado")

    # Aplicar threshold adaptativo com parâmetros ajustados
    img_thresh = cv2.adaptiveThreshold(
        img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 11
    )
    mostrar_imagem(img_thresh, "Threshold Adaptativo")

    # Remover ruído com filtro bilateral
    img_denoise = cv2.bilateralFilter(img_thresh, 9, 75, 75)
    mostrar_imagem(img_denoise, "Remoção de Ruído")

    # Aplicar operações morfológicas para melhorar a qualidade do texto
    kernel = np.ones((2,2), np.uint8)
    img_morph = cv2.morphologyEx(img_denoise, cv2.MORPH_CLOSE, kernel)
    mostrar_imagem(img_morph, "Morfologia")

    # Criar diretório para debug se não existir
    debug_dir = Path(__file__).parent / "debug_images"
    debug_dir.mkdir(exist_ok=True)

    # Salvar imagens de cada etapa
    cv2.imwrite(str(debug_dir / "1_original.png"), img)
    cv2.imwrite(str(debug_dir / "2_grayscale.png"), img_gray)
    cv2.imwrite(str(debug_dir / "3_threshold.png"), img_thresh)
    cv2.imwrite(str(debug_dir / "4_denoised.png"), img_denoise)
    cv2.imwrite(str(debug_dir / "5_morphology.png"), img_morph)

    return img_morph

def extrair_texto(imagem_processada):
    """
    Extrai texto da imagem usando OCR com configurações otimizadas.
    """
    # Configurar parâmetros do OCR otimizados para tabelas
    custom_config = '--oem 3 --psm 6 -c preserve_interword_spaces=1 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-.'
    
    # Realizar OCR
    texto = pytesseract.image_to_string(
        imagem_processada,
        config=custom_config
    )
    
    return texto

def processar_faltas(texto):
    """
    Processa o texto extraído para identificar alunos com falta.
    """
    linhas = texto.split('\n')
    alunos_falta = []
    
    for linha in linhas:
        # Ignorar linhas vazias ou muito curtas
        if len(linha.strip()) < 5:
            continue
            
        # Procurar por 'F' nas colunas P1, P2, P3 ou P4
        if 'F' in linha.upper():
            # Tentar extrair matrícula e nome do aluno
            partes = linha.split()
            if len(partes) >= 2:
                # Assumindo que a matrícula é o primeiro campo numérico
                matricula = None
                nome = []
                encontrou_f = False
                
                for parte in partes:
                    if parte.upper() == 'F':
                        encontrou_f = True
                        continue
                    
                    if parte.isdigit() and not matricula:
                        matricula = parte
                    elif not encontrou_f and not parte.isdigit():
                        nome.append(parte)
                
                if matricula and nome:
                    aluno_info = f"Matrícula: {matricula} - Nome: {' '.join(nome)}"
                    if aluno_info not in alunos_falta:
                        alunos_falta.append(aluno_info)
    
    return alunos_falta

def processar_chamada(imagem_path):
    """
    Função principal que processa a imagem da chamada e retorna os alunos com falta.
    """
    # Pré-processar imagem
    img_processada = preprocessar_imagem(imagem_path)
    
    # Extrair texto
    texto = extrair_texto(img_processada)
    
    # Processar faltas
    alunos_falta = processar_faltas(texto)
    
    return alunos_falta

def salvar_debug_image(img, nome_arquivo):
    """
    Salva uma imagem para debug/visualização.
    """
    debug_dir = Path("debug")
    debug_dir.mkdir(exist_ok=True)
    cv2.imwrite(str(debug_dir / nome_arquivo), img)
