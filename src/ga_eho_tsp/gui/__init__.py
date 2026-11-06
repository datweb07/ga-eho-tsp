"""Desktop GA; import package không khởi tạo Tk hoặc Matplotlib."""


def main() -> int:
    """Khởi động cùng ứng dụng cho Demo.py và python -m."""
    from .app import main as launch

    return launch()
