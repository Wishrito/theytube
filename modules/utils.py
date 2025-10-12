from pathlib import Path
import platform

def get_chromedriver_path() -> Path:
    base_dir = Path("src") / "drivers"
    system = platform.system()

    driver_path = base_dir / (
        "chromedriver.exe" if system not in ["Linux", "Darwin"] else "chromedriver"
    )
    return driver_path.resolve()
