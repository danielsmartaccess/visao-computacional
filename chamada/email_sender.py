import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def criar_mensagem_email(alunos_falta):
    """
    Cria a mensagem do e-mail com a lista de alunos faltantes.
    """
    data_atual = datetime.now().strftime("%d/%m/%Y")
    
    mensagem = f"""
    Prezados,

    Segue relação de alunos ausentes na aula do dia {data_atual}:

    """
    
    for i, aluno in enumerate(alunos_falta, 1):
        mensagem += f"{i}. {aluno}\n"
    
    mensagem += """
    
    Atenciosamente,
    Sistema Automático de Controle de Frequência
    """
    
    return mensagem

def enviar_email(alunos_falta):
    """
    Envia e-mail com a lista de alunos faltantes.
    """
    # Carregar configurações do e-mail
    remetente = os.getenv('EMAIL_SENDER')
    senha = os.getenv('EMAIL_PASSWORD')
    destinatarios = [os.getenv('EMAIL_COORD'), os.getenv('EMAIL_PEDAG')]
    
    # Criar mensagem
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = ', '.join(destinatarios)
    msg['Subject'] = f'Relatório de Faltas - {datetime.now().strftime("%d/%m/%Y")}'
    
    # Adicionar corpo do e-mail
    corpo = criar_mensagem_email(alunos_falta)
    msg.attach(MIMEText(corpo, 'plain'))
    
    try:
        # Configurar servidor SMTP (exemplo com Gmail)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        # Login
        server.login(remetente, senha)
        
        # Enviar e-mail
        server.send_message(msg)
        
        # Fechar conexão
        server.quit()
        
        print("E-mail enviado com sucesso!")
        return True
        
    except Exception as e:
        print(f"Erro ao enviar e-mail: {str(e)}")
        return False
