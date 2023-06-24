from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from colorama import init, AnsiToWin32
from colorama import Fore, Style
import datetime
from bs4 import BeautifulSoup
import os
from time import sleep
import sys
followerss, likess = 0, 0
banner = '''                                              
TTTTTTTTTTTTTTTTTTTTTTTUUUUUUUU     UUUUUUUU       CCCCCCCCCCCCC
T:::::::::::::::::::::TU::::::U     U::::::U    CCC::::::::::::C
T:::::::::::::::::::::TU::::::U     U::::::U  CC:::::::::::::::C
T:::::TT:::::::TT:::::TUU:::::U     U:::::UU C:::::CCCCCCCC::::C
TTTTTT  T:::::T  TTTTTT U:::::U     U:::::U C:::::C       CCCCCC
        T:::::T         U:::::D     D:::::UC:::::C              
        T:::::T         U:::::D     D:::::UC:::::C              
        T:::::T         U:::::D     D:::::UC:::::C              
        T:::::T         U:::::D     D:::::UC:::::C              
        T:::::T         U:::::D     D:::::UC:::::C              
        T:::::T         U:::::D     D:::::UC:::::C              
        T:::::T         U::::::U   U::::::U C:::::C       CCCCCC
      TT:::::::TT       U:::::::UUU:::::::U  C:::::CCCCCCCC::::C
      T:::::::::T        UU:::::::::::::UU    CC:::::::::::::::C
      T:::::::::T          UU:::::::::UU        CCC::::::::::::C
      TTTTTTTTTTT            UUUUUUUUU             CCCCCCCCCCCCC
      
                                        Tiktok Username Checker by Quang Nhan v2.0
'''
os.system('cls')
os.system('Tiktok Username Checker by Quang Nhan v2.0')
n_live = 0
n_die = 0
init(wrap=False)
stream = AnsiToWin32(sys.stderr).stream
f = open('tiktokid.txt', 'r')
f2 = open('live.txt', 'w')
f3 = open('die.txt', 'w')
print(Fore.MAGENTA + banner, file=stream)
print(Fore.WHITE, 'Check live username Tiktok. Input list of usernames in file tiktokid.txt in the same directory.', file = stream)
print(Fore.WHITE, 'Live accounts will be written to live.txt and the banned accounts will be written to die.txt.', file = stream)
print('\n\n')
while True:
    try:
        s = input('Username filter [followers likes] (leave it blank to check live): ')
        if s == '':
            followerss, likess = 0, 0
            break
        followerss, likess = map(int, s.split())
        break
    except:
        continue
data2 = f.readlines()
data = []
data = [i for i in data2 if i not in data]
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument('log-level=3')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-logging')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-default-apps')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--log-level=3')
driver = webdriver.Chrome(options=chrome_options)
def get_username_information(html_source):
    soup = BeautifulSoup(html_source, 'html.parser')
    likes_counts = 0
    followers_counts = 0
    for tag in soup.find_all(attrs={"data-e2e": "likes-count"}):
        likes_counts = tag.text
    for tag in soup.find_all(attrs={"data-e2e": "followers-count"}):
        followers_counts = tag.text
    if followers_counts[len(followers_counts)-1]=='K':
        followers_counts = int(followers_counts.replace('K', ''))*1000
    elif followers_counts[len(followers_counts)-1]=='M':
        followers_counts = int(followers_counts.replace('M', ''))*1000000
    if likes_counts[len(likes_counts)-1]=='K':
        likes_counts = int(likes_counts.replace('K', ''))*1000
    elif likes_counts[len(likes_counts)-1]=='M':
        likes_counts = int(likes_counts.replace('M', ''))*1000000
    return [int(followers_counts), int(likes_counts)]
driver.get('https://www.tiktok.com/@tiktok')
sleep(5)
input('\x1b[32mSolve the captcha and press enter.....\x1b[0m')
count = 0
for i in data:
    i = str(i).replace('\n', '')
    url = 'https://tiktok.com/@'+i
    driver.get(url)
    WebDriverWait(driver, timeout = 0.2)
    sleep(1)
    try:
        while driver.find_element(By.CLASS_NAME, 'captcha-disable-scroll'):
            now = datetime.datetime.now()
            print(Fore.RED + '[',now.strftime("%Y-%m-%d %H:%M:%S"),'] Captcha protection !! Solve it and press enter to continue', file=stream, end='')
    except:
        pass
    try:
        e = driver.find_element(By.XPATH, '//*[@id="main-content-others_homepage"]/div/div[1]/div[1]/div[2]/div/div[1]/button')
        f2.write(i)
        n_live += 1
        html_source = driver.page_source
        data = get_username_information(html_source)
        if data[0] < followerss or data[1] < likess:
            continue
        now = datetime.datetime.now()
        print(Fore.BLUE + '[',now.strftime("%Y-%m-%d %H:%M:%S"),'] ', file=stream, end = '')
        print(Fore.GREEN + '[LIVE] -> ', file=stream, end = '')
        print(f'\x1b[33m{i}  \x1b[0m(\x1b[32m {data[0]} \x1b[0mFollowers -- \x1b[32m{data[1]}\x1b[0m Likes)  [\x1b[36m{((driver.title).split("(")[0]).replace(" ", "")}\x1b[0m]')
    except:
        f3.write(i)
        n_die += 1
        now = datetime.datetime.now()
        print(f'\x1b[33m{count}\x1b[0m', end='')
        print(Fore.BLUE + '[',now.strftime("%Y-%m-%d %H:%M:%S"),'] ', file=stream, end = '')
        s1 = '[DIE]  -> '+ i
        print(Fore.RED + s1, file = stream)
    count += 1
now = datetime.datetime.now()
print(Fore.GREEN + '███████████████████████████████████████████████████████████████████████████████████████████████████████████████')
print()
print(Fore.YELLOW + '[', now.strftime("%Y-%m-%d %H:%M:%S"), '] Scan successfully ' +  str(n_live+n_die) +  ' account(s).', file=stream)
print(Fore.GREEN + '[', now.strftime("%Y-%m-%d %H:%M:%S"), '] ' + str(n_live) + ' alive account(s). --> ' + str(round(n_live/count, 2)*100) + '%',file=stream)
print(Fore.RED + '[', now.strftime("%Y-%m-%d %H:%M:%S"), '] ' + str(n_die) + ' died account(s). --> ' + str(round(n_die/count, 2)*100) + '%',file=stream)
print()
print(Fore.GREEN + '███████████████████████████████████████████████████████████████████████████████████████████████████████████████')
f.close()
f2.close()
f3.close()
driver.quit()
print(Style.RESET_ALL)