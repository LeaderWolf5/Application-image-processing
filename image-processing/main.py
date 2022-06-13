from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication,QMessageBox,QFileDialog
from PyQt5.uic import loadUi
import sys
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from skimage.util import random_noise

class LoadQt(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('S.ui',self)
        self.setWindowIcon(QtGui.QIcon('image/icon.png'))
        self.setWindowTitle('H2Team')
        self.image = None

        # Kết nối các ation trong File
        self.actionOpen_File.triggered.connect(self.Open_File)
        self.actionSave_File.triggered.connect(self.Save_File)
        self.actionExit.triggered.connect(self.Exit)
        # Kết nôi các action trong nâng cấp ảnh
        # Các phép toán điểm ảnh
        self.action_Daoanh.triggered.connect(self.Dao_Anh)
        self.action_Catng.triggered.connect(self.Cat_Nguong)
        self.action_Gamma.triggered.connect(self.BD_gamma)
        # Lọc ảnh
        self.action_locgau.triggered.connect(self.Loc_Gaussian)
        self.action_Tv.triggered.connect(self.Loc_Median)
        self.action_loclap.triggered.connect(self.Loc_Laplace)
        # Kỹ thuật histogram
        self.action_cbhist.triggered.connect(self.CB_hist)
        self.action_histanh.triggered.connect(self.Hist_anh)
        # Action nhiễu ảnh
        self.action_nhieugau.triggered.connect(self.Nhieu_Gaussian)
        self.action_nhieumt.triggered.connect(self.Nhieu_MT)
        # Kết nối các button
        self.dial.valueChanged.connect(self.Quay_Anh)
        self.pt_90.clicked.connect(self.Xoay_Anh90)
        self.pt_axam.clicked.connect(self.Anh_Xam)
        self.pt_reset.clicked.connect(self.Reset)
        self.sl_tll.valueChanged.connect(self.Ti_leloc)
        # Cài đặt
        self.action_pt.triggered.connect(self.Zoom_in)
        self.action_tn.triggered.connect(self.Zoom_out)
        self.action_den.triggered.connect(lambda: self.change('#14618A'))
        self.action_trang.triggered.connect(lambda: self.change('thistle'))
        self.action_xanh.triggered.connect(lambda: self.change('azure'))
        # Kết nối giới thiệu
        self.action_ud.triggered.connect(self.About)
    @pyqtSlot()
    def loadImage(self, fname):
        self.image = cv.imread(fname)
        self.tmp = self.image
        self.displayImage()
    def displayImage(self, window=1):
        qformat = QImage.Format_Indexed8

        if len(self.image.shape) == 3:
            if (self.image.shape[2]) == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(self.image, self.image.shape[1], self.image.shape[0], self.image.strides[0], qformat)
        img = img.rgbSwapped()  # chuyển đổi hiệu quả một ảnh RGB thành một ảnh BGR.
        if window == 1:
            self.img_lb1.setPixmap(QPixmap.fromImage(img))
            self.img_lb1.setAlignment(
                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)  # căn chỉnh vị trí xuất hiện của hình trên lable
        if window == 2:
            self.img_lb2.setPixmap(QPixmap.fromImage(img))
            self.img_lb2.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
# Xử lý toolbar File
    def Open_File(self):
        fname, filter = QFileDialog.getOpenFileName(self, 'Open File', '',"Image Files (*)")
        if fname:
            self.loadImage(fname)
        else:
            print("Invalid Image")

    def Save_File(self):
        fname, filter = QFileDialog.getSaveFileName(self, 'Save File', "D:\python\Xulyanh\DA5\image",filter="JPG(*.jpg);;PNG(*.png);;All File(*)")
        if fname:
            cv.imwrite(fname, self.image)  # Lưu trữ ảnh
            print("Error")
    def Exit(self):
        mes = QMessageBox.question(self, 'Exit','Bạn muốn thoát ứng dụng?', QMessageBox.Yes | QMessageBox.No)
        if mes == QMessageBox.Yes:
            print('Ok,Hẹn gặp lại bạn sau!')
            self.close()
        else:
            print('No')
# Xử lý nâng cấp ảnh
    #Các phép toán điểm ảnh
    def Dao_Anh(self):
        self.image = self.tmp
        self.image = ~self.image
        self.displayImage(2)
    def Cat_Nguong(self):
        self.image = self.tmp
        grayscaled = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
        ret,threshold = cv.threshold(grayscaled, 125, 255, cv.THRESH_BINARY)
        self.image = threshold
        self.displayImage(2)
    def BD_gamma(self):
        self.image = self.tmp
        # gamma < 1 => chuyển ảnh về phía tối hơn
        # gamma > 1 => chuyển đổi ảnh về phía sáng hơn
        gamma = 0.5
        invGamma = 1.0 / gamma
        # Xây dựng bảnh tra cứu các giá trị pixel[0,255] thành các giá trị gamma được điều chỉnh
        table = np.array([((i / 255.0) ** invGamma) * 255
                for i in np.arange(0, 256)]).astype("uint8")
        # Áp dụng hiệu chỉnh gamma bằng cách sử dụng bảng tra cứu
        self.image = cv.LUT(self.image,table)
        self.displayImage(2)
    # Kỹ thuật histogram
    def CB_hist(self):
        self.image = self.tmp
        # Chuyển đổi ảnh sang thang độ xám
        grayImg = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
        equalImg = cv.equalizeHist(grayImg)
        self.image = equalImg
        self.displayImage(2)
    def Hist_anh(self):
        self.image = self.tmp
        '''
            Chức năng calchist chứa các giá trị
                + ảnh
                + Tính toán biểu đồ của thang độ xám(0, còn nếu màu RGB thì[0,1,2])
                + mặt nạ
                + histsize
                +ranges
        '''
        hist = cv.calcHist([self.image], [0], None, [256], [0, 256])
        self.image = hist
        plt.plot(self.image)
        plt.show()
        self.displayImage(2)
#===========================================================================
# Xử lý lọc ảnh
    def Loc_Gaussian(self):
        self.image = self.tmp
        # một bộ lọc gau có dạng (img, ksize(kích thược kernel), độ lệch chuẩn)
        self.image = cv.GaussianBlur(self.image, (5, 5), 0)
        self.displayImage(2)
    def Loc_Median(self):
        self.image = self.tmp
        self.image = cv.medianBlur(self.image,5)
        self.displayImage(2)
    def Loc_Laplace(self):
        self.image = self.tmp
        #ảnh đầu vào là CV_8U chúng ta thường xác định độ sâu cho ảnh đầu ra
        #là CV_16S để tránh tràn ảnh
        self.image = cv.Laplacian(self.image,cv.CV_16S,ksize=5)
        self.displayImage(2)
# ===========================================================================
# Nhiễu ảnh
    def Nhieu_Gaussian(self):
        self.image = self.tmp
        # Sử dụng ramdom_noise từ thư viện skitlearn
        gauss = random_noise(self.image,mode='gaussian',seed=None,clip=True)
        noise_gauss = self.image + gauss
        self.image = noise_gauss
        self.displayImage(2)
    def Nhieu_MT(self):
        self.image = self.tmp
        s_vs_p = 0.2
        amount = 0.008
        out = np.copy(self.image)
        # Salt noise
        num_salt = np.ceil(amount * self.image.size * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt))
                  for i in self.image.shape]
        out[coords[0], coords[1], :] = 255
         #Pepper mode
        num_pepper = np.ceil(amount * self.image.size * (1.0 - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper))
                  for i in self.image.shape]
        out[coords[0], coords[1], :] = 0
        self.image = out
        self.displayImage(2)
#===========================================================================
# Xử lý các button
    def Quay_Anh(self):
        h , w = self.image.shape[:2]
        # lấy tọa độ tâm để tạo ma trận quay 2D
        center = (w//2,h//2)
        #scale là hệ số tỉ lệ đẳng hướng giúp chia tỉ lệ hình ảnh lên hoặc xuống theo giá trị đã được cung cấp
        rotate_mt = cv.getRotationMatrix2D(center = center, angle = 45 , scale=1.0)
        rotate_img = cv.warpAffine(self.image, M = rotate_mt , dsize=(h,w))
        self.image = rotate_img
        self.displayImage(2)
    def Xoay_Anh90(self):
        rows, cols = self.image.shape[:2]
        M = cv.getRotationMatrix2D((cols / 2, rows / 2), 90, 1)  # thay đổi chiều của ảnh
        self.image = cv.warpAffine(self.image, M, (cols, rows))
        self.displayImage(2)
    def Reset(self):
        self.image = self.tmp
        self.displayImage(2)
    def Anh_Xam(self):
        self.image = self.tmp
        self.image = cv.cvtColor(self.image,cv.COLOR_BGR2GRAY)
        self.displayImage(2)
    def Ti_leloc(self,c):
        self.image = self.tmp
        self.image = cv.GaussianBlur(self.image, (5, 5), c)
        self.displayImage(2)
# ===========================================================================
# Cài đặt
    def Zoom_in(self):
        self.image = cv.resize(self.image, None, fx=1.5, fy=1.5, interpolation=cv.INTER_CUBIC)
        self.displayImage(2)
    def Zoom_out(self):
        self.image = cv.resize(self.image, None, fx=0.75, fy=0.75, interpolation=cv.INTER_CUBIC)
        self.displayImage(2)
    def change(self,color):
        self.setStyleSheet(f"background-color: {color};")
#===========================================================================
    def About(self):
        QMessageBox.about(self,'Ứng dụng xử lý ảnh desktop',
                          'Sinh viên thực hiện: Nguyễn Văn Hưng'
                          '\nLớp: 19IT6 '
                          ' \nGiảng viên hướng dẫn : TS. Nguyễn Hoàng Hải')
# chạy app
app = QApplication(sys.argv)
window = LoadQt()
window.show()
sys.exit(app.exec_())


