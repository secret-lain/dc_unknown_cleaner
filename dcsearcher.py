import sys
from bs4 import BeautifulSoup
from dcdeleter import Deleter
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

if len(sys.argv) < 4:
    print('valid argument required (ex. python filename.py [galleryname] [username] [password] [?:-m])')

# Set field
gallery_name = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
is_minor = False
if None is sys.argv[4] and sys.argv[4] == '-m':
    is_minor = True

if is_minor:
    gallery_type = '/mgallery'
gallDomain = 'http://gall.dcinside.com'

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome('src/chromedriver.exe', chrome_options=options)
driver.implicitly_wait(3)
# Set field Ended

# address example : http://gall.dcinside.com/board/lists/?id=leagueoflegends1&s_type=search_name&s_keyword=TEST
driver.get(gallDomain + gallery_type + '/board/lists/?id=' + gallery_name + '&s_type=search_name&s_keyword=' + username)
ids = []

# search logic
while True:
    document = BeautifulSoup(driver.page_source, "html.parser")

    # if null, expect gallery is not exist
    board = document.select_one(".list_table")
    nextButton = document.select_one("#dgn_btn_paging > a.b_next")

    if board is None:
        print('Gallery search error. maybe gallery is not exist')
        break

    # get column
    views = board.select('tbody > tr')

    pageCnt = 0
    for col in views:
        notice = col.select('.t_notice')[0].contents[0]
        if notice != '공지':
            ids.append(notice)
            pageCnt += 1

    if pageCnt > 0:
        # if next page button exist(maybe always exist)
        if nextButton is not None:
            driver.get(gallDomain + nextButton.attrs['href'])
            driver.implicitly_wait(5)
    else:
        print('Gallery Search done.')
        print('Found ' + str(len(ids)) + ' objects')
        print('Execute delete logic..')
        break

deleter = Deleter(gallery_name, is_minor)
for view_id in ids:
    deleter.delete_page_using_id(view_id, password)

print('delete process done. check manually')
