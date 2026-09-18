from flask import Blueprint, jsonify, render_template, request

from app.database import lead_ekle, tum_leadler
from app.services.ai_service import AIServiceError, ai_service


# Web sayfaları için Blueprint
page_bp = Blueprint("pages", __name__)


# API işlemleri için Blueprint
api_bp = Blueprint("api", __name__, url_prefix="/api")


@page_bp.route("/")
def ana_sayfa():
    """Ana sayfayı gösterir."""
    return render_template("index.html")


@page_bp.route("/dashboard")
def dashboard():
    """Yönetici panelini gösterir."""
    return render_template("dashboard.html")


@api_bp.route("/sohbet", methods=["POST"])
def sohbet():
    """Kullanıcı mesajını AI servisine gönderir."""
    try:
        data = request.get_json()

        if not data or not data.get("mesaj"):
            return jsonify({
                "basarili": False,
                "hata": "Mesaj alanı zorunludur."
            }), 400

        mesaj = data["mesaj"]
        gecmis = data.get("gecmis", [])

        cevap = ai_service.yanit_uret(
            mesaj,
            gecmis
        )

        return jsonify({
            "basarili": True,
            "cevap": cevap
        }), 200

    except AIServiceError as error:
        return jsonify({
            "basarili": False,
            "hata": str(error)
        }), 503

    except Exception:
        return jsonify({
            "basarili": False,
            "hata": "Beklenmeyen bir hata oluştu."
        }), 500


@api_bp.route("/leads", methods=["POST"])
def lead_olustur():
    """Yeni müşteri adayını kaydeder."""
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "basarili": False,
                "hata": "Veri gönderilmedi."
            }), 400

        isim = data.get("isim", "").strip()
        telefon = data.get("telefon", "").strip()
        mesaj = data.get("mesaj", "").strip()

        if not isim or not telefon:
            return jsonify({
                "basarili": False,
                "hata": "İsim ve telefon alanları zorunludur."
            }), 400

        lead_ekle(isim, telefon, mesaj)

        return jsonify({
            "basarili": True,
            "mesaj": "Müşteri adayınız başarıyla kaydedildi."
        }), 201

    except Exception:
        return jsonify({
            "basarili": False,
            "hata": "Müşteri adayı kaydedilirken bir hata oluştu."
        }), 500


@api_bp.route("/leads", methods=["GET"])
def leadleri_getir():
    """Kayıtlı müşteri adaylarını getirir."""
    try:
        leads = tum_leadler()

        return jsonify({
            "basarili": True,
            "leads": leads
        }), 200

    except Exception:
        return jsonify({
            "basarili": False,
            "hata": "Müşteri adayları alınırken bir hata oluştu."
        }), 500