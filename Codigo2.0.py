import cv2
import pytesseract
import threading
import pymysql
import logging
import time


class db:
    host:str
    user:str
    password:str
    database:str
    @classmethod
    def conect(cls):
        connection = pymysql.connect(
            host=cls.host,
            user=cls.user,
            password=cls.password,
            database=cls.database
        )
        cursor = connection.cursor()
        return cursor
    
    


class imagem:
    
    def ImageCapture(self):
        cap = cv2.VideoCapture(0)
        validation, frame = cap.read()
        while validation:
            validation, frame = cap.read()
            cv2.imshow('Webcam', frame)
            k = cv2.waitKey(2000)
            if k == 113:
                cap.release()
                cv2.destroyAllWindows()
                break
            self.contorno_imagem(frame)
            self.preProcessamentoRoi()
            self.ocrImagePlate()
    
    def contorno_imagem(self, frame):
        if frame is not None:
            image_resized = cv2.resize(frame, (800, 400))
            gray_image = cv2.cvtColor(image_resized, cv2.COLOR_BGR2GRAY)
            _, binary_image = cv2.threshold(gray_image, 90, 255, 0)
            blur_img = cv2.GaussianBlur(binary_image, (3, 3), 0)
            contours, _ = cv2.findContours(blur_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

            for contour in contours:
                perimeter = cv2.arcLength(contour, True)
                if perimeter > 300:
                    aprox_retangulo = cv2.approxPolyDP(contour, 0.03 * perimeter, True)
                    if len(aprox_retangulo) == 4:
                        x, y, height, width = cv2.boundingRect(contour)
                        cv2.rectangle(image_resized, (x, y), (x + height, y + width), (90, 255, 35), 3)
                        roi = image_resized[y:y + width, x:x +height]
                        cv2.imwrite('D:/VSCODE_PY/Projeto_placas/roi.png', roi)
    
    def preProcessamentoRoi(self):
        max_width = 800
        max_height = 400    
        roi = cv2.imread('D:/VSCODE_PY/Projeto_placas/roi.png')
        if roi is None:
            return 
        
        current_height, current_width = roi.shape[:2]
        if current_width > max_width or current_height > max_height:
            roi = cv2.resize(roi, (max_width, max_height), interpolation=cv2.INTER_CUBIC)
        roi_risezed = cv2.resize(roi, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        gray_roi = cv2.cvtColor(roi_risezed, cv2.COLOR_BGR2GRAY)   
        n, binary_roi = cv2.threshold(gray_roi, 70, 255, cv2.THRESH_BINARY)
        blur_roi = cv2.GaussianBlur(binary_roi, (5, 5), 0)
        cv2.imwrite('D:/VSCODE_PY/Projeto_placas/roi.png', blur_roi)
        # cv2.imshow('blur', blur_roi)
        # cv2.waitKey()

    def ocrImagePlate(self):
        roi = cv2.imread('D:/VSCODE_PY/Projeto_placas/roi.png')
        if roi is not None:
            roi_resized = cv2.resize(roi, (800, 400))

            config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 6'

            saida = pytesseract.image_to_string(roi_resized, lang='eng', config=config)
            saida = saida.strip().upper()

            database = db
            database.host = 'localhost'
            database.user = 'root'
            database.password = '.VINxBLOw[JfTdo-'
            database.database = 'cadastros'

            cursor = db.conect()
            cursor.execute(f"select placa_automovel from pessoas where placa_automovel = '{saida}';")
            placa = cursor.fetchall()
            if len(placa) > 0:
                placa = placa[0][0]
                placa = placa.strip().upper()
            
            
            if saida == placa:
                print('foi')
                logging.basicConfig(filename='D:/VSCODE_PY/Projeto_placas/retorno.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
                logging.debug(f'A placa "{placa}" está presente no database: %s', True) 
                exit()
            else:
                print(saida)

if __name__ == "__main__":

    img = imagem()
    thread_processamnto = threading.Thread(target=img.ImageCapture(), daemon=True)
    thread_processamnto.start()
    
