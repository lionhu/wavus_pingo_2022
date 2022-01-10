from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

CHROMEDRIVER = "chromedriver.exeのパス"
URL = "https://fx.dmm.com/market/chart/?utm_source=google&utm_medium=cpc&utm_campaign=dsa&utm_campaign=admg_11267_14955_531442_531541&utm_content=fx&utm_source=google&utm_medium=cpc&gclid=CjwKCAjwh5qLBhALEiwAioods_zOg1vgceorNg-v1j7jgqjJCwajOotOvwMFpL1disKE6K6AYvqwfBoCe90QAvD_BwE"

options = Options()
# スクロールバーを非表示にする
options.add_argument('--hide-scrollbars')
# シークレットモードでChromeを起動する
options.add_argument('--incognito')
# ブラウザを表示しない
options.add_argument('--headless')

driver = webdriver.Remote(os.environ["SELENIUM_URL"], options=options)

# ウィンドウサイズ＝画像サイズ
driver.set_window_size(1024, 768)
# 対象ページへアクセス
driver.get(URL)
# スクリーンショットを取得
driver.save_screenshot('result.png')

driver.quit()
