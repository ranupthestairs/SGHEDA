import json
import sys
import webbrowser
import traceback

## UI
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMainWindow, QTabWidget, \
    QHBoxLayout, QSizePolicy, QComboBox, QFileDialog, QScrollArea, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QCursor, QMovie
from PyQt5.QtCore import Qt, QSize, QTimer, QPoint

from buttonclass import ImageButton, ExtraButton, SquareButton, ExitButton, MainButton1, ImageButton1, TextButton
from firstpageclass import FirstPageClass
from inputformclass import InputForm, InputDescription, CustomQTextEdit, LicenseForm, PersonalForm
from labelclass import IntroLabel1, TickerLabel, IntroLabel3
from notificationclass import CustomMessageBox, ExitNotification
import pyqtgraph as pg

## Calculation
import numpy as np
from scipy.special import erfc
from scipy.integrate import dblquad
import math
from decimal import *
getcontext().prec = 4

class DesignClass(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.license_info = None
        self.plt_gfunction = None
        self.parent = parent
        self.tabstack = []
        self.dict = {}
        self.designpath = './Logs/designpath.json'
        self.num_design = 5
        self.num_analysis = 4
        self.currentgldpath = ''

        # set the size of window
        self.setFixedSize(1210, 790)

        # Set the background color of the main window
        self.setStyleSheet("background-color: #1F2843; border: none")
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        # add all widgets

        self.left_widget = QWidget()
        self.left_widget.setStyleSheet("""
            background-color: #2C3751;
            border-radius: 10px;
        """)

        # Image button
        self.btn_home = ImageButton(self.left_widget, './Images/logo03_glowed_white.png')
        self.btn_home.move(20, 20)
        self.btn_home.clicked.connect(self.button0)

        self.combobox_selection = QComboBox(self.left_widget)
        self.icon_design = QIcon('./Images/design.png')
        self.icon_analysis = QIcon('./Images/analysis02.png')
        self.combobox_selection.addItem(self.icon_design, ' Design')
        self.combobox_selection.addItem(self.icon_analysis, 'Analysis ')
        self.combobox_selection.resize(100, 30)
        self.combobox_selection.setCursor(QCursor(Qt.PointingHandCursor))
        self.combobox_selection.setStyleSheet("""            
             QComboBox {
                color: #7C8AA7;
                background-color: #2C3751;
                selection-background-color: red;
                padding: 1px 1px 1px 1px;
                min-width: 0em;
                font-size: 16px;
            }
            
            QComboBox:hover {
                color: #2978FA;
            }
            
            QComboBox::drop-down {
                width: 10px;
                border: none;
            }
            
            QComboBox::down-arrow {
                border: 0px;
                background-image-width: 30px;
                border-image: url(./Images/down.png);
            }
        """
                                              )
        self.combobox_selection.currentIndexChanged.connect(self.combobox_selection_changed)
        self.combobox_selection.move(20, 155)

        self.label_num = QPushButton(self.left_widget)
        self.label_num_icon = QIcon('./Images/remain01.png')
        self.label_num.setIcon(self.label_num_icon)
        self.label_num.setIconSize(QSize(25, 25))
        self.label_num.setText(' ' + str(self.num_design))
        self.label_num.setGeometry(130, 155, 60, 30)
        self.label_num.setStyleSheet("""
            QPushButton {
                background-color: #374866;
                color: white;
                font-size: 16px;
                border-radius: 13px;
                transition: background-color 0.9s ease-in-out;
            }
            QPushButton:hover {
                background-color: #5A6B90;
            }
        """)
        self.label_num.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.btn_1 = SquareButton(self.left_widget, './Images/configuration01_b.png', './Images/configuration01.png')
        self.btn_1.setText(' System Design ')
        self.btn_1.setGeometry(0, 200, 212, 50)
        self.btn_2 = SquareButton(self.left_widget, './Images/fluid02_b.png', './Images/fluid02.png')
        self.btn_2.setText(' Fluid Properties ')
        self.btn_2.setGeometry(0, 250, 212, 50)
        self.btn_3 = SquareButton(self.left_widget, './Images/soil01_b.png', './Images/soil01.png')
        self.btn_3.setText(' Soil Properties ')
        self.btn_3.setGeometry(0, 300, 212, 50)
        self.btn_4 = SquareButton(self.left_widget, './Images/pipe01_b.png', './Images/pipe01.png')
        self.btn_4.setText(' Pipe Configuration ')
        self.btn_4.setGeometry(0, 350, 212, 50)
        self.btn_5 = SquareButton(self.left_widget, './Images/power02_b.png', './Images/power02.png')
        self.btn_5.setText(' Pump Info ')
        self.btn_5.setGeometry(0, 400, 212, 50)
        self.btn_6 = SquareButton(self.left_widget, './Images/result01_b.png', './Images/result01.png')
        self.btn_6.setText(' Design Result')
        self.btn_6.setGeometry(0, 450, 212, 50)
        self.btn_7 = SquareButton(self.left_widget, './Images/analysis11_b.png', './Images/analysis11.png')
        self.btn_7.setText(' Analysis')
        self.btn_7.setGeometry(0, 500, 212, 50)

        self.btn_1_ticker = TickerLabel(self.left_widget)
        self.btn_1_ticker.setGeometry(180, 210, 30, 30)
        self.btn_1_ticker.hide()

        self.btn_2_ticker = TickerLabel(self.left_widget)
        self.btn_2_ticker.setGeometry(180, 260, 30, 30)
        self.btn_2_ticker.hide()

        self.btn_3_ticker = TickerLabel(self.left_widget)
        self.btn_3_ticker.setGeometry(180, 310, 30, 30)
        self.btn_3_ticker.hide()

        self.btn_4_ticker = TickerLabel(self.left_widget)
        self.btn_4_ticker.setGeometry(180, 360, 30, 30)
        self.btn_4_ticker.hide()

        self.btn_5_ticker = TickerLabel(self.left_widget)
        self.btn_5_ticker.setGeometry(180, 410, 30, 30)
        self.btn_5_ticker.hide()

        self.btn_6_ticker = TickerLabel(self.left_widget)
        self.btn_6_ticker.setGeometry(180, 460, 30, 30)
        self.btn_6_ticker.hide()

        self.slide_label = QLabel(self.left_widget)
        self.slide_label.setStyleSheet('background-color: #31A8FC')
        self.slide_label.resize(5, 50)
        self.slide_label.hide()

        self.btn_1.clicked.connect(self.button1)
        self.btn_2.clicked.connect(self.button2)
        self.btn_3.clicked.connect(self.button3)
        self.btn_4.clicked.connect(self.button4)
        self.btn_5.clicked.connect(self.button5)
        self.btn_6.clicked.connect(self.button6)
        self.btn_7.clicked.connect(self.button7)

        self.btn_setting = ExtraButton(self.left_widget, './Images/setting_b.png', './Images/setting.png')
        self.btn_setting.setText(' Settings')
        self.btn_setting.setGeometry(0, 590, 200, 50)
        self.btn_setting.clicked.connect(self.btnsetting)

        self.line = QLabel(self.left_widget)
        self.line.setStyleSheet('''
            QLabel {background-color: #ACACBF;;}
        ''')
        self.line.setGeometry(25, 640, 150, 1)


        self.btn_feedback = TextButton(self.left_widget)
        self.btn_feedback.setText(' Feedback')
        self.btn_feedback.clicked.connect(self.redirect_to_feedback)
        self.btn_feedback.setGeometry(50, 650, 100, 20)

        self.btn_help = TextButton(self.left_widget)
        self.btn_help.setText('  Help  ')
        self.btn_help.clicked.connect(self.redirect_to_help)
        self.btn_help.setGeometry(50, 675, 100, 20)


        self.btn_exit = ExitButton(self.left_widget, './Images/end01.png', './Images/end01_r.png')
        self.btn_exit.setText(' Exit')
        self.btn_exit.setGeometry(0, 695, 200, 50)
        self.btn_exit.clicked.connect(self.btnexit)

        # add tabs
        self.tab1 = self.ui1()
        self.tab2 = self.ui2()
        self.tab3 = self.ui3()
        self.tab4 = self.ui4()
        self.tab5 = self.ui5()
        self.tab6 = self.ui6()
        self.tab7 = self.ui7()
        self.tab8 = self.ui8()
        self.tab9 = self.ui9()

        # right widget
        self.right_widget = QTabWidget()
        self.right_widget.tabBar().setObjectName("mainTab")

        self.right_widget.addTab(self.tab1, '')
        self.right_widget.addTab(self.tab2, '')
        self.right_widget.addTab(self.tab3, '')
        self.right_widget.addTab(self.tab4, '')
        self.right_widget.addTab(self.tab5, '')
        self.right_widget.addTab(self.tab6, '')
        self.right_widget.addTab(self.tab7, '')
        self.right_widget.addTab(self.tab8, '')
        self.right_widget.addTab(self.tab9, '')

        self.tab1.loadtable()
        self.right_widget.setCurrentIndex(0)

        self.right_widget.setStyleSheet('''
            QTabWidget::pane {
                border: none;
            }
        
            QTabBar::tab{
                width: 0;
                height: 0; 
                margin: 0; 
                padding: 0; 
                border: none;
            }
        ''')

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.left_widget)
        main_layout.addWidget(self.right_widget)
        main_layout.setStretch(0, 22)
        main_layout.setStretch(1, 100)
        self.setLayout(main_layout)

    #     self.is_dragging = False
    #     self.offset = QPoint()
    #
    # def mousePressEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         self.is_dragging = True
    #         self.offset = event.pos()
    #
    # def mouseMoveEvent(self, event):
    #     if self.is_dragging:
    #         self.move(event.globalPos() - self.offset)
    #
    # def mouseReleaseEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         self.is_dragging = False
    # -----------------
    # ticker button
    def tickerbutton(self):
        currentIndex = self.right_widget.currentIndex()
        if self.right_widget.currentIndex() == 0:
            self.slide_label.hide()
        else:
            self.slide_label.move(0, 200 + 50 * (currentIndex - 1))
            self.slide_label.show()

    # combobox
    def combobox_selection_changed(self):
        selected_text = self.combobox_selection.currentText()
        print(selected_text)
        if selected_text == ' Design':
            self.label_num.setText(' ' + str(self.num_design))
        else:
            self.label_num.setText(' ' + str(self.num_analysis))

    # -----------------
    # buttons
    def button0(self):
        print("button0")
        self.right_widget.clear()
        self.tab1 = self.ui1()
        self.tab2 = self.ui2()
        self.tab3 = self.ui3()
        self.tab4 = self.ui4()
        self.tab5 = self.ui5()
        self.tab6 = self.ui6()
        self.tab7 = self.ui7()
        self.tab8 = self.ui8()
        self.tab9 = self.ui9()

        self.right_widget.addTab(self.tab1, '')
        self.right_widget.addTab(self.tab2, '')
        self.right_widget.addTab(self.tab3, '')
        self.right_widget.addTab(self.tab4, '')
        self.right_widget.addTab(self.tab5, '')
        self.right_widget.addTab(self.tab6, '')
        self.right_widget.addTab(self.tab7, '')
        self.right_widget.addTab(self.tab8, '')
        self.right_widget.addTab(self.tab9, '')

        self.tab1.loadtable()
        self.right_widget.setCurrentIndex(0)
        self.tickerbutton()
        self.dict = {}
        self.btn_1_ticker.hide()
        self.btn_2_ticker.hide()
        self.btn_3_ticker.hide()
        self.btn_4_ticker.hide()
        self.btn_5_ticker.hide()
        self.btn_6_ticker.hide()

    def button1(self):
        self.right_widget.setCurrentIndex(1)
        self.tickerbutton()

    def button2(self):
        self.right_widget.setCurrentIndex(2)
        self.tickerbutton()

    def button3(self):
        self.right_widget.setCurrentIndex(3)
        self.tickerbutton()

    def button4(self):
        self.right_widget.setCurrentIndex(4)
        self.tickerbutton()

    def button5(self):
        self.right_widget.setCurrentIndex(5)
        self.tickerbutton()

    def button6(self):
        self.right_widget.setCurrentIndex(6)
        self.tickerbutton()

    def button7(self):
        if len(self.dict.keys()) == 7:
            self.right_widget.setCurrentIndex(7)
            self.tickerbutton()
        else:
            icon = QIcon('./Images/logo03.png')
            custom_message_box = CustomMessageBox(icon, 'Custom Message', 'Please input design \n'
                                                                          '    parameter.', self)
            custom_message_box.setGeometry(900, 20, 300, 70)
            custom_message_box.show()
            print("notification")
    def btnsetting(self):
        self.right_widget.setCurrentIndex(8)
    # -----------------
    # pages

    def ui1(self):
        main = FirstPageClass('./Backgrounds/designbackground.png', self.designpath, self)
        main.loadtable()
        return main

    def ui2(self):
        #         System
        main = QWidget()
        label = IntroLabel1(main)
        label.setText("System")
        label.move(410, 30)

        self.data_form_systemdesign = ["System Design",
                                       ["Heat Load", "W", "lineedit", "2000"],
                                       ["Input Fluid Temperature", "dC", "lineedit", '60']]
        self.form_systemdesign = InputForm(main, self.data_form_systemdesign)
        self.form_systemdesign.move(240, 100)



        def uimovenext():
            print("uimovenext")
            dict = {}
            if self.form_fluidsystemdesign.getValidation():
                dict = self.form_fluidsystemdesign.getData()
            else:
                self.btn_1_ticker.hide()
                self.movenext()
                return False
            self.btn_1_ticker.show()
            self.dict["System"] = dict
            self.movenext()
            return True

        def uimoveprevious():
            self.moveprevious()

        def setData(data):
            self.form_fluidsystemdesign.setData(data['System'])

        btn_open = MainButton1(main)
        btn_open.setText(main.tr('Previous Step'))
        btn_open.move(200, 670)
        btn_open.resize(170, 55)
        btn_open.clicked.connect(uimoveprevious)

        btn_next = MainButton1(main)
        btn_next.setText(main.tr('Next Step'))
        btn_next.move(550, 670)
        btn_next.resize(170, 55)
        btn_next.clicked.connect(uimovenext)
        return main

    def ui3(self):
        #       Fluid
        main = QWidget()

        label = IntroLabel1(main)
        label.setText("Fluid")
        label.move(410, 30)

        self.data_form_fluidproperties = ["Fuild Properties",
                                     ["Fluid Type",
                                      ["Water", "Methanol", "Ethylene Glycol", "Propylene Glycol", "Sodium Chloride",
                                       "Calcium Chloride"], "combobox"],
                                     ["Viscosity", "Pa*s", "lineedit", "0.011"],
                                     ["Specific Heat", "K/(Kg*dC)", "lineedit", "3344"],
                                     ["Density", "Kg/m^3", "lineedit", "1100"]
                                     ]
        self.form_fluidproperties = InputForm(main, self.data_form_fluidproperties)
        self.form_fluidproperties.move(240, 100)


        def uimovenext():
            print("uimovenext")
            dict = {}
            if self.form_fluidproperties.getValidation():
                dict = self.form_fluidproperties.getData()
            else:
                self.btn_2_ticker.hide()
                self.movenext()
                return False

            self.dict["Fluid"] = dict
            self.btn_2_ticker.show()
            self.movenext()
            return True

        def uimoveprevious():
            self.moveprevious()

        btn_open = MainButton1(main)
        btn_open.setText(main.tr('Previous Step'))
        btn_open.move(200, 670)
        btn_open.resize(170, 55)
        btn_open.clicked.connect(uimoveprevious)

        btn_next = MainButton1(main)
        btn_next.setText(main.tr('Next Step'))
        btn_next.move(550, 670)
        btn_next.resize(170, 55)
        btn_next.clicked.connect(uimovenext)
        return main

    def ui4(self):
        # Soil
        main = QWidget()

        label = IntroLabel1(main)
        label.setText("Soil")
        label.move(425, 30)

        self.data_form_soilthermalproperties = ["Soil Thermal Properties",
                                    ["Thermal Conductivity", "W/(m*K)", "lineedit", "0.07"],
                                    ["Ground Temperature", "⁰C", "lineedit", '10']
                                 ]
        self.form_soilthermalproperties = InputForm(main, self.data_form_soilthermalproperties)
        self.form_soilthermalproperties.move(240, 100)

        def uimovenext():
            print("uimovenext")
            dict = {}
            if self.form_soilthermalproperties.getValidation():
                dict = self.form_soilthermalproperties.getData()
            else:
                self.btn_3_ticker.hide()
                self.movenext()
                return False

            self.dict["Soil"] = dict
            self.btn_3_ticker.show()
            self.movenext()
            return True

        def uimoveprevious():
            self.moveprevious()

        btn_open = MainButton1(main)
        btn_open.setText(main.tr('Previous Step'))
        btn_open.move(200, 670)
        btn_open.resize(170, 55)
        btn_open.clicked.connect(uimoveprevious)

        btn_next = MainButton1(main)
        btn_next.setText(main.tr('Next Step'))
        btn_next.move(550, 670)
        btn_next.resize(170, 55)
        btn_next.clicked.connect(uimovenext)

        return main

    def ui5(self):
        # Pipe
        main = QWidget()

        label = IntroLabel1(main)
        label.setText("Pipe")
        label.move(425, 30)

        self.data_form_pipeproperties = ["Pipe Properties",
                                    ["Pipe Size", ["3/4 in. (20mm)", "1 in. (25mm)", "1 1/4 in. (32mm)", "1 1/2 in. (40mm)"], "combobox"],
                                    ["Outer Diameter", "m", "lineedit", '0.021'],
                                    ["Inner Diameter", "m", "lineedit", '0.026'],
                                    ["Pipe Type", ["SDR11", "SDR11-OD", "SDR13.5", "SDR13.5-OD"], "combobox"],
                                    ["Flow Type", ["Turbulent", "Transition", "Laminar"], "combobox"],
                                    ["Pipe Conductivity", "W/(m*K)", "lineedit", '0.14']
                                  ]
        self.form_pipeproperties = InputForm(main, self.data_form_pipeproperties)
        self.form_pipeproperties.move(230, 100)

        self.data_form_pipeconfiguration = ["Pipe Configuration",
                                        ['Buried Depth', 'm', 'lineedit', '2.0']]
        self.form_pipeconfiguration = InputForm(main, self.data_form_pipeconfiguration)
        self.form_pipeconfiguration.move(270, 450)

        def uimovenext():
            print("uimovenext")
            dict = {}
            if self.form_pipeproperties.getValidation():
                dict = self.form_pipeproperties.getData()
            else:
                self.btn_4_ticker.hide()
                self.movenext()
                return False
            if self.form_pipeconfiguration.getValidation():
                dict.update(self.form_pipeconfiguration.getData())
            else:
                self.btn_4_ticker.hide()
                self.movenext()
                return False

            self.dict["Pipe"] = dict
            self.btn_4_ticker.show()
            self.movenext()
            return True

        def uimoveprevious():
            self.moveprevious()

        btn_open = MainButton1(main)
        btn_open.setText(main.tr('Previous Step'))
        btn_open.move(200, 670)
        btn_open.resize(170, 55)
        btn_open.clicked.connect(uimoveprevious)

        btn_next = MainButton1(main)
        btn_next.setText(main.tr('Next Step'))
        btn_next.move(550, 670)
        btn_next.resize(170, 55)
        btn_next.clicked.connect(uimovenext)

        return main

    def ui6(self):
        # Pump
        main = QWidget()

        label = IntroLabel1(main)
        label.setText("Pump")
        label.move(425, 30)

        self.data_form_circulationpumps = ["Circulation Pump",
                                      ["Required Power", 'W', "lineedit", '600'],
                                      ["Fluid Velocity", "m/s", 'lineedit', '1.5'],
                                      ['Pump Motor Efficiency', '%', 'lineedit', '85']
                                      ]
        self.form_circulationpumps = InputForm(main, self.data_form_circulationpumps)
        self.form_circulationpumps.move(250, 100)

        timer = QTimer()

        def uimovenext():
            print("Design")
            dict = {}
            if self.form_circulationpumps.getValidation():
                dict = self.form_circulationpumps.getData()
            else:
                return False

            self.dict["Pump"] = dict
            self.btn_5_ticker.show()

            if len(self.dict.keys()) == 5:
                self.result()
            else:
                print("notification")
                return False
            return True

        def uimoveprevious():
            self.moveprevious()

        def end_loading():

            self.left_widget.setEnabled(True)
            loading_label.setVisible(False)
            btn_loading_stop.setVisible(False)
            movie.stop()
            timer.stop()
            uimovenext()

        def start_loading():
            loading_label.setVisible(True)
            self.left_widget.setEnabled(False)
            btn_loading_stop.setVisible(True)
            movie.start()
            timer.timeout.connect(end_loading)
            timer.start(2000)

        def loading_stop():
            self.left_widget.setEnabled(True)
            loading_label.setVisible(False)
            btn_loading_stop.setVisible(False)
            movie.stop()
            timer.stop()

        btn_open = MainButton1(main)
        btn_open.setText(main.tr('Previous Step'))
        btn_open.move(200, 670)
        btn_open.resize(170, 55)
        btn_open.clicked.connect(uimoveprevious)

        btn_next = MainButton1(main)
        btn_next.setText(main.tr('Design'))
        btn_next.move(550, 670)
        btn_next.resize(170, 55)
        btn_next.clicked.connect(start_loading)

        movie = QMovie('./Images/loading.gif')
        loading_label = QLabel(main)
        loading_label.setAlignment(Qt.AlignCenter)
        loading_label.setFixedSize(800, 800)
        loading_label.setVisible(False)
        loading_label.setMovie(movie)
        loading_label.move(100, 0)

        btn_loading_stop = ImageButton1(main, './Images/x02.png')
        btn_loading_stop.setToolTip('Cancel Calculation')
        btn_loading_stop.move(900, 30)
        btn_loading_stop.clicked.connect(loading_stop)
        btn_loading_stop.setVisible(False)

        return main

    def ui7(self):
        # Result
        main = QWidget()

        label = IntroLabel1(main)
        label.setText("Result")
        label.move(425, 30)

        main.setStyleSheet('''
            color: white;
        ''')
        self.data_form_designdimensions = ["Design Dimensions",
                                      ["Pipe Length", 'm', "lineedit", '200'],
                                      ['Inlet Temperature', '⁰F', 'lineedit', '70'],
                                      ["Outlet Temperature", '⁰F', "lineedit", '40'],
                                      ['System Flow Rate', 'gpm', 'lineedit', '10']
                                      ]
        self.form_designdimensions = InputForm(main, self.data_form_designdimensions)
        self.form_designdimensions.move(260, 100)

        label_description = IntroLabel3(main)
        label_description.setText('Description')
        label_description.setAlignment(Qt.AlignCenter)
        label_description.move(420, 420)

        self.textedit_description = CustomQTextEdit(main)
        # textedit_description.place
        self.textedit_description.setPlaceholderText('Design GHE for blockchain mining equipment')
        self.textedit_description.setGeometry(150, 450, 700, 150)



        timer = QTimer()
        def uisavedesign():
            print("uimovenext")
            dict = {}

            if self.form_designdimensions.getValidation():
                dict[self.data_form_designdimensions[0]] = self.form_designdimensions.getData()
            else:
                icon = QIcon('./Images/logo03.png')
                custom_message_box = CustomMessageBox(icon, 'Custom Message', 'You have to input values \n'
                                                                              '    correctly.', self)
                custom_message_box.setGeometry(900, 20, 300, 70)
                custom_message_box.show()
                return False

            if self.textedit_description.toPlainText() == "":
                self.textedit_description.setText('Design GHE for blockchain mining equipment')
            description = self.textedit_description.toPlainText()
            self.dict["Description"] = description
            # self.movenext()
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            file_path, _ = QFileDialog.getSaveFileName(main, "Save File", "", "Text Files *.gld;;",
                                                       options=options)
            print(file_path)
            if file_path:
                temp_file_path = file_path.split('/')[-1].split('.')
                if len(temp_file_path) == 1:
                    file_path = file_path + '.gld'
                with open(file_path, 'w') as file:
                    file.write(json.dumps(self.dict))
                with open(self.designpath, 'r') as tablefile:
                    tablecontent = json.load(tablefile)
                with open(self.designpath, 'w') as savefile:
                    tablecontent[file_path] = description["Description"]
                    savefile.write(json.dumps(tablecontent))
            return True

        def gotoanalysis():
            print("gotoanalysis")
            dict = {}

            if self.form_designdimensions.getValidation():
                dict[self.data_form_designdimensions[0]] = self.form_designdimensions.getData()
            else:
                self.btn_6_ticker.hide()
                icon = QIcon('./Images/logo03.png')
                custom_message_box = CustomMessageBox(icon, 'Custom Message', 'You have to input values \n'
                                                                              '    correctly.', self)
                custom_message_box.setGeometry(900, 20, 300, 70)
                custom_message_box.show()
                return False
            print('1')
            if self.textedit_description.toPlainText() == "":
                self.textedit_description.setText('Design GHE for blockchain mining equipment')
            description = self.textedit_description.toPlainText()
            self.dict["Results"] = dict
            self.dict["Description"] = description
            self.btn_6_ticker.show()
            self.button7()

        def end_loading():

            self.left_widget.setEnabled(True)
            loading_label.setVisible(False)
            btn_loading_stop.setVisible(False)
            movie.stop()
            timer.stop()
            # Validation
            self.analysis()

        def start_loading():
            loading_label.setVisible(True)
            self.left_widget.setEnabled(False)
            btn_loading_stop.setVisible(True)
            movie.start()
            timer.timeout.connect(end_loading)
            timer.start(2000)

        def loading_stop():
            self.left_widget.setEnabled(True)
            loading_label.setVisible(False)
            btn_loading_stop.setVisible(False)
            movie.stop()
            timer.stop()

        btn_save = MainButton1(main)
        btn_save.setText(main.tr('Save design'))
        btn_save.move(150, 670)
        btn_save.resize(170, 55)
        btn_save.clicked.connect(uisavedesign)

        btn_redesign = MainButton1(main)
        btn_redesign.setText(main.tr('Redesign'))
        btn_redesign.move(412, 670)
        btn_redesign.resize(170, 55)
        btn_redesign.clicked.connect(self.button0)

        btn_gotoanalysis = MainButton1(main)
        btn_gotoanalysis.setText(main.tr('Go to Analysis'))
        btn_gotoanalysis.move(675, 670)
        btn_gotoanalysis.resize(170, 55)
        btn_gotoanalysis.clicked.connect(start_loading)

        movie = QMovie('./Images/loading.gif')
        loading_label = QLabel(main)
        loading_label.setAlignment(Qt.AlignCenter)
        loading_label.setFixedSize(800, 800)
        loading_label.setVisible(False)
        loading_label.setMovie(movie)
        loading_label.move(100, 0)

        btn_loading_stop = ImageButton1(main, './Images/x02.png')
        btn_loading_stop.setToolTip('Cancel Calculation')
        btn_loading_stop.move(900, 30)
        btn_loading_stop.clicked.connect(loading_stop)
        btn_loading_stop.setVisible(False)

        return main

    def ui8(self):
        # Analysis
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)


        main = QWidget()

        label = IntroLabel1(main)
        label.setText("Analysis")
        label.move(400, 30)
        
        self.plt_gfunction = pg.PlotWidget(main)
        self.plt_gfunction.setTitle("G-function")
        self.plt_gfunction.setLabel('left', 'g-function')
        self.plt_gfunction.setLabel('bottom', 'Time')
        self.plt_gfunction.setBackground('#2C3751')
        self.plt_gfunction.setGeometry(150, 100, 700, 400)

        self.plt_temperaturepertubation = pg.PlotWidget(main)


        btn_redesign = MainButton1(main)
        btn_redesign.setText(main.tr('Redesign'))
        btn_redesign.move(450, 670)
        btn_redesign.resize(170, 55)
        # btn_redesign.clicked.connect(uiredesign)

        # btn_gotoanalysis = MainButton1(main)
        # btn_gotoanalysis.setText(main.tr('Go to Analysis'))
        # btn_gotoanalysis.move(625, 670)
        # btn_gotoanalysis.resize(170, 55)
        # # btn_gotoanalysis.clicked.connect(uigotoanalysis)

        scroll_area.setWidget(main)
        return scroll_area

    def ui9(self):
        # Settings
        main = QWidget()

        label = IntroLabel1(main)
        label.setText("Settings")
        label.move(425, 30)

        # data_form_designdimensions = ["Design Dimensions",
        #                               ["Pipe Length", 'm', "lineedit", '200'],
        #                               ['Inlet Temperature', '⁰F', 'lineedit', '70'],
        #                               ["Outlet Temperature", '⁰F', "lineedit", '40'],
        #                               ['System Flow Rate', 'gpm', 'lineedit', '10']
        #                               ]
        # self.form_designdimensions = InputForm(main, data_form_designdimensions)
        # self.form_designdimensions.move(260, 100)

        self.data_license_info = ["1010101010101010", '1010101010101010']
        self.license_info = LicenseForm(main)
        self.license_info.resize(600, 200)
        self.license_info.move(200, 100)

        self.data_time_setting = ['Time Setting',
                                  ['Prediction Time', ['1 month', '2 month', '6 month', '1 year'], 'combobox']
                                  ]

        self.time_setting = InputForm(main, self.data_time_setting)
        self.time_setting.resize(300, 100)
        self.time_setting.move(160, 350)

        self.personal_setting = PersonalForm(main)
        self.personal_setting.resize(300, 137)
        self.personal_setting.move(160, 470)

        self.data_userinfo = ['User Info',
                              ['Username', '', 'lineedit', '**** ****'],
                              ['Gmail','', 'lineedit', 'default@gmail.com'],
                              ['Purpose', '', 'lineedit', 'Residental Building'],
                              ['Country', '', 'lineedit', 'Canada'],
            ['Phone', '', 'lineedit', '1010101010']
            ]
        self.userinfo = InputForm(main, self.data_userinfo)
        self.userinfo.move(500, 350)

        return main

    def movenext(self):
        self.right_widget.setCurrentIndex(self.right_widget.currentIndex() + 1)
        self.tickerbutton()

    def moveprevious(self):
        self.right_widget.setCurrentIndex(self.right_widget.currentIndex() - 1)
        self.tickerbutton()

    def loaddata(self):
        with open(self.currentgldpath, 'r') as f:
            context = json.load(f)
        self.form_systemdesign.setData(context['System'].values())
        self.form_fluidproperties.setData(context['Fluid'].values())
        self.form_soilthermalproperties.setData(context['Soil'].values())
        self
        print(context)

    def redirect_to_feedback(self):
        webbrowser.open('https://stackoverflow.com/')

    def redirect_to_help(self):
        webbrowser.open('https://stackoverflow.com/')

    def exitbutton(self):
        self.parent.exit()

    def sizing(self):
        # System
        try:
            E_heat = float(self.dict['System']['Heat Load'])  # heat load [W*h]
            T_in = float(self.dict['System']['Input Fluid Temperature'])  # Hot Fluid Temperature 60~65dC, 140~150dF

            # Fluid
            mu = float(self.dict["Fluid"]["Viscosity"])
            c_p = float(self.dict["Fluid"]["Specific Heat"])
            rho = float(self.dict["Fluid"]["Density"])

            # Soil
            k_soil = float(self.dict["Soil"]["Thermal Conductivity"])
            T_g = float(self.dict["Soil"]["Ground Temperature"])

            print(E_heat, T_in, mu, c_p, rho, k_soil, T_g)

            # Pipe
            D_i = float(self.dict['Pipe']['Inner Diameter'])
            D_o = float(self.dict['Pipe']['Outer Diameter'])
            f_type = self.dict['Pipe']['Flow Type']
            k_pipe = float(self.dict['Pipe']['Pipe Conductivity'])
            d = float(self.dict['Pipe']['Buried Depth'])

            # Pump
            V = float(self.dict["Pump"]["Fluid Velocity"])  # modify
            p = float(self.dict['Pump']['Required Power'])

        except Exception as e:
            print('Exception: ', traceback.format_exc())
            return False
        print('after input variable')
        try:
        # Resistance
            R_e = rho * V * D_i / mu  # Reynolds number    Re<2100 laminar regime; 2100<Re<10000: transitional regime;
            # Re>10000 turbulent regime
            P_r = mu * c_p / k_pipe  # Prandtl number
            h_w = 0.023 * R_e ** 0.8 * P_r ** 0.3 * k_pipe / D_i  # heat transfer coefficient [W/(m^2*k)]

            R_conv = 1 / (3.14159 * D_i * h_w)
            R_pipe = math.log(D_o / D_i) / (2 * 3.14159 * k_pipe)
            S = 2 * 3.14159 / math.log((2 * d / D_o) + math.sqrt((2 * d / D_o) ** 2 - 1))  # conduction shape factor of
            # the pipe
            R_soil = 1 / (S * k_soil)

            R_total = R_conv + R_pipe + R_soil

            # Length calculation
            m_w = rho * V * 3.14159 * (D_i / 2) ** 2
            T_out = T_in - E_heat / (m_w * c_p)
            theta_w_in = T_in - T_g
            theta_w_out = T_out - T_g

            L = (m_w * c_p * R_total) * math.log(theta_w_in / theta_w_out)

            print("length of pipe:", L)
            self.dict['Result'] = {'Pipe Length': str(L)}
            loop_diameter = 0.75
            pitch = 0.4
            return True
        except Exception as e:
            print('Size Calculation Error:', traceback.format_exc())
            return False

    def result(self):
        if self.sizing():
            data_form_designdimensions = ["Design Dimensions",
                                          ["Pipe Length", 'm', "lineedit", self.dict['Result']['Pipe Length']],
                                          ['Inlet Temperature', '⁰F', 'lineedit', '70'],
                                          ["Outlet Temperature", '⁰F', "lineedit", '40'],
                                          ['System Flow Rate', 'gpm', 'lineedit', '10']
                                          ]
            self.form_designdimensions.setData(data_form_designdimensions)
            self.form_designdimensions.setReadOnly(True)
            self.movenext()
        else:
            print('Show Notification')
    def analysis(self):
        print('Analysis')
        # N_ring = 5
        # R = 1  # m
        # pitch = 0.2  # m
        # alpha = 1e-6  # m2/s
        # t_series = np.arange(10000, 3e7 + 1, 1e6)
        # t_1 = int(1e6)
        # h = 2  # m
        #
        # # gs_series = []
        # # for N_ring in N_ring_series:
        # gs_series = []
        # for t in t_series:
        #     gs = Decimal(0)
        #     for i in range(1, N_ring + 1):
        #         for j in range(1, N_ring + 1):
        #             if i != j:
        #                 def d(w, phi):
        #                     return np.sqrt((pitch * (i - j) + R * (np.cos(phi) - np.cos(w))) ** 2 +
        #                                    (R * (np.sin(phi) - np.sin(w))) ** 2)
        #
        #                 def fun(w, phi):
        #                     return erfc(d(w, phi) / (2 * np.sqrt(alpha * t))) / d(w, phi) - erfc(
        #                         np.sqrt(d(w, phi) ** 2 + 4 * h ** 2) / (2 * np.sqrt(alpha * t))) / np.sqrt(
        #                         d(w, phi) ** 2 + 4 * h ** 2)
        #
        #                 b, _ = dblquad(fun, 0, 2 * np.pi, lambda phi: 0, lambda phi: 2 * np.pi, epsabs=1e-2,
        #                                epsrel=1e-2)
        #                 print(b)
        #                 gs += Decimal(b)
        #
        #     print(f"gs: {gs}")
        #     gs_series.append(gs)
        x = np.linspace(0, 2*np.pi, 1000)
        y = np.sin(x)
        self.plt_gfunction.clear()
        self.plt_gfunction.plot(x, y, pen='b')

        self.movenext()

    def btnexit(self):
        self.setEnabled(False)
        notification = ExitNotification(self)
        result = notification.exec_()

        if result == QMessageBox.No:
            self.setEnabled(True)
        
        elif result == QMessageBox.Yes:
            sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DesignClass()
    ex.show()
    sys.exit(app.exec_())
