# Sistema de Processamento de Chamada

Este projeto processa imagens de chamadas de sala de aula para extrair informações sobre faltas e gerar e-mails automáticos.

## Configuração do Ambiente

1. Instale o Tesseract OCR:
   - Windows: Baixe o instalador em https://github.com/UB-Mannheim/tesseract/wiki
   - Durante a instalação, anote o caminho de instalação (geralmente `C:\Program Files\Tesseract-OCR`)

2. Instale as dependências Python:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
   - Crie um arquivo `.env` com as seguintes informações:
```
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
EMAIL_SENDER=seu_email@exemplo.com
EMAIL_PASSWORD=sua_senha_de_app
EMAIL_COORD=coordenacao@exemplo.com
EMAIL_PEDAG=pedagogico@exemplo.com
```

## Uso

1. Coloque a imagem da chamada na pasta `imagens/`
2. Execute o script principal:
```bash
python main.py
```

## Estrutura do Projeto
- `main.py`: Script principal
- `processamento.py`: Funções de processamento de imagem
- `email_sender.py`: Funções para envio de e-mail
- `imagens/`: Pasta para armazenar as imagens de chamada
- `.env`: Arquivo de configuração (não versionado)
