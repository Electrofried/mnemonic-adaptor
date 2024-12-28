import logging
from pathlib import Path
from typing import Dict, Any
from config import CONFIG

def setup_logging() -> None:
    """Configure logging for the application"""
    log_dir = Path(CONFIG.output_dir) / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_level = logging.INFO
    
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.FileHandler(log_dir / "mnemonic_adaptor.log"),
            logging.StreamHandler()
        ]
    )

def get_logger(name: str) -> logging.Logger:
    """Get a configured logger instance"""
    return logging.getLogger(name)
