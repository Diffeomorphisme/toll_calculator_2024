from pathlib import Path

from app.core.utils import get_logger

logger = get_logger()

BASE_DIR: Path = Path(__file__).parents[1]
