from flask import Flask
from flask_cors import CORS

from ayarlar import Ayarlar
from uygulama.veritabani import veritabani_olustur


def uygulama_olustur():

    uygulama = Flask(
        __name__,
        template_folder="sablonlar"
    )

    # Ayarları yükle
    uygulama.config.from_object(Ayarlar)

    # Türkçe karakterler düzgün görünsün
    uygulama.json.ensure_ascii = False

    # Wix'in Render API'ye erişebilmesi için CORS
    CORS(
        uygulama,
        resources={
            r"/api/*": {
                "origins": "*"
            }
        },
        methods=[
            "GET",
            "POST",
            "OPTIONS"
        ],
        allow_headers=[
            "Content-Type",
            "Authorization"
        ]
    )

    # Veritabanını oluştur / hazırla
    with uygulama.app_context():
        veritabani_olustur()

    # Route'ları yükle
    from uygulama.rotalar import (
        api_arayuzu,
        sayfa_arayuzu
    )

    # Normal sayfalar
    uygulama.register_blueprint(
        sayfa_arayuzu
    )

    # API adresleri
    uygulama.register_blueprint(
        api_arayuzu,
        url_prefix="/api"
    )

    return uygulama