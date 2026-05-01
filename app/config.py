from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centraliza as configurações e variáveis de ambiente da aplicação.
    Utiliza o pydantic-settings para validação e parse automático.
    """

    llm_api_url: str = (
        "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
    )
    llm_api_key: str = ""
    llm_model: str = "gemini-2.5-flash"

    # O Pydantic carregará automaticamente de um arquivo .env, caso exista.
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


# Instância singleton pronta para ser importada por qualquer módulo
settings = Settings()
