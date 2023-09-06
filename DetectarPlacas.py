import cv2
import pytesseract
import threading
import pymysql
import logging

class db:
    host:str
    user:str
    password:str
    database:str
    @classmethod
    def conect(self):
        connection = pymysql.connect(
            host=self.host,
            user=(f'{self.user}'),
            password=(f'{self.password}'),
            database=(f'{self.database}')
        )
        cursor = connection.cursor()
        return cursor
    

def contorno_imagem(imagem):
    image = cv2.imread(imagem)
    image_resized = cv2.resize(image, (800, 400))
    gray_image = cv2.cvtColor(image_resized, cv2.COLOR_BGR2GRAY)
    n, binary_image = cv2.threshold(gray_image, 90, 255, 0)
    blur_img = cv2.GaussianBlur(binary_image, (3, 3), 0)
    contours, hierarquia = cv2.findContours(blur_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        if perimeter > 300:
            aprox_retangulo = cv2.approxPolyDP(contour, 0.03 * perimeter, True)
            if len(aprox_retangulo) == 4:
                x, y, height, width = cv2.boundingRect(contour)
                cv2.rectangle(image_resized, (x, y), (x + height, y + width), (90, 255, 35), 3)
                roi = image_resized[y:y + width, x:x +height]
                cv2.imwrite('D:/VSCODE_PY/OpenCV/roi.png', roi)
    # cv2.imshow('roi', image_resized)
    # cv2.waitKey(0)

def preProcessamentoRoi():
    roi = cv2.imread('D:/VSCODE_PY/OpenCV/roi.png')
    if roi is None:
        return 
    
    roi_risezed = cv2.resize(roi, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    gray_roi = cv2.cvtColor(roi_risezed, cv2.COLOR_BGR2GRAY)   
    n, binary_roi = cv2.threshold(gray_roi, 70, 255, cv2.THRESH_BINARY)
    blur_roi = cv2.GaussianBlur(binary_roi, (5, 5), 0)
    cv2.imwrite('D:/VSCODE_PY/OpenCV/roi.png', blur_roi)
    # cv2.imshow('blur', blur_roi)
    # cv2.waitKey()

def ocrImagePlate():
    database = db
    database.host = 'localhost'
    database.user = 'root'
    database.password = '.VINxBLOw[JfTdo-'
    database.database = 'cadastros'
    cursor = db.conect()
    
    roi = cv2.imread('D:/VSCODE_PY/OpenCV/roi.png')
    if roi is not None:
        roi_resized = cv2.resize(roi, (800, 400))

        config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 6'

        saida = pytesseract.image_to_string(roi_resized, lang='eng', config=config)

        cursor.execute(f"select * from pessoas where placa_automovel = '{saida}';")
        
        placa = cursor.fetchall()

        if saida == placa:
            logging.basicConfig(filename='D:/VSCODE_PY/OpenCV/retorno.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
            logging.debug('A placa está presente no database é: %s', True)
        else:
            print(saida)
        


def webcam():
    validation, frame = cap.read()
    return frame

def imageAndOcrProcessing():
    while True:
        frame = webcam()
        cv2.imshow('webcam', frame)
        cv2.imwrite('D:/VSCODE_PY/OpenCV/imagem_webcam.png', frame)
        k = cv2.waitKey(5000)
        if k == ord('e'):
            cap.release()
            cv2.destroyAllWindows()
            break
        contorno_imagem('D:/VSCODE_PY/OpenCV/imagem_webcam.png')
        preproc = preProcessamentoRoi()
        ocrImagePlate()


if __name__ == "__main__":

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print('Erro ao abrir a camera!')
        exit()

    thread_processamento = threading.Thread(target=imageAndOcrProcessing, daemon=True)
    thread_processamento.start()
    
    while True:
        k = cv2.waitKey(5000)
        if k == ord('e'):
            cap.release()
            cv2.destroyAllWindows()
            break

    # imagecap('http://211.132.61.124/mjpg/video.mjpg')
    # contorno_imagem('D:/VSCODE_PY/Imagens/WIN_20230831_21_55_25_Pro.jpg') # normal ABC1234  if perimeter > 300: // n, binary_roi = cv2.threshold(gray_roi, 65, 255, cv2.THRESH_BINARY)
    # contorno_imagem('D:/VSCODE_PY/Imagens/WIN_20230831_22_18_14_Pro.jpg')       # m   ercosul FBR2A23  if perimeter > 300 and perimeter < 350: // roi_risezed = cv2.resize(roi, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
    # contorno_imagem('D:/VSCODE_PY/Imagens/WIN_20230831_22_23_23_Pro.jpg')    # moto
