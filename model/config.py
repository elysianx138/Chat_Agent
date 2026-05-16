import os
from pathlib import Path


class Settings:
    # === 项目相关管理 ===
    # 项目名称
    # 项目版本号
    APP_NAME = os.getenv("APP_NAME","CHAT_AGENT")
    APP_VERSION = os.getenv("APP_VERSION","1.0.0")

    # === 文件管理模块 ===
    # 允许上传文件
    # 上传文件保存路径
    # json文件保存
    ALLOWED_FILE_EXTENSIONS = [".md"]
    UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR","uploads"))
    DATA_PATH = Path(os.getenv("DATA_PATH","db"))
    DOCUMENTS_REGISTRY_PATH = DATA_PATH / "documents.json"


    # Logging configuration
    def logging_config(self):
        import logging
        from logging import basicConfig
        logging = baseConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logger = logging.getLogger(__name__)




