import requests
import truststore

truststore.inject_into_ssl()

from config import Config


class AIServiceError(Exception):
    """Yapay zekâ servisiyle ilgili hataları temsil eder."""
    pass


class AIService:
    """THE MACHINE için yapay zekâ servisini yönetir."""

    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.model = "openai/gpt-oss-20b"
        self.url = "https://api.groq.com/openai/v1/chat/completions"

    def _sistem_talimati(self):
        """Yapay zekânın işletme bağlamını döndürür."""
        return Config.BUSINESS_CONTEXT

    def yanit_uret(self, mesaj, gecmis=None):
        """Kullanıcı mesajına yapay zekâdan yanıt üretir."""

        if not self.api_key:
            return (
                "Demo modu: Şu anda yapay zekâ API anahtarı "
                "yapılandırılmamış durumda."
            )

        if gecmis is None:
            gecmis = []

        messages = [
            {
                "role": "system",
                "content": self._sistem_talimati()
            }
        ]

        messages.extend(gecmis)

        messages.append({
            "role": "user",
            "content": mesaj
        })

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "messages": messages
        }

        try:
            response = requests.post(
                self.url,
                headers=headers,
                json=data,
                timeout=30
            )

            response.raise_for_status()

            result = response.json()

            return result["choices"][0]["message"]["content"]

        except (requests.RequestException, KeyError, IndexError) as error:
            raise AIServiceError(
                "Yapay zekâ servisine ulaşılamadı."
            ) from error


ai_service = AIService()