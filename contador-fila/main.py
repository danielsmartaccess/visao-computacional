import cv2
import numpy as np
import sys

def contar_pessoas():
    try:
        # Inicializar a captura de vídeo (0 é geralmente a webcam)
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Erro: Não foi possível abrir a webcam")
            return
        
        # Configurar a resolução da webcam para melhor qualidade
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        # Carregar o classificador HOG para detecção de pessoas
        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        
        # Configurações para melhorar a detecção
        frame_count = 0
        detected_counts = []
        last_boxes = []  # Para rastreamento simples
        
        while True:
            # Ler o frame da câmera
            ret, frame = cap.read()
            if not ret:
                print("Erro: Não foi possível ler o frame da câmera")
                break
            
            # Melhorar o contraste da imagem
            lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
            cl = clahe.apply(l)
            limg = cv2.merge((cl,a,b))
            frame = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
            
            # Redimensionar o frame mantendo a proporção
            height, width = frame.shape[:2]
            scale = 640 / width
            dim = (640, int(height * scale))
            frame = cv2.resize(frame, dim)
            
            # Aplicar um leve desfoque para reduzir ruído
            frame = cv2.GaussianBlur(frame, (5, 5), 0)
            
            # Detectar pessoas no frame com parâmetros ainda mais sensíveis
            boxes, weights = hog.detectMultiScale(
                frame, 
                winStride=(8,8),      # Aumentado para reduzir falsos positivos
                padding=(4,4),        # Aumentado um pouco
                scale=1.05,          # Aumentado para ser mais seletivo
                hitThreshold=0.1     # Aumentado para ser mais rigoroso
            )
            
            # Filtrar e combinar detecções próximas
            filtered_boxes = []
            if len(boxes) > 0:
                pick = non_max_suppression(boxes, weights, 0.5)  # Aumentado threshold de sobreposição
                for i in pick:
                    if weights[i] > 0.3:  # Aumentado limiar de confiança significativamente
                        filtered_boxes.append((boxes[i], weights[i]))
            
            # Usar rastreamento simples para manter detecções estáveis
            if len(filtered_boxes) == 0 and len(last_boxes) > 0:
                filtered_boxes = last_boxes
            else:
                last_boxes = filtered_boxes
            
            # Desenhar retângulos ao redor das pessoas detectadas
            for (x, y, w, h), weight in filtered_boxes:
                # Desenhar com cor baseada na confiança
                color = (0, int(255 * min(weight, 1.0)), 0)
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                # Adicionar o valor de confiança acima do retângulo
                cv2.putText(frame, f'{weight:.2f}', (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
            
            # Suavizar a contagem usando média móvel
            frame_count += 1
            detected_counts.append(len(filtered_boxes))
            if len(detected_counts) > 3:
                detected_counts.pop(0)
            
            num_pessoas = round(sum(detected_counts) / len(detected_counts))
            
            # Mostrar o número de pessoas detectadas
            texto = f'Pessoas na fila: {num_pessoas}'
            cv2.putText(frame, texto, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Adicionar instruções e informações na tela
            cv2.putText(frame, 'Pressione "q" ou "ESC" para sair', (10, frame.shape[0]-20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Mostrar o frame
            cv2.imshow('Contador de Pessoas na Fila', frame)
            
            # Verificar teclas - agora aceita 'q' ou ESC
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:  # 27 é o código ASCII para ESC
                print("\nEncerrando o programa...")
                break
    
    except Exception as e:
        print(f"Erro: {str(e)}")
    
    finally:
        # Liberar recursos
        if 'cap' in locals():
            cap.release()
        cv2.destroyAllWindows()
        print("Programa encerrado com sucesso!")

def non_max_suppression(boxes, weights, overlap_thresh):
    """Função para combinar detecções sobrepostas"""
    if len(boxes) == 0:
        return []
    
    # Converter para float
    boxes = boxes.astype("float")
    
    # Inicializar a lista de índices selecionados
    pick = []
    
    # Pegar coordenadas das caixas
    x1 = boxes[:,0]
    y1 = boxes[:,1]
    x2 = boxes[:,0] + boxes[:,2]
    y2 = boxes[:,1] + boxes[:,3]
    
    # Computar área das caixas
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    
    # Ordenar por probabilidade
    idxs = np.argsort(weights)
    
    while len(idxs) > 0:
        # Pegar o último índice e adicionar à lista
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)
        
        # Encontrar as maiores coordenadas para início
        # e menores coordenadas para fim
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])
        
        # Computar altura e largura
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)
        
        # Computar razão de sobreposição
        overlap = (w * h) / area[idxs[:last]]
        
        # Deletar índices com sobreposição maior que threshold
        idxs = np.delete(idxs, np.concatenate(([last],
            np.where(overlap > overlap_thresh)[0])))
    
    return pick

if __name__ == "__main__":
    print("Iniciando sistema de contagem de pessoas...")
    print("Pressione 'q' ou ESC para sair")
    contar_pessoas()
