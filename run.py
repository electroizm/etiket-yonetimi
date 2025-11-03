"""
Etiket Programı - Ana Kontrol Paneli
PRG tarzı tek pencere, üstte butonlar
"""

import sys
import os
import subprocess
import multiprocessing
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QApplication, QMainWindow, QStackedWidget,
                             QFrame, QTextEdit, QMessageBox)
from PyQt5.QtGui import QFont, QIcon

# Modülleri import et
from jsonGoster import JsonGosterWidget
from etiketYazdir import EtiketYazdirWidget


def get_resource_path(filename):
    """PyInstaller ile paketlenmiş resource dosyalarının yolunu döndür"""
    if getattr(sys, 'frozen', False):
        # PyInstaller _MEIPASS: geçici klasörde dosyalar
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)


def setup_script_file(filename):
    """
    Script dosyasını exe'nin yanına kopyala (ilk çalışmada)
    dogtasCom.py gibi subprocess ile çalıştırılan scriptler için
    """
    if not getattr(sys, 'frozen', False):
        # Script olarak çalışıyorsa kopyalamaya gerek yok
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

    # Exe olarak çalışıyorsa
    exe_dir = os.path.dirname(sys.executable)
    target_file = os.path.join(exe_dir, filename)

    # Dosya zaten exe'nin yanındaysa, onu kullan
    if os.path.exists(target_file):
        return target_file

    # Dosya yoksa, _internal'dan kopyala
    source_file = get_resource_path(filename)
    if os.path.exists(source_file):
        import shutil
        try:
            shutil.copy2(source_file, target_file)
            print(f"[SETUP] {filename} dosyası kopyalandı: {target_file}")
        except Exception as e:
            print(f"[HATA] {filename} kopyalanamadı: {e}")
    else:
        print(f"[UYARI] Kaynak dosya bulunamadı: {source_file}")

    return target_file


class OutputReaderThread(QThread):
    """Subprocess çıktısını okuyan thread"""
    output_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(int)

    def __init__(self, process):
        super().__init__()
        self.process = process
        self.running = True

    def run(self):
        """Çıktıları satır satır oku"""
        try:
            for line in iter(self.process.stdout.readline, ''):
                if not self.running:
                    break
                if line:
                    self.output_signal.emit(line.rstrip())

            self.process.wait()
            self.finished_signal.emit(self.process.returncode)
        except Exception as e:
            self.output_signal.emit(f"[THREAD ERROR] {str(e)}")

    def stop(self):
        """Thread'i durdur"""
        self.running = False


class DogtasComWidget(QWidget):
    """dogtas.Com modülü için widget - subprocess ile çalıştırır"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.process = None
        self.reader_thread = None
        # dogtasCom.py script yolunu bul (PyInstaller uyumlu)
        self.script_path = setup_script_file("dogtasCom.py")
        self.setup_ui()

    def setup_ui(self):
        """UI bileşenlerini oluştur"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(10)

        # Başlık
        title_label = QLabel("🌐 Dogtas.Com Web Taraması")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50; padding: 5px;")
        main_layout.addWidget(title_label)

        # Açıklama
        desc_label = QLabel(
            "Dogtas.com sitesinden ürün verilerini çeker ve Etiket.gsheet dosyasına Google Sheets API yardımıyla kaydeder.\n"
            "⚠ İşlem uzun sürebilir."
        )
        desc_label.setStyleSheet("""
            QLabel {
                color: #34495e;
                font-size: 11px;
                padding: 8px;
                background-color: #ecf0f1;
                border-radius: 4px;
                border: 1px solid #bdc3c7;
            }
        """)
        desc_label.setWordWrap(True)
        main_layout.addWidget(desc_label)

        # Butonlar
        button_layout = QHBoxLayout()

        self.start_btn = QPushButton("▶ Web Taraması Başlat")
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        self.start_btn.clicked.connect(self.start_scraping)
        button_layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton("⏹ İptal Et")
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        self.stop_btn.clicked.connect(self.stop_scraping)
        self.stop_btn.setEnabled(False)
        button_layout.addWidget(self.stop_btn)

        clear_btn = QPushButton("🗑 Temizle")
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        clear_btn.clicked.connect(self.clear_log)
        button_layout.addWidget(clear_btn)

        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        # Log alanı
        log_label = QLabel("📋 İşlem Günlüğü")
        log_label.setStyleSheet("font-weight: bold; font-size: 11px; padding: 3px;")
        main_layout.addWidget(log_label)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                font-family: 'Courier New', monospace;
                font-size: 20px;
                border: 2px solid #bdc3c7;
                border-radius: 4px;
                padding: 8px;
                background-color: #1e1e1e;
                color: #d4d4d4;
            }
        """)
        main_layout.addWidget(self.log_text)

        # Status
        self.status_label = QLabel("Hazır - Web taraması başlatmayı bekliyor...")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                padding: 6px;
                background-color: #ecf0f1;
                border-top: 1px solid #bdc3c7;
                font-size: 10px;
                font-weight: bold;
            }
        """)
        main_layout.addWidget(self.status_label)

    def start_scraping(self):
        """Scraping başlat"""
        if not os.path.exists(self.script_path):
            QMessageBox.warning(self, "Uyarı", f"Script bulunamadı:\n{self.script_path}")
            return

        reply = QMessageBox.question(
            self,
            "Web Taraması Başlat",
            "Doğtaş web sitesinden tüm ürünleri çekmeye başlayacak.\n\n"
            "Bu işlem UZUN sürebilir (1-3 saat).\n\n"
            "Devam etmek istiyor musunuz?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.log_text.clear()
        self.status_label.setText("⏳ Web taraması başlatılıyor...")

        self.append_log("="*60)
        self.append_log("WEB TARAMASI BAŞLATILDI")
        self.append_log("="*60)

        try:
            # Python interpreter'ı bul
            if getattr(sys, 'frozen', False):
                # Exe olarak çalışıyorsa, sistem Python'unu kullan
                python_exe = self.find_system_python()
                if not python_exe:
                    raise FileNotFoundError("Python interpreter bulunamadı! Lütfen Python'u sisteme yükleyin.")
            else:
                # Script olarak çalışıyorsa, mevcut Python'u kullan
                python_exe = sys.executable

            self.append_log(f"[INFO] Python: {python_exe}")
            self.append_log(f"[INFO] Script: {self.script_path}")
            self.append_log("")

            # Windows'ta konsol penceresi açılmasını engelle
            startupinfo = None
            if sys.platform == 'win32':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE

            # Subprocess'i başlat (konsol penceresi olmadan)
            self.process = subprocess.Popen(
                [python_exe, self.script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
                cwd=os.path.dirname(self.script_path),
                startupinfo=startupinfo
            )

            # Reader thread'i başlat
            self.reader_thread = OutputReaderThread(self.process)
            self.reader_thread.output_signal.connect(self.append_log)
            self.reader_thread.finished_signal.connect(self.on_process_finished)
            self.reader_thread.start()

            self.status_label.setText("⏳ Web taraması devam ediyor...")

        except Exception as e:
            self.append_log(f"[HATA] {str(e)}")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)

    def find_system_python(self):
        """Sistem Python'unu bul"""
        # Olası Python konumları
        possible_paths = [
            r"C:\Python\python.exe",
            r"C:\Python312\python.exe",
            r"C:\Python311\python.exe",
            r"C:\Python310\python.exe",
            r"C:\Python39\python.exe",
            r"C:\Program Files\Python312\python.exe",
            r"C:\Program Files\Python311\python.exe",
            r"C:\Program Files\Python310\python.exe",
        ]

        # Önce olası konumlarda ara
        for path in possible_paths:
            if os.path.exists(path):
                return path

        # PATH'te ara
        try:
            result = subprocess.run(
                ["where", "python"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                # İlk bulunan Python'u kullan
                python_path = result.stdout.strip().split('\n')[0]
                if os.path.exists(python_path):
                    return python_path
        except:
            pass

        return None

    def stop_scraping(self):
        """Scraping durdur"""
        if self.process:
            reply = QMessageBox.question(
                self,
                "İptal Et",
                "Web taraması işlemini iptal etmek istiyor musunuz?",
                QMessageBox.Yes | QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                # Reader thread'i durdur
                if self.reader_thread:
                    self.reader_thread.stop()

                # Process'i terminate et
                self.process.terminate()

                self.append_log("\n[İPTAL EDİLDİ] Kullanıcı tarafından iptal edildi.")
                self.status_label.setText("⏹ Web taraması iptal edildi")
                self.start_btn.setEnabled(True)
                self.stop_btn.setEnabled(False)

    def on_process_finished(self, return_code):
        """Process bittiğinde çağrılır"""
        self.append_log("\n" + "="*60)

        if return_code == 0:
            self.append_log("[TAMAMLANDI] Web taraması başarıyla tamamlandı!")
            self.status_label.setText("✅ Web taraması tamamlandı")
        else:
            self.append_log(f"[HATA] Web taraması hata ile sonlandı (kod: {return_code})")
            self.status_label.setText("❌ Web taraması hatası")

        self.append_log("="*60)
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

    def append_log(self, text):
        """Log'a metin ekle"""
        self.log_text.append(text)
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def clear_log(self):
        """Log'u temizle"""
        self.log_text.clear()
        self.status_label.setText("Hazır - Web taraması başlatmayı bekliyor...")


class EtiketEkleWidget(QWidget):
    """Etiket Ekle modülü için widget wrapper"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.window = None  # Window referansını sakla
        self.setup_ui()

    def setup_ui(self):
        """UI bileşenlerini oluştur"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        try:
            # etiketEkle.py'den EtiketListesiWindow'u import et
            from etiketEkle import EtiketListesiWindow

            # Window'u oluştur ve REFERANSTA TUT (garbage collection engellemek için)
            self.window = EtiketListesiWindow()

            # Ayrı pencereyi gizle (sadece central widget'ı embed edeceğiz)
            self.window.hide()

            # Window'un central widget'ını al
            widget = self.window.centralWidget()

            # Widget'ı layout'a ekle
            widget.setParent(self)
            main_layout.addWidget(widget)

        except Exception as e:
            error_label = QLabel(f"❌ Etiket Ekle modülü yüklenemedi:\n{str(e)}")
            error_label.setStyleSheet("""
                QLabel {
                    color: #e74c3c;
                    font-size: 12px;
                    font-weight: bold;
                    padding: 20px;
                    background-color: #fadbd8;
                    border: 2px solid #e74c3c;
                    border-radius: 8px;
                }
            """)
            error_label.setAlignment(Qt.AlignCenter)
            error_label.setWordWrap(True)
            main_layout.addWidget(error_label)


class MainWindow(QMainWindow):
    """Ana kontrol paneli penceresi - PRG tarzı"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Etiket Programı")
        self.setGeometry(50, 50, 1400, 900)

        # UI setup
        self.setup_ui()

        # İlk modülü göster
        self.show_module(0)

    def setup_ui(self):
        """UI bileşenlerini oluştur"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Ana layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Üst panel - Butonlar
        top_panel = QFrame()
        top_panel.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border-bottom: 3px solid #3498db;
            }
        """)
        top_panel.setFixedHeight(60)

        top_layout = QHBoxLayout(top_panel)
        top_layout.setContentsMargins(10, 5, 10, 5)
        top_layout.setSpacing(5)

        # Logo/Başlık - Kaldırıldı (PRG yazısı istenmedi)

        # Modül butonları
        self.module_buttons = []

        modules = [
            ("Dogtas.Com", "🌐"),
            ("Etiket Ekle", "📝"),
            ("Json Göster", "📋"),
            ("Yazdır", "🖨️")
        ]

        for idx, (name, icon) in enumerate(modules):
            btn = QPushButton(f"{icon} {name}")
            btn.setCheckable(True)
            btn.setStyleSheet(self.get_button_style(False))
            btn.clicked.connect(lambda checked, i=idx: self.on_module_button_clicked(i))
            btn.setMinimumWidth(150)
            btn.setMinimumHeight(45)
            top_layout.addWidget(btn)
            self.module_buttons.append(btn)

        top_layout.addStretch()

        # Çıkış butonu
        exit_btn = QPushButton("❌ Çıkış")
        exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        exit_btn.clicked.connect(self.close_application)
        top_layout.addWidget(exit_btn)

        main_layout.addWidget(top_panel)

        # İçerik alanı - Stacked Widget
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: white;")

        # Modül widget'larını ekle
        # 1. dogtas.Com
        self.stacked_widget.addWidget(DogtasComWidget())

        # 2. Etiket Ekle
        self.stacked_widget.addWidget(EtiketEkleWidget())

        # 3. Json Göster
        self.stacked_widget.addWidget(JsonGosterWidget())

        # 4. Yazdır
        self.stacked_widget.addWidget(EtiketYazdirWidget())

        main_layout.addWidget(self.stacked_widget)

        # Alt durum çubuğu
        self.status_bar = self.statusBar()
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #ecf0f1;
                color: #2c3e50;
                font-weight: bold;
                font-size: 11px;
                border-top: 1px solid #bdc3c7;
            }
        """)

        # Sağ alt köşeye copyright etiketi ekle
        copyright_label = QLabel("©   by İsmail Güneş")
        copyright_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-weight: bold;
                font-size: 11px;
                padding: 0px 5px;
            }
        """)
        self.status_bar.addPermanentWidget(copyright_label)

    def get_button_style(self, is_active):
        """Buton stilini döndür"""
        if is_active:
            return """
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-bottom: 3px solid #2980b9;
                    border-radius: 0px;
                    padding: 8px 16px;
                    font-size: 13px;
                    font-weight: bold;
                }
            """
        else:
            return """
                QPushButton {
                    background-color: transparent;
                    color: #ecf0f1;
                    border: none;
                    border-bottom: 3px solid transparent;
                    border-radius: 0px;
                    padding: 8px 16px;
                    font-size: 13px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #34495e;
                    border-bottom: 3px solid #3498db;
                }
                QPushButton:checked {
                    background-color: #3498db;
                    border-bottom: 3px solid #2980b9;
                }
            """

    def on_module_button_clicked(self, index):
        """Modül butonu tıklandığında"""
        self.show_module(index)

    def show_module(self, index):
        """Belirtilen modülü göster"""
        # Tüm butonların checked durumunu güncelle
        for i, btn in enumerate(self.module_buttons):
            btn.setChecked(i == index)
            btn.setStyleSheet(self.get_button_style(i == index))

        # İlgili widget'i göster
        self.stacked_widget.setCurrentIndex(index)

    def close_application(self):
        """Uygulamayı kapat"""
        reply = QMessageBox.question(
            self,
            "Çıkış",
            "Uygulamadan çıkmak istiyor musunuz?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            QApplication.quit()

    def closeEvent(self, event):
        """Pencere kapatılırken"""
        reply = QMessageBox.question(
            self,
            "Çıkış",
            "Uygulamayı kapatmak istiyor musunuz?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def main():
    """Ana program"""
    # PyInstaller ile exe olarak çalışırken subprocess sorunlarını önle
    multiprocessing.freeze_support()

    app = QApplication(sys.argv)

    # Uygulama bilgileri
    app.setApplicationName("Etiket Programı")
    app.setApplicationVersion("2.1.0")
    app.setOrganizationName("Doğtaş")

    # Icon'u yükle ve ayarla (Görev çubuğu için)
    # Önce exe'nin yanında ara, yoksa _internal/ klasöründe ara
    if getattr(sys, 'frozen', False):
        # Exe olarak çalışıyorsa
        exe_dir = os.path.dirname(sys.executable)
        icon_path = os.path.join(exe_dir, "icon.ico")

        # Exe'nin yanında yoksa _internal'da ara
        if not os.path.exists(icon_path):
            icon_path = get_resource_path("icon.ico")
    else:
        # Script olarak çalışıyorsa
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")

    if os.path.exists(icon_path):
        app_icon = QIcon(icon_path)
        app.setWindowIcon(app_icon)
        print(f"[INFO] Icon yuklendi: {icon_path}")
    else:
        print(f"[UYARI] Icon bulunamadi: {icon_path}")

    # Ana pencereyi oluştur
    window = MainWindow()

    # Pencereye de icon'u set et
    if os.path.exists(icon_path):
        window.setWindowIcon(QIcon(icon_path))

    window.showMaximized()  # Tam ekran (maximize) olarak aç

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
