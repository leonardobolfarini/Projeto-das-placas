import cv2
import pytesseract

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

    cv2.imshow('contourno', image_resized)
    cv2.waitKey()
    cv2.destroyAllWindows()

def preProcessamentoRoi():
    roi = cv2.imread('D:/VSCODE_PY/OpenCV/roi.png')
    if roi is None:
        return 
    
    roi_risezed = cv2.resize(roi, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    gray_roi = cv2.cvtColor(roi_risezed, cv2.COLOR_BGR2GRAY)   
    n, binary_roi = cv2.threshold(gray_roi, 65, 255, cv2.THRESH_BINARY)
    blur_roi = cv2.GaussianBlur(binary_roi, (5, 5), 0)
    cv2.imshow('blur', blur_roi)
    cv2.imwrite('D:/VSCODE_PY/OpenCV/roi.png', blur_roi)
    cv2.waitKey()
    cv2.destroyAllWindows()

def ocrImagePlate():
    roi = cv2.imread('D:/VSCODE_PY/OpenCV/roi.png')

    config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 6'

    output = pytesseract.image_to_string(roi, lang='eng', config=config)

    print(output)


if __name__ == "__main__":
    contorno_imagem('D:/VSCODE_PY/Imagens/WIN_20230831_21_55_25_Pro.jpg') # normal ABC1234  if perimeter > 300: // n, binary_roi = cv2.threshold(gray_roi, 65, 255, cv2.THRESH_BINARY)
    # contorno_imagem('D:/VSCODE_PY/Imagens/WIN_20230831_22_18_14_Pro.jpg')       # mercosul FBR2A23  if perimeter > 300 and perimeter < 350: // roi_risezed = cv2.resize(roi, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
    # contorno_imagem('D:/VSCODE_PY/Imagens/WIN_20230831_22_23_23_Pro.jpg')    # moto (not working)
    
    processamento_roi = preProcessamentoRoi()

    ocrImagePlate()
    
