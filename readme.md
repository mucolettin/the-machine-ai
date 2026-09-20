THE MACHINE AI
Yapay zekâ donanımları, yüksek performanslı GPU sistemleri,
AI iş istasyonları, AI sunucuları ve Edge Computing çözümleri sunan
teknoloji odaklı bir proje markasıdır.

Bu proje, ziyaretçilerin yapay zekâ destekli bir asistan ile sohbet
edebilmesini, ihtiyaçlarını belirtmesini ve iletişim bilgilerini
bırakabilmesini sağlayan bir SmartLead AI uygulamasıdır.

ÖZELLİKLER

- Yapay zekâ destekli müşteri sohbeti
- Kullanıcı mesajlarına işletme bağlamına uygun cevaplar
- İsim, telefon ve mesaj bilgilerinin lead olarak kaydedilmesi
- SQLite veritabanı kullanımı
- Yönetim panelinde lead kayıtlarının listelenmesi
- Wix Velo ile REST API bağlantısı
- Render üzerinde canlı Flask backend
- '/health' ile sunucu durum kontrolü
- CORS desteği
- Hata yönetimi ve güvenli API kullanımı

NE KULLANDIDM

- Python
- Flask
- SQLite
- Groq API
- Wix Velo
- Render
- GitHub
- HTML / CSS / JavaScript

PROJE YAPISI

```text
the_machine_ai/
│
├── run.py
├── config.py
├── requirements.txt
├── .env
├── .gitignore
│
└── app/
    ├── __init__.py
    ├── database.py
    ├── routes.py
    │
    ├── templates/
    │   ├── index.html
    │   └── dashboard.html
    │
    └── services/
        ├── __init__.py
        └── ai_service.py