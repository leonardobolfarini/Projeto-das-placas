import cv2
import pytesseract
import pymysql
import serial
import time
import numpy as np
from datetime import datetime

arduino = serial.Serial("COM6", 9600)

class Database:
    _host:str
    _user:str
    _port:int
    _password:str
    _database:str

    def __init__(self):
        self._host = None
        self._user = None
        self._password = None
        self._database = None   

    @classmethod
    def _connect(cls):
        try:
            connection = pymysql.connect(
                host=cls._host,
                user=cls._user,
                password=cls._password,
                database=cls._database
            )
            return connection
        except:
            print('Não foi possivel estabelecer a conexão com o banco de dados')

class Image:
    def _ImageCapture(self):   
        cap = cv2.VideoCapture(0)
        _, frame = cap.read()
        cv2.waitKey(2000)
        return frame

    def _ContourImage(self, frame):
        if frame is not None:
            image_resized = cv2.resize(frame, (800, 400))
            gray_image = cv2.cvtColor(image_resized, cv2.COLOR_BGR2GRAY)
            _, binary_image = cv2.threshold(gray_image, 90, 255, 0)
            blur_img = cv2.GaussianBlur(binary_image, (3, 3), 0)
            contours, _ = cv2.findContours(blur_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

            for contour in contours:
                perimeter = cv2.arcLength(contour, True)
                if perimeter > 300: 
                    aprox_retang = cv2.approxPolyDP(contour, 0.03 * perimeter, True)
                    if len(aprox_retang) == 4:
                        x, y, height, width = cv2.boundingRect(contour)
                        cv2.rectangle(image_resized, (x, y), (x + height, y + width), (90, 255, 35), 3)
                        region_of_interest = image_resized[y:y + width, x:x +height]
                        return region_of_interest
                        
    def _PreProcessRoi(self, roi):
        max_width = 800
        max_height = 400    
        if roi is None:
            return 
            
        current_height, current_width = roi.shape[:2]
        if current_width > max_width or current_height > max_height:
            roi = cv2.resize(roi, (max_width, max_height), interpolation=cv2.INTER_CUBIC)
        roi_risezed = cv2.resize(roi, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        gray_roi = cv2.cvtColor(roi_risezed, cv2.COLOR_BGR2GRAY)   
        _, binary_roi = cv2.threshold(gray_roi, 70, 255, cv2.THRESH_BINARY)
        blur_roi = cv2.GaussianBlur(binary_roi, (5, 5), 0)
        return blur_roi

    def _OcrImagePlate(self, roi):
        output = ''
        if roi is not None:
            roi_resized = cv2.resize(roi, (800, 400))
            config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 6'
            string_founded = pytesseract.image_to_string(roi_resized, lang='eng', config=config)
            string_founded = string_founded.strip().upper()
        return string_founded

def open_gate():
    image = Image()
    frame = image._ImageCapture()
    while frame is not None:
        frame = image._ImageCapture()
        roi = image._ContourImage(frame)
        img_preprocess = image._PreProcessRoi(roi)
        string_founded = image._OcrImagePlate(img_preprocess)

        db = Database
        db._host = '162.240.34.167' 
        db._user = 'devbr_wp_kqeph'
        db._password = '#rbwqU77X3Zy5Zz#'
        db._database = 'devbr_wp_yx08y'
        connection = db._connect()
        cursor = connection.cursor()
        cursor.execute(f"select placa_automovel from pessoas where placa_automovel = '{string_founded}';")
        plate = cursor.fetchall()

        if len(plate) > 0:
            plate = plate[0][0]
            plate = plate.strip().upper()

        if string_founded == plate:
            arduino.write(b'0')
            time.sleep(5)
            arduino.write(b'1')
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_message = (f'{timestamp} - Cancela aberta - Placa {plate}')
            cursor.execute(f'insert into logs values(default, "{log_message}")')
            connection.commit()
            connection.close()

        else:
            arduino.write(b'1')

if __name__ == '__main__':
    open_gate()
