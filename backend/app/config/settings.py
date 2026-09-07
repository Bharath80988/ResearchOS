import os
from functools import lru_cache
from typing import Optional, List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # App & Server
    FLASK_ENV: str = Field(default="development", alias="FLASK_ENV")
    FLASK_DEBUG: bool = Field(default=True, alias="FLASK_DEBUG")
    PORT: int = Field(default=5000, alias="PORT")
    HOST: str = Field(default="0.0.0.0", alias="HOST")
    SECRET_KEY: str = Field(default="researchos-dev-secret-key", alias="SECRET_KEY")

    # Database
    DATABASE_URL: str = Field(
        default="postgresql://researchos:researchos@localhost:5432/researchos_db",
        alias="DATABASE_URL"
    )
    DATABASE_TEST_URL: str = Field(
        default="sqlite:///./test_researchos.db",
        alias="DATABASE_TEST_URL"
    )

    # Redis & Celery
    REDIS_URL: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")
    CELERY_BROKER_URL: str = Field(default="redis://localhost:6379/0", alias="CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = Field(default="redis://localhost:6379/0", alias="CELERY_RESULT_BACKEND")
    CELERY_TASK_ALWAYS_EAGER: bool = Field(default=True, alias="CELERY_TASK_ALWAYS_EAGER")

    # LLM Settings & Free Model Routing
    DEFAULT_LLM_PROVIDER: str = Field(default="openrouter", alias="DEFAULT_LLM_PROVIDER")
    DEFAULT_REASONING_MODEL: str = Field(default="deepseek/deepseek-r1:free", alias="DEFAULT_REASONING_MODEL")
    DEFAULT_FAST_MODEL: str = Field(default="meta-llama/llama-3.3-70b-instruct:free", alias="DEFAULT_FAST_MODEL")
    DEFAULT_WORKER_MODEL: str = Field(default="llama-3.1-8b-instant", alias="DEFAULT_WORKER_MODEL")
    DEFAULT_EMBEDDING_MODEL: str = Field(default="sentence-transformers/all-MiniLM-L6-v2", alias="DEFAULT_EMBEDDING_MODEL")

    # API Keys for Free & Standard Providers
    HUGGINGFACE_API_KEY: Optional[str] = Field(default=None, alias="HUGGINGFACE_API_KEY")
    OPENROUTER_API_KEY: Optional[str] = Field(default=None, alias="OPENROUTER_API_KEY")
    GROQ_API_KEY: Optional[str] = Field(default=None, alias="GROQ_API_KEY")
    GEMINI_API_KEY: Optional[str] = Field(default=None, alias="GEMINI_API_KEY")

    # Multi-AI Worker Sharding Configuration
    WORKER_BATCH_SIZE: int = Field(default=10, alias="WORKER_BATCH_SIZE") # E.g. 10 sources per AI worker
    MAX_PARALLEL_WORKERS: int = Field(default=4, alias="MAX_PARALLEL_WORKERS")

    # Search Providers
    TAVILY_API_KEY: Optional[str] = Field(default=None, alias="TAVILY_API_KEY")
    SERPER_API_KEY: Optional[str] = Field(default=None, alias="SERPER_API_KEY")
    SEMANTIC_SCHOLAR_API_KEY: Optional[str] = Field(default=None, alias="SEMANTIC_SCHOLAR_API_KEY")
    PUBMED_API_KEY: Optional[str] = Field(default=None, alias="PUBMED_API_KEY")
    GITHUB_TOKEN: Optional[str] = Field(default=None, alias="GITHUB_TOKEN")
    REDDIT_CLIENT_ID: Optional[str] = Field(default=None, alias="REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET: Optional[str] = Field(default=None, alias="REDDIT_CLIENT_SECRET")
    REDDIT_USER_AGENT: str = Field(default="ResearchOS/2.0", alias="REDDIT_USER_AGENT")

    # Research Engine Limits & Budgets
    MAX_RESEARCH_ITERATIONS: int = Field(default=5, alias="MAX_RESEARCH_ITERATIONS")
    MAX_SEARCH_QUERIES_PER_STEP: int = Field(default=5, alias="MAX_SEARCH_QUERIES_PER_STEP")
    MAX_SOURCES_PER_RUN: int = Field(default=30, alias="MAX_SOURCES_PER_RUN")
    MAX_CRAWL_CONCURRENCY: int = Field(default=5, alias="MAX_CRAWL_CONCURRENCY")
    EMBEDDING_CHUNK_SIZE: int = Field(default=512, alias="EMBEDDING_CHUNK_SIZE")
    EMBEDDING_CHUNK_OVERLAP: int = Field(default=64, alias="EMBEDDING_CHUNK_OVERLAP")
    RERANKER_TOP_K: int = Field(default=10, alias="RERANKER_TOP_K")

    # Crawler Safeguards
    CRAWL_TIMEOUT_SECONDS: int = Field(default=15, alias="CRAWL_TIMEOUT_SECONDS")
    CRAWL_USER_AGENT: str = Field(default="ResearchOS-Bot/2.0", alias="CRAWL_USER_AGENT")
    BLOCKED_IP_RANGES: str = Field(
        default="127.0.0.0/8,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,169.254.0.0/16",
        alias="BLOCKED_IP_RANGES"
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()
