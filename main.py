import random
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from fake_useragent import UserAgent
from playsound import playsound
from selenium.webdriver.common.proxy import Proxy, ProxyType
#from proxymanager import ProxyManager
from fp.fp import FreeProxy


check_count = 0
round_count = 0

def set_proxy(profile):
    PROXY_HOST = "203.142.69.67"
    PROXY_PORT = 8080

    profile.set_preference("network.proxy.type", 1)
    profile.set_preference("network.proxy.http", PROXY_HOST)
    profile.set_preference("network.proxy.http_port", PROXY_PORT)
    profile.update_preferences()

def set_proxy():
    myProxy = "203.142.69.67:8080"

    proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': myProxy,
        'ftpProxy': myProxy,
        'sslProxy': myProxy,
        'noProxy': ''  # set this value as desired
    })
    return proxy

addresses = ["129.146.180.91:3128", "38.102.153.210:3128", "168.138.211.5:8080", "192.241.172.93:8080",
                 "105.27.116.46:30032", "44.229.45.197:33128", "209.212.33.99:8080", "194.250.57.253:8080",
                  "70.169.141.35:3128", "161.35.70.249:1080", "46.4.96.137:1080",
                 "88.198.50.103:1080", "154.16.202.22:1080", "176.9.119.170:1080", "88.198.24.108:1080",
                 "81.255.13.197:8080", "51.158.123.35:9999", "103.156.225.178:8080", "139.0.137.64:8080"
                 ]

def set_capabilities():


    #proxy = random.choice(addresses)
    proxy = FreeProxy(timeout=0.3, rand=True).get()
    proxy = proxy[7:]
    print(proxy)
    firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True
    firefox_capabilities['proxy'] = {
        "proxyType": "MANUAL",
        "httpProxy": proxy,
        "ftpProxy": proxy,
        "sslProxy": proxy
    }
    return firefox_capabilities


def try_get_content_by_class_name(browser, name):
    try:
        content = browser.find_element_by_class_name(name)
        return content
    except:
        print("Bot got blocked")
        return False


def CheckOnePage(url):
    #profile = webdriver.FirefoxProfile()
    #set_proxy(profile)
    opts = Options()
    opts.headless = True
    ua = UserAgent()
    userAgent = ua.random
    print('------------------------')
    print(userAgent)
    # random user agent
    opts.add_argument(f'user-agent={userAgent}')
    # random viewport size
    #browser = webdriver.Firefox(options=opts, proxy=set_proxy())
    #browser = webdriver.Firefox(options=opts, firefox_profile=profile)
    browser = webdriver.Firefox(options=opts, capabilities=set_capabilities())
    #browser.set_page_load_timeout(10)
    #browser = webdriver.Firefox(options=opts)
    browser.delete_all_cookies()
    browser.set_window_size(random.randint(720, 1920), random.randint(720, 1920))
    try:
        browser.get(url)
    except:
        print('Timeout proxy is slow')
        #print(set_capabilities().get('proxy')['httpProxy'])
        #addresses.remove(set_capabilities().get('proxy')['httpProxy'])
        return

    # print(browser.page_source)

    # assert "Python" in driver.title
    # elem = browser.find_elements_by_name("main-title")
    #content = browser.find_element_by_class_name('main-title')
    content = try_get_content_by_class_name(browser, 'main-title')
    if content:
        print('content.text: ' + content.text)
        if content.text == "Oops!" or content.text == "Hoppla!" or content.text == "Oups !" or content.text == "Ops!":
            print("No bag")

        else:
            # content = browser.find_element_by_class_name('product-item-name')
            content = try_get_content_by_class_name(browser, 'product-item-name')
            print('content.text: ' + content.text)
            if content.text != "Picotin Equipages d'Hermès" and content.text != 'Mueble auxiliar "picotin" Équipages d’Hermès':
                print('Found bag at ' + url)
                playsound('alarm.mp3')

    print(url)
    time.sleep(10)
    browser.close()


urls = ["https://www.hermes.com/se/en/search/?s=picotin#||",
        "https://www.hermes.com/be/en/search/?s=picotin#||",
        "https://www.hermes.com/cz/en/search/?s=picotin#||",
        "https://www.hermes.com/de/de/search/?s=picotin#||",  # Hoppla!
        "https://www.hermes.com/es/es/search/?s=picotin#||",  # Oops!
        "https://www.hermes.com/fi/en/search/?s=picotin#||",
        "https://www.hermes.com/fr/fr/search/?s=picotin#||",  # Oups !
        "https://www.hermes.com/it/it/search/?s=picotin#||",  # Ops!
        "https://www.hermes.com/lu/fr/search/?s=picotin#||",  # Oups !
        "https://www.hermes.com/nl/en/search/?s=picotin#||",
        "https://www.hermes.com/no/en/search/?s=picotin#||",
        "https://www.hermes.com/pl/en/search/?s=picotin#||",
        "https://www.hermes.com/at/de/search/?s=picotin#||",  # Hoppla!
        "https://www.hermes.com/pt/en/search/?s=picotin#||",
        "https://www.hermes.com/ch/fr/search/?s=picotin#||",  # Oups !
        "https://www.hermes.com/ch/de/search/?s=picotin#||"  # Hoppla!
        ]

i = 0
# CheckOnePage("https://www.hermes.com/se/en/search/?s=picotin#||")


while True:
    for url in urls:
        CheckOnePage(url)
        check_count += 1
    round_count += 1
    i += 1
    print(i)
    print("tried times: ", check_count, " in ", round_count, " rounds.")


