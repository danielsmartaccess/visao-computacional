from pathlib import Path
from processamento import processar_chamada
from email_sender import enviar_email
import sys

def main():
    # Criar diretório de imagens se não existir
    script_dir = Path(__file__).parent
    imagens_dir = script_dir / "imagens"
    imagens_dir.mkdir(exist_ok=True)
    
    # Verificar se há imagens na pasta
    imagens = list(imagens_dir.glob("*.png")) + list(imagens_dir.glob("*.jpg"))
    
    if not imagens:
        print("Nenhuma imagem encontrada na pasta 'imagens/'")
        print("Por favor, adicione uma imagem de chamada (.png ou .jpg) na pasta.")
        return
    
    # Processar a primeira imagem encontrada
    imagem_path = imagens[0]
    print(f"Processando imagem: {imagem_path}")
    
    try:
        # Processar a chamada
        alunos_falta = processar_chamada(imagem_path)
        
        if not alunos_falta:
            print("\n=== RESULTADO DA CHAMADA ===")
            print("✓ Todos os alunos presentes!")
            print("============================")
            return
        
        print("\n=== RESULTADO DA CHAMADA ===")
        print("Alunos ausentes detectados:")
        print("---------------------------")
        for i, aluno in enumerate(alunos_falta, 1):
            print(f"  {i}. {aluno}")
        print("============================")
        
        # Perguntar se deseja enviar e-mail
        resposta = input("\nDeseja enviar e-mail com esta lista? (s/n): ")
        
        if resposta.lower() == 's':
            print("\nEnviando e-mail...")
            sucesso = enviar_email(alunos_falta)
            if sucesso:
                print("✓ E-mail enviado com sucesso!")
            else:
                print("❌ Erro ao enviar e-mail. Verifique as configurações no arquivo .env")
        
    except Exception as e:
        print(f"Erro ao processar a imagem: {str(e)}")
        return

if __name__ == "__main__":
    main()
