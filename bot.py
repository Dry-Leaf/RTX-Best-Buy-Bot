from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import info
from selenium_driver import SeleniumDriver

from plyer import notification

import time

def notify() :
    notification.notify (
        title="!!!!!!!!",
        message="MANUAL INPUT REQUIRED",
        app_name="RTX BOT",
        timeout=10
    )


selenium_object = SeleniumDriver()
selenium_object.login(info.email, info.password)

driver = selenium_object.driver
driver.get(info.RTXLINK1)

isComplete = False

notify()
input("Press Enter to continue...")

while not isComplete:
    # find add to cart button
    try:
        atcBtn = WebDriverWait(driver, 6).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".add-to-cart-button"))
        )
    except:
        driver.refresh()
        continue

    print("Add to cart button found")

    try:
        # add to cart
        atcBtn.click()

        time.sleep(100)

        # go to cart and begin checkout as guest
        driver.get("https://www.bestbuy.com/cart")

        checkoutBtn = WebDriverWait(driver, 10).until(
             EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div/div[2]/div/div[1]/div/div[1]/div[1]/section[2]/div/div/div[3]/div/div[1]/button"))
        )
        checkoutBtn.click()
        print("Successfully added to cart - beginning check out")

        #I will try and be logged-in in advance

        # fill in card cvv
        cvvField = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".summary-tile__cvv-code-input"))
        )
        cvvField.send_keys(info.cvv)
        
        print("Attempting to place order")

        # place order
        placeOrderBtn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/main/div[3]/div[1]/div/div[4]/section/div/div/div[2]/div/button"))
        )
        placeOrderBtn.click()

        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".thank-you-enhancement__info"))
        )

        isComplete = True
    except Exception as e:
        # make sure this link is the same as the link passed to driver.get() before looping
        driver.get(info.RTXLINK1)
        print(f"Error - {e}")
        notify()
        input("Press Enter to continue...")
        continue

print("Order successfully placed")



