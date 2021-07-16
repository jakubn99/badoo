
# Import modules
####################################################################
import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from twilio.rest import Client
from time import sleep, time
import requests
from PIL import Image
from io import BytesIO

# Website navigation functions
####################################################################

def getLastPoint(path):
    listBadoo = os.listdir(path)
    countDict = {}
    if len(listBadoo) != 1:
        for name in listBadoo:
            name = name.split(sep='_')
            if len(name) == 4:
                num = int(name[2])
                if num in countDict.keys():
                    countDict[num] += 1
                else: countDict[num] = 1
        
        return max(countDict.keys())
    else:
        return 0

def login(username, password):
    loginInput = driver.find_element_by_xpath('//*[@class="text-field__input text-field__input--ltr js-signin-login"]')
    passwordInput = driver.find_element_by_xpath('//*[@class="text-field__input js-signin-password"]')
    confirmButton = driver.find_element_by_xpath('//*[@id="page"]/div[1]/div[3]/section/div/div/div[1]/form/div[5]/div/div[1]/button')
    action = ActionChains(driver)
    action.move_to_element(loginInput).click().send_keys(username)
    action.move_to_element(passwordInput).click().send_keys(password)
    action.perform()
    sleep(2)
    confirmButton.click()

def checkOrientation(pref):
    shouldBeScraped = False
    endings = ['p[2]', 'p', 'p[1]']
    for end in endings:
        try:
            info = driver.find_element_by_xpath('//*[@id="mm_cc"]/div[1]/div/div/div[1]/div/div[2]/div[2]/div/div[2]/div/' + end).text 
            if pref == 1:
                if 'gej' in info or 'Gej' in info:
                    shouldBeScraped = True
            elif pref == 2 or pref == 4:
                if 'hetero' in info or 'Hetero' in info:
                    shouldBeScraped = True
            elif pref == 3:
                if 'lesb' in info or 'Lesb' in info:
                    shouldBeScraped = True
            break
        except:
            pass
    return shouldBeScraped

def scrapeData(path, pref, num, limit=5):
    doesNextButtonExist = True
    name = driver.find_element_by_xpath('//*[@id="mm_cc"]/div[1]/div/div/div[1]/div/div[1]/div/div[1]/div[2]/h1/span[1]').text
    age = driver.find_element_by_xpath('//*[@id="mm_cc"]/div[1]/div/div/div[1]/div/div[1]/div/div[1]/div[2]/h1/span[2]').text[2:]
    total = int(driver.find_element_by_xpath('//*[@class="js-gallery-photo-total js-gallery-total"]').text)
    if total > limit:
        total = limit
    try:
        nextPhotoButton = driver.find_element_by_xpath('//*[@id="mm_cc"]/div[1]/section/div/div[1]/div/span[2]')
    except:
        doesNextButtonExist = False
    
    for i in range(total):

        pid = str(pref)+'_'+name+age+'_'+str(num)+'_'+str(i+1)
        print(pid)
        image = driver.find_element_by_xpath('//*[@class="photo-gallery__photo-bg js-mm-photo"]')
        imageURL = image.value_of_css_property("background-image").replace('url("', '').replace('")', '')
        res = requests.get(imageURL)
        imageFinal = Image.open(BytesIO(res.content)).convert("RGB")
        imageFinal.save(path + '/'+ pid + '.png')
        if doesNextButtonExist == True:
            action = ActionChains(driver)
            action.move_to_element(nextPhotoButton).click()
            action.perform()
        

def swipeLeft():
    rejectButton = driver.find_element_by_xpath('//*[@id="mm_cc"]/div[1]/section/div/div[2]/div/div[2]/div[2]/div[1]')
    rejectButton.click()
    sleep(2)



# C O D E   E X E C U T I O N
####################################################################
####################################################################

#   1 - gay men           
#   2 - hetero men        
#   3 - lesbian women     
#   4 - hetero women     

pref = 1
goal = 1000

path = '/Users/jakubniewiadomski/Desktop/badoo_pics2'
username = 'jakubn99@gmail.com'
password = 'n*KU28BAN*99'
length = getLastPoint(path)
threshold = goal+length

os.system('clear')
start_time = time()
driver = webdriver.Chrome()
driver.get('https://badoo.com/pl/signin/')
sleep(3)

login(username, password)
sleep(15)

while length != threshold:
    if checkOrientation(pref):
        length += 1
        scrapeData(path, pref, length)
    swipeLeft()

duration = time() - start_time
os.system('clear')
print('Done.')
print("Scraping time: " + str(round(duration, 2)) + " seconds.")

driver.quit()

