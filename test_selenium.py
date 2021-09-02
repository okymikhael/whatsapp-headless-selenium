from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

# QR Terminal
from pyzbar import pyzbar
import qrcode_terminal
from PIL import Image
import base64



options = Options()
# options.add_argument("--user-data-dir=chrome-data") # Should be work on Linux for session
options.add_argument('--headless')
options.add_argument("user-agent=User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")
# options.add_argument('--disable-gpu')  # Last I checked this was necessary.
# options.headless = True
# options.add_argument("--window-size=0,0")
driver = webdriver.Chrome('./driver/chromedriver', options=options)
driver.get('https://web.whatsapp.com')

# Show qr on Terminal
while True:
    try:
        time.sleep(2)
        canvas_qr = driver.find_element_by_xpath("/html/body/div/div[1]/div/div[2]/div[1]/div/div[2]/div/canvas")
        canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas_qr)
        canvas_png = base64.b64decode(canvas_base64)
        with open(r"canvas.png", 'wb') as f:
            f.write(canvas_png)
        time.sleep(2)
        img = Image.open('canvas.png')
        output = pyzbar.decode(img)
        qrcode_terminal.draw(output[0][0].decode())
    except NoSuchElementException:  #spelling error making this code not work as expected
        break
    
    try:
        refresh_qr = driver.find_element_by_xpath('/html/body/div/div[1]/div/div[2]/div[1]/div/div[2]/div/span/button')
        if refresh_qr:
            refresh_qr.click()
        if driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/div[3]/div/div[1]/div/label/div/div[2]'):
            break
    except NoSuchElementException:  #spelling error making this code not work as expected
        print("Trying to getting QR Code")
        pass
    
print("You're logged in")

while True:
    phone = input("Enter Phone Number: ")
    msg = input("Enter Message: ")
    driver.get('https://wa.me/{}?text={}'.format(phone,msg))
    WebDriverWait(driver,50).until(lambda driver: driver.find_element_by_xpath('//*[@id="action-button"]')).click()
    time.sleep(2)
    WebDriverWait(driver,50).until(lambda driver: driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div/div/div[2]/div/div/a')).click()
    time.sleep(2)
    WebDriverWait(driver,50).until(lambda driver: driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]/button')).click()
    