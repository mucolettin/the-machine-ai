from flask import Flask, jsonify
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

    # Wix'in Render API'ye bağlanabilmesi için CORS
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

    # Veritabanını hazırla
    with uygulama.app_context():
        veritabani_olustur()

    # API rotalarını yükle
    from uygulama.rotalar import api_arayuzu

    uygulama.register_blueprint(
        api_arayuzu,
        url_prefix="/api"
    )

    # Render ana adresi 404 vermesin
    @uygulama.route("/")
    def ana_sayfa():
        return jsonify({
            "basari": True,
            "mesaj": "THE MACHINE AI backend çalışıyor."
        })

    # Sağlık kontrolü
    @uygulama.route("/health")
    def health():
        return jsonify({
            "durum": "ok"
        })

    return uygulama