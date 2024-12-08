# Sistema de Detecção de Pessoas em Vídeo

Este é um sistema que utiliza visão computacional para detectar e contar pessoas em vídeos em tempo real.

## Funcionalidades

- Detecção de pessoas em tempo real usando webcam
- Suporte para análise de vídeos do YouTube
- Contagem automática de pessoas detectadas
- Visualização em tempo real com retângulos marcando as pessoas
- Exibição do número total de pessoas na tela

## Como usar

### Com Webcam
```bash
python main_v2.py
# ou
python main_v2.py --source 0
```

### Com vídeo do YouTube
```bash
python main_v2.py --source "URL_DO_YOUTUBE"
```

Por exemplo:
```bash
python main_v2.py --source "https://www.youtube.com/watch?v=exemplo"
```

## Requisitos

- Python 3.x
- OpenCV (opencv-python)
- NumPy
- pytube (para vídeos do YouTube)

## Instalação

```bash
pip install -r requirements.txt
```

## Controles

- Pressione 'q' para sair do programa

## Limitações

- O sistema funciona melhor com boa iluminação
- A detecção pode variar dependendo da qualidade do vídeo
- Pessoas parcialmente visíveis podem não ser detectadas
- O sistema pode ocasionalmente gerar falsos positivos
