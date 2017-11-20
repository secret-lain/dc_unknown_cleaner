from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Deleter:
    baseUrl = 'http://gall.dcinside.com/board/delete/?id='
    galleryId = ''

    def __init__(self, gallery, is_minor):
        self.set_gallery_name(gallery)
        if is_minor:
            self.baseUrl = 'http://gall.dcinside.com/mgallery/board/delete/?id='

    def set_gallery_name(self, gallery):
        self.galleryId = gallery

    def get_request_url(self):
        return self.baseUrl + self.galleryId

    # function call each Browser(maybe)
    def delete_page_using_id(self, view_id, password):
        if self.galleryId == '':
            print('GalleryId is not set')
            return

        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome('src/chromedriver.exe', chrome_options=options)
        driver.implicitly_wait(3)

        driver.get(self.baseUrl + self.galleryId + '&no=' + view_id)

        driver.find_element_by_name('password').send_keys(password)
        submit = driver.find_element_by_css_selector('#delete > ul > li.t_btn > input')
        submit.click()

        driver.implicitly_wait(1)
        alert = driver.switch_to.alert
        alert.accept()
        driver.implicitly_wait(2)
        print('id' + view_id + ' has deleted.')