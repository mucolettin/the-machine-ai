import sqlite3
from datetime import datetime
from pathlib import Path

from flask import current_app, has_app_context


PROJE_KLASORU = Path(__file__).resolve().parent.parent
VARSAYILAN_VERITABANI = PROJE_KLASORU / "the_machine.db"


def veritabani_yolu():
    if has_app_context():
        ayardaki_yol = current_app.config.get("DATABASE_URL")

        if ayardaki_yol:
            ayardaki_yol = str(ayardaki_yol)

            if ayardaki_yol.startswith("sqlite:///"):
                ayardaki_yol = ayardaki_yol.replace(
                    "sqlite:///",
                    "",
                    1
                )

            yol = Path(ayardaki_yol)

            if not yol.is_absolute():
                yol = PROJE_KLASORU / yol

            return str(yol)

    return str(VARSAYILAN_VERITABANI)


def veritabani_baglantisi():
    baglanti = sqlite3.connect(
        veritabani_yolu()
    )

    baglanti.row_factory = sqlite3.Row

    return baglanti


def veritabani_olustur():
    baglanti = veritabani_baglantisi()
    cursor = baglanti.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS musteri_adaylari (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            isim TEXT NOT NULL,
            soyisim TEXT,
            telefon TEXT NOT NULL,
            mesaj TEXT,
            kvkk INTEGER DEFAULT 0,
            kvkk_onay_tarihi TEXT,
            olusturulma_tarihi TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        PRAGMA table_info(musteri_adaylari)
    """)

    mevcut_sutunlar = {
        satir["name"]
        for satir in cursor.fetchall()
    }

    eklenecek_sutunlar = {
        "email": "TEXT",
        "soyisim": "TEXT",
        "kvkk": "INTEGER DEFAULT 0",
        "kvkk_onay_tarihi": "TEXT",
    }

    for sutun, tip in eklenecek_sutunlar.items():
        if sutun not in mevcut_sutunlar:
            cursor.execute(
                f"""
                ALTER TABLE musteri_adaylari
                ADD COLUMN {sutun} {tip}
                """
            )

    if "olusturulma_tarihi" not in mevcut_sutunlar:
        cursor.execute("""
            ALTER TABLE musteri_adaylari
            ADD COLUMN olusturulma_tarihi TEXT
        """)

        cursor.execute("""
            UPDATE musteri_adaylari
            SET olusturulma_tarihi = CURRENT_TIMESTAMP
            WHERE olusturulma_tarihi IS NULL
        """)

    baglanti.commit()
    baglanti.close()


def veritabani_baslat(uygulama=None):
    if has_app_context():
        veritabani_olustur()
        return

    if uygulama is not None:
        with uygulama.app_context():
            veritabani_olustur()


def aday_kaydet(*args, **kwargs):
    """
    Hem eski kodlarla hem yeni Wix formuyla çalışır.
    """

    email = ""
    isim = ""
    soyisim = ""
    telefon = ""
    mesaj = ""
    kvkk = False

    if kwargs:
        email = kwargs.get("email", "")
        isim = kwargs.get("isim", "")
        soyisim = kwargs.get("soyisim", "")
        telefon = kwargs.get("telefon", "")
        mesaj = kwargs.get("mesaj", "")
        kvkk = kwargs.get("kvkk", False)

    elif len(args) == 3:
        # Eski kullanım:
        # aday_kaydet(isim, telefon, mesaj)

        isim = args[0]
        telefon = args[1]
        mesaj = args[2]

    elif len(args) >= 4:
        # Yeni kullanım:
        # aday_kaydet(email, isim, soyisim, telefon, mesaj, kvkk)

        email = args[0]
        isim = args[1]
        soyisim = args[2]
        telefon = args[3]

        if len(args) >= 5:
            mesaj = args[4]

        if len(args) >= 6:
            kvkk = args[5]

    else:
        raise ValueError(
            "Müşteri adayı bilgileri eksik."
        )

    email = str(email or "").strip()
    isim = str(isim or "").strip()
    soyisim = str(soyisim or "").strip()
    telefon = str(telefon or "").strip()
    mesaj = str(mesaj or "").strip()

    if not isim:
        raise ValueError(
            "İsim boş bırakılamaz."
        )

    if not telefon:
        raise ValueError(
            "Telefon boş bırakılamaz."
        )

    kvkk_degeri = 1 if kvkk else 0

    kvkk_onay_tarihi = None

    if kvkk_degeri == 1:
        kvkk_onay_tarihi = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    baglanti = veritabani_baglantisi()
    cursor = baglanti.cursor()

    cursor.execute("""
        INSERT INTO musteri_adaylari (
            email,
            isim,
            soyisim,
            telefon,
            mesaj,
            kvkk,
            kvkk_onay_tarihi,
            olusturulma_tarihi
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        email,
        isim,
        soyisim,
        telefon,
        mesaj,
        kvkk_degeri,
        kvkk_onay_tarihi,
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    ))

    baglanti.commit()

    yeni_id = cursor.lastrowid

    baglanti.close()

    return yeni_id


def adaylari_getir():
    baglanti = veritabani_baglantisi()
    cursor = baglanti.cursor()

    cursor.execute("""
        SELECT *
        FROM musteri_adaylari
        ORDER BY id DESC
    """)

    sonuc = cursor.fetchall()

    baglanti.close()

    return sonuc


def aday_sayisi():
    baglanti = veritabani_baglantisi()
    cursor = baglanti.cursor()

    cursor.execute("""
        SELECT COUNT(*) AS toplam
        FROM musteri_adaylari
    """)

    sonuc = cursor.fetchone()

    baglanti.close()

    return sonuc["toplam"]