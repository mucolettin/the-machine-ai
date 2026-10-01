import os

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv


def uygulama_olustur():

    # .env dosyasını yükle
    load_dotenv()


    # Flask uygulamasını oluştur
    uygulama = Flask(__name__)


    # Türkçe karakter desteği
    uygulama.json.ensure_ascii = False


    # Temel ayarlar
    uygulama.config["SECRET_KEY"] = os.getenv(
        "SECRET_KEY",
        "the-machine-secret"
    )


    uygulama.config["DATABASE_URL"] = os.getenv(
        "DATABASE_URL",
        "the_machine.db"
    )


    # Wix'in API'ye erişebilmesi için CORS
    CORS(
        uygulama,
        resources={
            r"/api/*": {
                "origins": "*"
            }
        }
    )


    # Veritabanını hazırla
    from uygulama.veritabani import (
        veritabani_baslat
    )

    veritabani_baslat(
        uygulama
    )


    # Sadece API route'larını yükle
    from uygulama.rotalar import (
        api_arayuzu
    )


    # /api ile başlayan adresler
    uygulama.register_blueprint(
        api_arayuzu,
        url_prefix="/api"
    )


    return uygulama