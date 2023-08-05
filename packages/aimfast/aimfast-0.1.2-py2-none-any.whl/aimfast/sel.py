import time
from selenium import webdriver

profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2)  # custom location
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir', '/tmp')
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'image/png')

driver = webdriver.Firefox(firefox_profile=profile)
driver.get("file:///home/athanaseus/Documents/Rhodes_MSc/git@RadioAstronomy/aimfast/aimfast/InputOutputFluxDensity.png.html")
export_button = driver.find_element_by_xpath(
                    "//a[@data-title='Download plot as a png']")
export_button.click()
time.sleep(2)
driver.quit()
