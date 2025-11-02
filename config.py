"""
Google Sheets API Yapılandırması
"""
import os
from pathlib import Path

def get_base_dir():
    """Çalışma dizinini döndür"""
    import sys
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

# Google Sheets yapılandırması
SPREADSHEET_ID = "1-H9fA5dD9rxqcPd0VymKjMgggxUl7hAZBK0csysN-3k"

# Credentials dosya yolu
CREDENTIALS_FILE = os.path.join(get_base_dir(), "credentials.json")

# Google Sheets API scope
SCOPES = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

# Etiket Resimleri (Google Drive Links)
# NOT: Google Drive'da dosyaları public paylaşıma açın ve FILE_ID'yi aşağıya yapıştırın
# Link formatı: https://drive.google.com/uc?export=download&id=FILE_ID

# Etiket başlık resmi (etiket_baslik.png)
ETIKET_BASLIK_URL = "https://drive.google.com/file/d/1RSP3YaCUNqy9Nedaaz5OUlKq9855Glh9/view?usp=drive_link" 
# Google Drive FILE_ID'yi buraya ekleyin
# Örnek: "https://drive.google.com/uc?export=download&id=1ABC123DEF456"

# Yerli üretim logosu (yerli_uretim.jpg)
YERLI_URETIM_URL = "https://drive.google.com/file/d/1pYA85nxhmU6yhWJ3n0jIz1zAkTUeY--8/view?usp=drive_link"  
# Google Drive FILE_ID'yi buraya ekleyin
# Örnek: "https://drive.google.com/uc?export=download&id=1XYZ789GHI012"

