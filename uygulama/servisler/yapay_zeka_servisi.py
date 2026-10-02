import os
import requests


class YapayZekaServisHatasi(Exception):
    """Yapay zeka servisi ile ilgili hatalar."""
    pass


class YapayZekaServisi:

    def __init__(self):

        self.api_anahtari = os.getenv(
            "GROQ_API_KEY"
        )

        self.api_url = (
            "https://api.groq.com/openai/v1/chat/completions"
        )

        self.model = "openai/gpt-oss-20b"


    def yanit_uret(
        self,
        mesaj,
        gecmis=None
    ):

        # ------------------------------------
        # API ANAHTARI KONTROLÜ
        # ------------------------------------

        if not self.api_anahtari:

            raise YapayZekaServisHatasi(
                "GROQ_API_KEY bulunamadı."
            )


        # ------------------------------------
        # SYSTEM PROMPT
        # ------------------------------------

        sistem_mesaji = """
Sen THE MACHINE şirketinin Akıllı Satış ve Çözüm Asistanısın.

Görevin, ziyaretçilerin THE MACHINE hakkında sordukları sorulara
doğru, anlaşılır ve profesyonel cevaplar vermektir.

THE MACHINE; yapay zeka ve yüksek performanslı hesaplama
ihtiyaçlarına yönelik çözüm, analiz ve danışmanlık sunar.

THE MACHINE fiziksel ürün satan bir e-ticaret şirketi değildir.

Kullanıcılara özellikle şu konularda yardımcı olabilirsin:

- AI Workstation çözümleri
- AI Server çözümleri
- Yüksek performanslı GPU sistemleri
- Edge Computing çözümleri
- Yapay zeka altyapıları
- İş yükü ve ihtiyaç analizi
- Sistem gereksinimlerinin belirlenmesi
- Teknik çözüm önerileri
- TCO (Toplam Sahip Olma Maliyeti)
- ROI (Yatırım Getirisi)
- Teknik ve finansal uygunluk analizi
- Kullanıcının ihtiyacından gereksiz yere daha güçlü
  veya daha pahalı sistem önermemek

Kullanıcının sorusuna göre cevap ver.

Her kullanıcıya aynı hazır mesajı verme.

Kullanıcı sadece selam verirse kısa ve doğal karşılık ver.

Bilmediğin bir bilgiyi uydurma.

Cevaplarını varsayılan olarak Türkçe ver.
Kullanıcı başka dilde sorarsa uygun şekilde cevap verebilirsin.

Cevapların gereksiz yere çok uzun olmasın.
Profesyonel ama doğal bir dil kullan.
"""


        mesajlar = [
            {
                "role": "system",
                "content": sistem_mesaji
            }
        ]


        # ------------------------------------
        # KONUŞMA GEÇMİŞİ
        # ------------------------------------

        if isinstance(gecmis, list):

            for kayit in gecmis:

                if not isinstance(
                    kayit,
                    dict
                ):
                    continue


                rol = kayit.get(
                    "role"
                )

                icerik = kayit.get(
                    "content"
                )


                if (
                    rol in [
                        "user",
                        "assistant"
                    ]
                    and icerik
                ):

                    mesajlar.append({
                        "role": rol,
                        "content": str(
                            icerik
                        )
                    })


        # ------------------------------------
        # YENİ KULLANICI MESAJI
        # ------------------------------------

        mesajlar.append({
            "role": "user",
            "content": mesaj
        })


        # ------------------------------------
        # GROQ API
        # ------------------------------------

        try:

            cevap = requests.post(

                self.api_url,

                headers={
                    "Authorization":
                        f"Bearer {self.api_anahtari}",

                    "Content-Type":
                        "application/json"
                },

                json={
                    "model":
                        self.model,

                    "messages":
                        mesajlar,

                    "temperature":
                        0.5,

                    "max_tokens":
                        700
                },

                timeout=30
            )


            # HTTP hatasını yakala
            cevap.raise_for_status()


            veri = cevap.json()


            # --------------------------------
            # AI CEVABINI AL
            # --------------------------------

            ai_cevabi = (
                veri
                .get("choices", [])[0]
                .get("message", {})
                .get("content", "")
            )


            if not ai_cevabi:

                raise YapayZekaServisHatasi(
                    "Yapay zeka boş cevap döndürdü."
                )


            return ai_cevabi.strip()


        except requests.exceptions.Timeout:

            raise YapayZekaServisHatasi(
                "Yapay zeka servisi zaman aşımına uğradı."
            )


        except requests.exceptions.RequestException as hata:

            print(
                "GROQ API HATASI:",
                hata
            )

            if hasattr(
                hata,
                "response"
            ) and hata.response is not None:

                print(
                    "GROQ CEVABI:",
                    hata.response.text
                )


            raise YapayZekaServisHatasi(
                "Yapay zeka servisine bağlanılamadı."
            )


        except (
            KeyError,
            IndexError,
            TypeError
        ) as hata:

            print(
                "GROQ CEVAP AYRIŞTIRMA HATASI:",
                hata
            )

            raise YapayZekaServisHatasi(
                "Yapay zeka cevabı okunamadı."
            )


# =========================================================
# SERVİS NESNESİ
# =========================================================

yapay_zeka_servisi = YapayZekaServisi()