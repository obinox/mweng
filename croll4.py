from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


class CommentUploader:
    def __init__(self, urls, comment_files, comment_box_selector, submit_button_selector):
        self.urls = urls
        self.comment_files = comment_files
        self.comment_box_selector = comment_box_selector
        self.submit_button_selector = submit_button_selector
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        if len(self.urls) != len(self.comment_files):
            raise ValueError("URLs와 댓글 파일들의 수가 일치하지 않습니다.")

    def load_comment(self, comment_file):
        # 댓글 파일 하나 열기
        if not os.path.exists(comment_file):
            raise FileNotFoundError(f"댓글 파일이 존재하지 않습니다: {comment_file}")
        
        with open(comment_file, "r", encoding="utf-8") as f:
            comment = f.read().strip()
        
        return comment

    def login(self):
        self.driver.get("https://nid.naver.com/nidlogin.login")
        input("로그인을 완료하고 Enter를 누르세요...")
        time.sleep(1)

    def wait_for_page_load(self, url):
        self.driver.get(url)
        time.sleep(3)

    def upload_comments(self):
        for idx, (url, comment_file) in enumerate(zip(self.urls, self.comment_files)):
            self.wait_for_page_load(url)
            comment = self.load_comment(comment_file)

            try:
                # 필요시 iframe 이동
                # self.driver.switch_to.frame("iframe 이름 또는 id")
                
                # 댓글 입력창 찾기
                comment_box = self.driver.find_element(By.CSS_SELECTOR, self.comment_box_selector)
                comment_box.clear()
                comment_box.send_keys(comment)
                time.sleep(0.5)

                # 등록 버튼 클릭
                submit_button = self.driver.find_element(By.CSS_SELECTOR, self.submit_button_selector)
                submit_button.click()

                print(f"[{idx+1}] {url}에 댓글 작성 완료 ({comment_file})")
                time.sleep(2)

                # self.driver.switch_to.default_content()  # iframe 썼으면 원래 페이지로 돌아오기

            except Exception as e:
                print(f"[{idx+1}] {url}에 댓글 작성 실패 ({comment_file}): {e}")

    def close(self):
        self.driver.quit()


# 사용 예시
url_prefix = "https://cafe.naver.com/ca-fe/cafes/x/articles/"
from urls import urls  # [123, 456, 789, ...] 이런 식

# 댓글 파일 리스트
# 예를 들면: ["comments/123.txt", "comments/456.txt", "comments/789.txt"]
comment_files = [f"./notes/{u}.txt" for u in urls]

comment_box_selector = "textarea.comment_inbox_text"  # CSS 선택자 (수정 필요)
submit_button_selector = "a.btn_register"  # CSS 선택자 (수정 필요)

uploader = CommentUploader(
    [url_prefix + str(u) for u in urls],
    comment_files,
    comment_box_selector,
    submit_button_selector
)

uploader.login()
uploader.upload_comments()
uploader.close()