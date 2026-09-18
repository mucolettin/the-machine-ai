import sqlite3
from flask import current_app


def get_db():
    """SQLite veritabanına bağlanır."""
    db = sqlite3.connect(current_app.config["DATABASE_URL"])
    db.row_factory = sqlite3.Row
    return db


def init_db(app):
    """Veritabanını ve leads tablosunu oluşturur."""
    with app.app_context():
        db = get_db()

        db.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                telefon TEXT NOT NULL,
                mesaj TEXT,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        db.commit()
        db.close()


def lead_ekle(isim, telefon, mesaj=""):
    """Yeni bir müşteri adayı kaydeder."""
    db = get_db()

    db.execute(
        """
        INSERT INTO leads (isim, telefon, mesaj)
        VALUES (?, ?, ?)
        """,
        (isim, telefon, mesaj)
    )

    db.commit()
    db.close()


def tum_leadler():
    """Tüm müşteri adaylarını yeniden eskiye getirir."""
    db = get_db()

    leads = db.execute(
        """
        SELECT id, isim, telefon, mesaj, tarih
        FROM leads
        ORDER BY tarih DESC
        """
    ).fetchall()

    db.close()

    return [dict(lead) for lead in leads]