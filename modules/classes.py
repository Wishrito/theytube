import os
import time
from pathlib import Path

from dotenv import load_dotenv
from flask import Blueprint, Flask
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from modules.utils import get_chromedriver_path

load_dotenv()


class Duration:
    def __init__(self, seconds: int):
        if seconds < 0:
            raise ValueError("Seconds can't be less than 0")

        self.hours = f"{seconds // 3600}"
        match len(self.hours):
            case 1:
                self.hours = "0" + self.hours
            case 0:
                self.hours = "00"

        reste = seconds % 3600

        self.minutes = f"{reste // 60}"
        match len(self.minutes):
            case 1:
                self.minutes = "0" + self.minutes
            case 0:
                self.minutes = "00"

        self.seconds = f"{reste % 60}"
        match len(self.seconds):
            case 1:
                self.seconds = "0" + self.seconds
            case 0:
                self.seconds = "00"

    def __str__(self):
        return f"{self.hours} h {self.minutes} min {self.seconds} s"

    def to_dict(self):
        return {"hours": self.hours, "minutes": self.minutes, "seconds": self.seconds}


class YTBVideo:
    def __init__(
        self,
        title: str,
        url: str,
        duration: int,
        channel: str,
        id: str,
        thumbnail: str = None,
    ) -> None:
        self.title = title
        self.url = url
        self.duration = Duration(duration)
        self.channel = channel
        self.id = id
        self.thumbnail = thumbnail

    def to_dict(self) -> dict:
        video_dict = {
            "title": self.title,
            "video_url": self.url,
            "duration": {
                "hours": self.duration.hours,
                "minutes": self.duration.minutes,
                "seconds": self.duration.seconds,
            },
            "channel": self.channel,
            "id": self.id,
        }
        if self.thumbnail is not None:
            video_dict["thumbnail"] = self.thumbnail
        return video_dict


class AdlessYTBPlayer(Flask):
    def __init__(self, import_name, static_url_path = None, static_folder = "static", static_host = None, host_matching = False, subdomain_matching = False, template_folder = "templates", instance_path = None, instance_relative_config = False, root_path = None):
        super().__init__(
            self.__class__.__name__,
            static_url_path,
            static_folder,
            static_host,
            host_matching,
            subdomain_matching,
            template_folder,
            instance_path,
            instance_relative_config,
            root_path,
        )
        self.localhost = os.environ.get("LOCALHOST")
        self.template_folder = Path(__file__).parent.parent / "templates"
        self.static_folder = Path(__file__).parent.parent / "src"
        self.webCookies: str = ""

    def get_cookies(self):
        service = Service(executable_path=get_chromedriver_path())
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options, service=service)
        driver.get("https://www.youtube.com/")
        time.sleep(5)  # Wait for the page to load
        selenium_cookies = driver.get_cookies()
        cookies_dict = {cookie["name"]: cookie["value"] for cookie in selenium_cookies}
        # Convertir en string formaté pour l'en-tête HTTP
        cookie_header = "; ".join([f"{k}={v}" for k, v in cookies_dict.items()])

        driver.quit()
        # Enregistrer les cookies dans une variable
        self.webCookies = cookie_header
        return cookie_header


app = AdlessYTBPlayer(__name__)

history_bp = Blueprint("history", __name__, url_prefix="/history")
