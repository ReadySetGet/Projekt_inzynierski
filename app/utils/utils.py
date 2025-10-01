from app.utils.keys import VIEWS_DIR


def load_stylesheet(filename: str) -> str:
    """Load a stylesheet from the specified filename."""
    stylesheet_path = VIEWS_DIR / filename
    return stylesheet_path.read_text()
