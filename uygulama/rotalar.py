from flask import Blueprint, jsonify, request

from uygulama.veritabani import aday_kaydet

from uygulama.servisler.yapay_zeka_servisi import (
    yapay_zeka_servisi,
    YapayZekaServisHatasi
)


api_arayuzu = Blueprint(
    "api",
    __name__
)


# =========================================================
# API ÇALIŞIYOR MU?
# =========================================================

@api_arayuzu.route(
    "/saglik-durumu",
    methods=["GET"]
)
def saglik_durumu():

    return jsonify({
        "basari": True,
        "durum": "THE MACHINE API çalışıyor."
    }), 200


# =========================================================
# WIX İLETİŞİM FORMU
# =========================================================

@api_arayuzu.route(
    "/iletisim",
    methods=["POST"]
)
def iletisim_formu():

    try:

        veri = request.get_json(
            silent=True
        ) or {}


        email = str(
            veri.get("email", "")
        ).strip()


        isim = str(
            veri.get("isim", "")
        ).strip()


        soyisim = str(
            veri.get("soyisim", "")
        ).strip()


        telefon = str(
            veri.get("telefon", "")
        ).strip()


        mesaj = str(
            veri.get("mesaj", "")
        ).strip()


        kvkk = veri.get(
            "kvkk",
            False
        )


        if isinstance(kvkk, str):

            kvkk = kvkk.lower() in [
                "true",
                "1",
                "evet",
                "onaylı",
                "onaylandi",
                "onaylandı"
            ]


        if not isim:

            return jsonify({
                "basari": False,
                "hata": "İsim alanı zorunludur."
            }), 400


        if not telefon:

            return jsonify({
                "basari": False,
                "hata": "Telefon alanı zorunludur."
            }), 400


        aday_id = aday_kaydet(
            email=email,
            isim=isim,
            soyisim=soyisim,
            telefon=telefon,
            mesaj=mesaj,
            kvkk=kvkk
        )


        print("")
        print("======================================")
        print("YENİ WIX MÜŞTERİ ADAYI")
        print("======================================")
        print("ID:", aday_id)
        print("E-posta:", email)
        print("İsim:", isim)
        print("Soyisim:", soyisim)
        print("Telefon:", telefon)
        print("Mesaj:", mesaj)
        print("KVKK:", kvkk)
        print("======================================")
        print("")


        return jsonify({
            "basari": True,
            "mesaj": "Form başarıyla kaydedildi.",
            "aday_id": aday_id
        }), 201


    except Exception as hata:

        print(
            "WIX FORM HATASI:",
            hata
        )

        return jsonify({
            "basari": False,
            "hata": str(hata)
        }), 500


# =========================================================
# WIX CHATBOT
# =========================================================

@api_arayuzu.route(
    "/sohbet",
    methods=["POST"]
)
def sohbet():

    try:

        veri = request.get_json(
            silent=True
        ) or {}


        mesaj = str(
            veri.get("mesaj", "")
        ).strip()


        gecmis = veri.get(
            "gecmis",
            []
        )


        if not mesaj:

            return jsonify({
                "basari": False,
                "hata": "Mesaj boş bırakılamaz."
            }), 400


        cevap = yapay_zeka_servisi.yanit_uret(
            mesaj,
            gecmis
        )


        return jsonify({
            "basari": True,
            "cevap": cevap
        }), 200


    except YapayZekaServisHatasi as hata:

        return jsonify({
            "basari": False,
            "hata": str(hata)
        }), 503


    except Exception as hata:

        print(
            "CHATBOT HATASI:",
            hata
        )

        return jsonify({
            "basari": False,
            "hata": str(hata)
        }), 500