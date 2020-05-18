import math
import glob
import sys
import cv2 as cv
import cv2
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, QBasicTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
from matplotlib import pyplot as plt

def proses_hitung(dagingImg):
    jmlTiapPixel = cv2.calcHist([dagingImg], [0], None, [256], [0, 256])
    jumlahpixel = sum(jmlTiapPixel)
    probabilitas = jmlTiapPixel / jumlahpixel
    return  probabilitas

def meanGray(probabilitas):
    rata2 = []
    i = 0
    while (i < 256):
        rata2.insert(i, (i * probabilitas[i]))
        i = i + 1
    rata2 = sum(rata2)
    print('Mean : ',rata2)
    return rata2

def varianceGray(probabilitas,rata2):
    varians = []
    i = 0
    while (i < 256):
        varians.insert(i, ((i - rata2) ** 2) * (probabilitas[i]))
        i = i + 1
    varians = sum(varians)
    print('Varian : ',varians)
    return varians

def skewnessGray(probabilitas,rata2,varians):
    skew = []
    i = 0
    while (i < 256):
        skew.insert(i, ((i - rata2) ** 3) * (probabilitas[i]))
        i = i + 1
    skew = (sum(skew)) / varians ** 1.5
    print('Skewness : ',skew)
    return skew

def kurtosisGray(rata2,probabilitas,varians):
    kurto = []
    i = 0
    while (i < 256):
        kurto.insert(i, ((i - rata2) ** 4) * (probabilitas[i]) - 3)
        i = i + 1
    kurto = (sum(kurto)) / (varians ** 2)
    print('Kurtosis : ',kurto)
    return kurto

def entrophyGray(probabilitas):
    entro = []
    i = 0
    while (i < 256):
        if probabilitas[i] == 0:
            i = i + 1
        else:
            entro.insert(i, (-((probabilitas[i]))) * (math.log(probabilitas[i]) / math.log(2)))
            i = i + 1
    entro = (sum(entro))
    print('Entrophy : ',entro)
    return entro
""" ================================================================================================================= """


def load_databaseBabi(rata2):
    jmlTiapPixel_dataBabi = []  # """ UNTUK DATA BABI DENGAN RATA RATA"""
    probabilitas_dataBabi = []
    rata2DataBabi = []
    ratababi = []
    euclidian_ratababi = []
    euclidian_ratababi_LABEL = []
    imagesBabi = [cv2.imread(file, cv2.IMREAD_GRAYSCALE) for file in
                  glob.glob("images/babi/*.jpg")]

    for a in range(0, 30):
        jmlTiapPixel_dataBabi.insert(a, (cv2.calcHist([imagesBabi[a]], [0], None, [256], [0, 256])))
        probabilitas_dataBabi.insert(a, (jmlTiapPixel_dataBabi[a] / sum(jmlTiapPixel_dataBabi[a])))
        for derjt in range(0, 255):
            ratababi.insert(derjt, (derjt * (probabilitas_dataBabi[a][derjt])))
        rata2DataBabi.insert(a, sum(ratababi[0:255]))
        euclidian_ratababi.insert(a, (math.sqrt((rata2DataBabi[a] - rata2) ** 2)))
    for gambar in range(0, 30):
        euclidian_ratababi_LABEL.insert(gambar, ((euclidian_ratababi[gambar]), 'babi'))  # kasih label babi
    return euclidian_ratababi_LABEL

def load_databaseSapi(rata2):
    jmlTiapPixel_dataSapi = []  # UNTUK DATA SAPI DENGAN RATA - RATA
    probabilitas_dataSapi = []
    rata2DataSapi = []
    ratasapi = []
    euclidian_ratasapi = []
    euclidian_ratasapi_LABEL = []

    imagesSapi = [cv2.imread(file, cv2.IMREAD_GRAYSCALE) for file in
                  glob.glob("images/sapi/*.jpg")]
    for a in range(0, 30):
        jmlTiapPixel_dataSapi.insert(a, (cv2.calcHist([imagesSapi[a]], [0], None, [256], [0, 256])))
        probabilitas_dataSapi.insert(a, (jmlTiapPixel_dataSapi[a] / sum(jmlTiapPixel_dataSapi[a])))
        for derjt in range(0, 255):
            ratasapi.insert(derjt, (derjt * (probabilitas_dataSapi[a][derjt])))
        rata2DataSapi.insert(a, sum(ratasapi[0:255]))
        euclidian_ratasapi.insert(a, (math.sqrt((rata2DataSapi[a] - rata2) ** 2)))

    for gambar in range(0,30):
        euclidian_ratasapi_LABEL.insert(gambar, ((euclidian_ratasapi[gambar]), 'sapi'))
    return euclidian_ratasapi_LABEL


def urut_hasil(euclidian_ratababi_LABEL,euclidian_ratasapi_LABEL,k):
    print('')
    ngurutinData = []
    s = 29
    for t in range(0, 60):
        if t < 30:
            ngurutinData.insert(t, (euclidian_ratababi_LABEL[t]))
        else:
            ngurutinData.insert(t, (euclidian_ratasapi_LABEL[s]))
            s = s - 1
        ngurutinData.sort()

    label_nomer = []
    print('N G U R U T - G R E Y S C L E')
    print('============================= MEAN')
    for t in range(0, 60):
        label_nomer.insert(t, (t + 1, (ngurutinData[t])))
        print(label_nomer[t])

    print('')
    print('K = '+str(k))
    t = 0
    #k = 8
    babie = 0
    sapie = 0

    while t < k:
        if label_nomer[t][1][1] == ('babi'):
            babie = babie + 1
            t = t + 1
        else:
            sapie = sapie + 1
            t = t + 1

    print('')
    print('Jumlah yg bertetangga sama Sapi = ', sapie)
    print('Jumlah yg bertetangga sama Babi = ', babie)
    if sapie > babie:
        print('')
        print('Hasilnya : SAPI')
        hasil = ("     S A P I")
    else:
        print('')
        print('Hasilnya : BABI')
        hasil = ("     B A B I")
    return hasil

""" ================================================================================================================"""


def canny_method(dagingIMGCanny):
    jmlTiapPixel = cv2.calcHist([dagingIMGCanny], [0], None, [256], [0, 256])
    return jmlTiapPixel

def loadDBSapiCanny(jmlTiapPixel):
    jmlTiapPixel_dataSapiCanny = []  # CANNY DATA SAPI
    imagesSapi_Canny = []
    euclidian_Cannysapi = []
    euclidian_Cannysapi_LABEL = []
    imagesSapi = [cv2.imread(file, cv2.IMREAD_GRAYSCALE)
                  for file in glob.glob("images/sapi/*.jpg")]

    for a in range(0, 30):
        imagesSapi_Canny.insert(a, (cv2.Canny(imagesSapi[a], 100, 200)))
        jmlTiapPixel_dataSapiCanny.insert(a, (
            cv2.calcHist([imagesSapi_Canny[a]], [0], None, [256], [0, 256])))  # hitung hisogram
        euclidian_Cannysapi.insert(a, (math.sqrt((jmlTiapPixel_dataSapiCanny[a][255] - jmlTiapPixel[255]) ** 2)))

    for gambar in range(0, 30):
        euclidian_Cannysapi_LABEL.insert(gambar, ((euclidian_Cannysapi[gambar]), 'sapi'))  # kasih label babi
    return euclidian_Cannysapi_LABEL

def loadDBBabiCanny(jmlTiapPixel):
    jmlTiapPixel_dataBabiCanny = []  # CANNY DATA BABI
    imagesBabi_Canny = []
    euclidian_Cannybabi = []
    euclidian_Cannybabi_LABEL = []
    imagesBabi = [cv2.imread(file, cv2.IMREAD_GRAYSCALE) for file in glob.glob("images/babi/*.jpg")]

    for a in range(0, 30):
        imagesBabi_Canny.insert(a, (cv2.Canny(imagesBabi[a], 100, 200)))
        jmlTiapPixel_dataBabiCanny.insert(a, (cv2.calcHist([imagesBabi_Canny[a]], [0], None, [256], [0, 256])))
        euclidian_Cannybabi.insert(a, (math.sqrt((jmlTiapPixel_dataBabiCanny[a][255] - jmlTiapPixel[255]) ** 2)))

    for gambar in range(0, 30):
        euclidian_Cannybabi_LABEL.insert(gambar, ((euclidian_Cannybabi[gambar]), 'babi'))  # kasih label babi
    return euclidian_Cannybabi_LABEL

def urut_hasilCanny(euclidian_Cannybabi_LABEL,euclidian_Cannysapi_LABEL,k):
    print("")
    print("N G U R U T - C A N N Y")
    print("=======================")
    ngurutin = []
    s = 29
    for t in range(0, 60):
        if t < 30:
            ngurutin.insert(t, (euclidian_Cannybabi_LABEL[t]))
        else:
            ngurutin.insert(t, (euclidian_Cannysapi_LABEL[s]))
            s = s - 1
    ngurutin.sort()
    label_nomer = []
    for t in range(0, 60):
        label_nomer.insert(t, (t + 1, (ngurutin[t])))
        print(label_nomer[t])

    print('K = '+str(k))
    t = 0
    babie = 0
    sapie = 0

    while t < k:
        if label_nomer[t][1][1] == ('babi'):
            babie = babie + 1
            t = t + 1
        else:
            sapie = sapie + 1
            t = t + 1
    print('Jumlah yg bertetangga sama Sapi = ', sapie)
    print('Jumlah yg bertetangga sama Babi = ', babie)
    if sapie > babie:
        print('Hasil    : Sapi')
        hasil = ("       S A P I")
    else:
        print('Hasil    : Babi')
        hasil = ("       B A B I")
    return hasil

""" ============================================================================================================== """

def histogram(dagingImg, cannyCitra):
    plt.figure('Histogram G R E Y',figsize=(4,3))
    plt.hist(dagingImg.ravel(), 256, [0, 256])
    plt.savefig("images/histogram/histogram.jpg")
    plt.title('G R E Y')

    plt.figure('Histogram C A N N Y',figsize=(4,3))
    plt.hist(cannyCitra.ravel(), 256, [0, 256])
    plt.savefig("images/histogram/histogramCanny.jpg")
    plt.title('C A N N Y')

class MainApp(QDialog):
    def __init__(self):
        super(MainApp,self).__init__()
        loadUi('MInterface3.ui',self)
        self.image = None
        self.btn_loadGambar.clicked.connect(self.loadClicked)
        self.btn_ProsesExec.clicked.connect(self.startProgress)
        self.btn_histogramShow.clicked.connect(self.histogramClicked)
        self.progressBar.hide()
        self.timer = QBasicTimer()
        self.progressBar.setValue(0)
        self.step = 0
        self.btn_histogramShow.setEnabled(False)
        self.btn_ProsesExec.setEnabled(False)
        self.slider_K.valueChanged.connect(self.gantiValue)
        self.edt_nilaiK.textChanged[str].connect(self.gantiValueSlider)

    def gantiValueSlider(self):
        if self.edt_nilaiK.text() == '':
            s = 0
            self.slider_K.setValue(s)
        else:
            self.slider_K.setValue(int(self.edt_nilaiK.text()))

        self.btn_ProsesExec.setEnabled(True)
        if self.btn_ProsesExec.setEnabled == True:
            self.btn_ProsesExec.setText('Proses')

    def gantiValue(self):
        s = self.slider_K.value()
        self.edt_nilaiK.setText(str(s))
        self.btn_ProsesExec.setEnabled(True)

    @pyqtSlot()
    def startProgress(self):
        self.progressBar.show()
        if self.timer.isActive():
            self.timer.stop()
            self.btn_ProsesExec.setText('Proses')
        else:
            self.timer.start(100,self)
            self.btn_ProsesExec.setText('Tunggu ...')


    @pyqtSlot()
    def timerEvent(self, event):
        if (fname != 0):
            if self.step >= 100:
                self.timer.stop()
                self.btn_ProsesExec.setText('Proses')
                self.progressBar.hide()
                k = self.slider_K.value()
                citra_awal = self.image
                gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY) if len(self.image.shape) >= 3 else self.image
                self.image = cv2.Canny(gray, 100, 200)
                self.displayImage(2)
                cannyCitra = self.image
                dagingImg = gray
                histogram(dagingImg, cannyCitra)
                TempProbabilitas = proses_hitung(dagingImg)
                TempRata2 = meanGray(TempProbabilitas)
                TempDBBabi = load_databaseBabi(TempRata2)
                TempDBSapi = load_databaseSapi(TempRata2)

                TempHasilMean = urut_hasil(TempDBBabi, TempDBSapi,k)

                arr = []
                stringTempRata2 = str(TempRata2)
                arr += stringTempRata2
                arr.remove('[')
                arr.remove(']')
                test = ''.join(map(str, arr))
                self.edt_meanGray.setText("" + str(test))


                dagingIMGCanny = cv2.Canny(dagingImg, 100, 200)
                TempJMLtiapPixel = canny_method(dagingIMGCanny)
                TempDBCannyBabi = loadDBBabiCanny(TempJMLtiapPixel)
                TempDBCannySapi = loadDBSapiCanny(TempJMLtiapPixel)
                TempHasilCanny = urut_hasilCanny(TempDBCannyBabi, TempDBCannySapi,k)

                self.edt_hasilProses.setText("" + str(TempHasilCanny))
                if str(TempHasilCanny) == ("       B A B I"):
                    self.edt_hasilProses.setStyleSheet("color: rgb(255, 0, 0);")
                else:
                    self.edt_hasilProses.setStyleSheet("color: rgb(29, 200, 20);")

                self.edt_hasilMean.setText("" + str(TempHasilMean))
                if str(TempHasilMean) == ("     B A B I"):
                    self.edt_hasilMean.setStyleSheet("color: rgb(255, 0, 0);")
                else:
                    self.edt_hasilMean.setStyleSheet("color: rgb(29, 200, 20);")


                arr = []
                stringTempRata2 = str(TempJMLtiapPixel[255])
                arr += stringTempRata2
                arr.remove('[')
                arr.remove(']')
                test = ''.join(map(str, arr))
                self.edt_PixelCanny.setText("" + str(test))
                self.image = dagingImg
                self.displayImage(3)

                citraHistogram = cv2.imread("images/histogram/histogram.jpg")
                height, width = citraHistogram.shape[:2]
                res = cv.resize(citraHistogram, (int(width / 1.8), int(height / 1.8)), interpolation=cv.INTER_AREA)
                self.image = res
                self.displayImage(4)

                citraHistogramCanny = cv2.imread("images/histogram/histogramCanny.jpg")
                height, width = citraHistogramCanny.shape[:2]
                resCanny = cv.resize(citraHistogramCanny, (int(width / 2), int(height / 2)),interpolation=cv.INTER_AREA)
                self.image = resCanny
                self.displayImage(5)
                print(fname)
                self.progressBar.setValue(0)
                self.step = 0
                self.btn_ProsesExec.setEnabled(False)
                self.btn_histogramShow.setEnabled(True)

                self.image = citra_awal
                plt.cla

        else:
            print('Load gambar terlebih dahulu !')
            self.step = 100
            self.timer.stop()

        self.step = self.step + 49
        self.progressBar.setValue(self.step)


    @pyqtSlot()
    def histogramClicked(self):
        plt.show()

    @pyqtSlot()
    def loadClicked(self):
        global fname

        fname = 0
        print(fname)
        self.btn_ProsesExec.setText("Proses")
        fname, filter = QFileDialog.getOpenFileName(self,'Open File','C:\\',"Image Files (*.jpg)")
        if fname:
            self.loadImage(fname)
            self.edt_meanGray.setText("")
            self.edt_hasilMean.setText("")
            self.edt_nilaiK.setText(str(self.slider_K.value()))
            self.edt_PixelCanny.setText("")
            self.edt_hasilProses.setText("")
            self.progressBar.setValue(0)
            self.img_histCanny.clear()
            self.img_histGray.clear()
            self.img_Grayscale.clear()
            self.img_Canny.clear()
            self.btn_ProsesExec.setEnabled(True)
            self.btn_histogramShow.setEnabled(False)
        else:
            print('INVALID IMAGE')

    @pyqtSlot()
    def saveClicked(self):
        fname, filter = QFileDialog.getSaveFileName(self,'Save File','C:\\',"Image Files (*.jpg)")
        if fname:
            cv2.imwrite(fname,self.image)
        else:
            print('Error')

    def loadImage(self,fname):
        self.image = cv2.imread(fname, cv2.IMREAD_COLOR)
        self.displayImage(1)

    def displayImage(self,window = 1):
        qformat = QImage.Format_Indexed8
        if len(self.image.shape) == 3: #rows[0],cols[1],channels[2]
            if(self.image.shape[2]) == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(self.image,self.image.shape[1],self.image.shape[0],self.image.strides[0],qformat)
        #BGR > RGB
        img = img.rgbSwapped()
        if window == 1:
            self.img_Load.setPixmap(QPixmap.fromImage(img))
            self.img_Load.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        if window ==2:
            self.img_Canny.setPixmap(QPixmap.fromImage(img))
            self.img_Canny.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        if window ==3:
            self.img_Grayscale.setPixmap(QPixmap.fromImage(img))
            self.img_Grayscale.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        if window ==4:
            self.img_histGray.setPixmap(QPixmap.fromImage(img))
            self.img_histGray.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        if window ==5:
            self.img_histCanny.setPixmap(QPixmap.fromImage(img))
            self.img_histCanny.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

if __name__=='__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    window.setWindowTitle('Applikasi PCD')
    window.show()
    sys.exit(app.exec_())