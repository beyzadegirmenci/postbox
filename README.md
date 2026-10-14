# Dilek, Şikayet ve Geri Bildirim Kutusu

Flask tabanlı web uygulaması. Kullanıcılar sol alttaki `?` düğmesinden mesaj türünü seçip geri bildirim bırakabilir; gelen kutusunda kategoriler zarf görünümünde listelenir.

## Kurulum ve çalıştırma

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

Uygulama `http://127.0.0.1:5000` adresinde açılır. Mesajlar `instance/feedback.sqlite3` dosyasında saklanır.
