from flask import Flask
from flask_cors import CORS

from config import Config
from app.database import init_db
from app.routes import page_bp, api_bp


def create_app():
    app = Flask(__name__)

    # Ayarları yükle
    app.config.from_object(Config)

    # CORS'u etkinleştir
    CORS(app)

    # Veritabanını oluştur
    init_db(app)

    # Blueprint'leri kaydet
    app.register_blueprint(page_bp)
    app.register_blueprint(api_bp)

    @app.route("/health")
    def health():
        return {
            "status": "ok",
            "service": "THE MACHINE AI"
        }

    return app