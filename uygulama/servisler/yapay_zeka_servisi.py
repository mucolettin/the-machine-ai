import requests

from flask import current_app


class YapayZekaServisHatasi(Exception):
    """THE MACHINE yapay zekâ servisinde oluşan hatalar."""
    pass


class YapayZekaServisi:

    GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

    GROQ_MODEL = "openai/gpt-oss-20b"

    def yanit_uret(
        self,
        kullanici_mesaji,
        sohbet_gecmisi=None
    ):

        saglayici = current_app.config.get(
            "AI_PROVIDER",
            "groq"
        ).lower()

        if saglayici == "groq":

            return self._groq_cagir(
                kullanici_mesaji,
                sohbet_gecmisi
            )

        raise YapayZekaServisHatasi(
            f"Desteklenmeyen AI sağlayıcısı: {saglayici}"
        )

    def _groq_cagir(
        self,
        kullanici_mesaji,
        sohbet_gecmisi=None
    ):

        api_key = current_app.config.get(
            "GROQ_API_KEY",
            ""
        )

        # API anahtarı yoksa demo modu
        if not api_key:
            return self._demo_yaniti_ver()

        # ayarlar.py içindeki THE MACHINE bilgileri
        system_talimati = current_app.config.get(
            "BUSINESS_CONTEXT",
            """
            Sen THE MACHINE şirketinin
            yapay zekâ destekli satış ve
            çözüm asistanısın.
            """
        )

        mesajlar = [
            {
                "role": "system",
                "content": system_talimati
            }
        ]

        # Önceki konuşmaları ekle
        if sohbet_gecmisi:

            for mesaj in sohbet_gecmisi[-10:]:

                if not isinstance(mesaj, dict):
                    continue

                rol = mesaj.get("role")
                icerik = mesaj.get("content")

                if (
                    rol in ["user", "assistant"]
                    and isinstance(icerik, str)
                    and icerik.strip()
                ):

                    mesajlar.append({
                        "role": rol,
                        "content": icerik.strip()
                    })

        # Kullanıcının yeni mesajı
        mesajlar.append({
            "role": "user",
            "content": kullanici_mesaji
        })

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        veri = {
            "model": self.GROQ_MODEL,
            "messages": mesajlar,
            "temperature": 0.4,
            "max_tokens": 500
        }

        try:

            cevap = requests.post(
                self.GROQ_URL,
                headers=headers,
                json=veri,
                timeout=60
            )

            cevap.raise_for_status()

            sonuc = cevap.json()

            return (
                sonuc["choices"][0]
                ["message"]
                ["content"]
            )

        except requests.RequestException as hata:

            raise YapayZekaServisHatasi(
                f"Groq bağlantı hatası: {hata}"
            )

        except (
            KeyError,
            IndexError,
            TypeError
        ):

            raise YapayZekaServisHatasi(
                "THE MACHINE AI servisinden "
                "beklenen yanıt alınamadı."
            )

    def _demo_yaniti_ver(self):

        return (
            "Merhaba! Ben THE MACHINE Akıllı Satış "
            "ve Çözüm Asistanıyım. Şu anda demo "
            "modunda çalışıyorum. AI Workstation, "
            "AI Server, yüksek performanslı GPU "
            "sistemleri ve Edge Computing çözümleri "
            "hakkında yardımcı olabilirim."
        )


yapay_zeka_servisi = YapayZekaServisi()