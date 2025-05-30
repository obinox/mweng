from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import os
import urllib.parse


class ImageDownloader:
    def __init__(self, urls, image_class):
        self.urls = urls
        self.image_class = image_class
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def login(self):
        # 로그인 페이지로 이동 (여기서는 네이버 예시)
        self.driver.get("https://nid.naver.com/nidlogin.login")

        input()

        time.sleep(1)  # 로그인 후 로딩 대기

    def wait_for_page_load(self, url):
        self.driver.get(url)
        time.sleep(2)  # 페이지 로드 대기

    def download_images(self):
        for url in self.urls:
            self.wait_for_page_load(url)
            self.extract_and_save_images(url)

    def extract_and_save_images(self, url: str):
        # URL 별 폴더 생성
        folder_name = url.split("/")[-1]  # URL에서 도메인 추출
        folder_path = os.path.join("./downloaded_images", folder_name)
        os.makedirs(folder_path, exist_ok=True)

        # 이미지 요소들 찾기 (클래스 기준)
        img_elements = self.driver.find_elements(By.CLASS_NAME, self.image_class)

        img_urls: list[str] = []
        for img in img_elements:
            img_url = img.get_attribute("src")
            if img_url:
                img_urls.append(img_url)

        print(f"URL: {url}")
        print(f"총 {len(img_urls)}개의 이미지 URL이 발견되었습니다.")

        # 이미지 다운로드
        for idx, img_url in enumerate(img_urls):
            try:
                img_data = requests.get(img_url).content
                img_name = img_url.split("/")[-1].split("?")[0]
                decoded_name = urllib.parse.unquote(img_name)
                with open(f"{folder_path}/{decoded_name}", "wb") as file:
                    file.write(img_data)
                print(f"이미지 {idx+1} 저장 완료: {img_url}")
            except Exception as e:
                print(f"이미지 다운로드 실패: {img_url} | {e}")

    def close(self):
        self.driver.quit()


# 사용 예시
url_pfix = "https://cafe.naver.com/ca-fe/cafes/x/articles/"
from urls import urls

image_class = "se-image-resource"  # 이미지가 포함된 클래스명

# 이미지 다운로드 시작
downloader = ImageDownloader([url_pfix + str(u) for u in urls], image_class)
downloader.login()  # 로그인
downloader.download_images()
downloader.close()
