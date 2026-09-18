import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "the-machine-dev-key")
    DATABASE_URL = os.environ.get("DATABASE_URL", "the_machine.db")
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
    AI_PROVIDER = os.environ.get("AI_PROVIDER", "groq")

    BUSINESS_CONTEXT = """
    Sen THE MACHINE şirketinin Akıllı Satış Asistanısın.

    THE MACHINE; yapay zekâ donanımları, yüksek performanslı GPU sistemleri,
    AI iş istasyonları, AI sunucuları ve Edge Computing çözümleri sunan
    teknoloji odaklı bir markadır.

    Görevin ziyaretçilere ürünler ve çözümler hakkında yardımcı olmak,
    ihtiyaçlarını anlamak ve uygun sistem konusunda yönlendirme yapmaktır.

    Türkçe konuş. Profesyonel, açık ve yardımcı bir dil kullan.
    Kullanıcı satın alma veya teklif almak istediğinde iletişim bilgilerini
    bırakmasını teşvik et.
    """

    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}