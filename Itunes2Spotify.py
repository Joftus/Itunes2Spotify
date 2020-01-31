'''
Step to Itunes2Spoitify
0. traverse to folder
1. get the name of the music file
2. parse the name based on derived formula
    - ignore song files with tags (remix) and (acoustic)
    - remove all parenthese
3. take song name and plug it into spotify
4. pick top *song* and then add it to a spotify folder ()
    - check if the song is already liked
'''

import time

from os import listdir
from os.path import isfile, join

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


username = ""
password = ""

log = True
progress_bar = not log
start_time = time.time()
wait_time = 3
short_wait_time = 1
songs = []

mypath = "./Itunes/"
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for file in files:
    output = str(file).partition("(")[0]
    output = output.partition(".mp3")[0]
    songs.append(output)

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://open.spotify.com/")
driver.find_element_by_xpath('//*[@id="main"]/div/div[4]/div[3]/div[1]/div/div/header/div/div[4]/button[2]').click()
time.sleep(wait_time)
driver.find_element_by_id("login-username").send_keys(username)
driver.find_element_by_xpath('//*[@id="login-password"]').send_keys(password)
driver.find_element_by_xpath('//*[@id="login-button"]').click()
time.sleep(wait_time)
driver.find_element_by_xpath('//*[@id="main"]/div/div[4]/div[1]/nav/ul/li[2]/div/a').click()

if log:
    print("\n\n\n")
total = len(songs)
marker = total // 20
failed = []

count = 0
songs = songs[count:]
print("Songs: " + str(total - count))

for song in songs:
    if progress_bar and count % marker == 0:
        print("#", end="", flush=False)
    try:
        time.sleep(wait_time)
        search = driver.find_element_by_xpath('//*[@id="main"]/div/div[4]/div[3]/div[1]/div/div/header/div/div[3]/div/label/input')
        search.clear()
        search.send_keys(song)
        time.sleep(short_wait_time)
    except Exception as e:
        print("Ending Index: " + str(count))
    try:
        driver.find_element_by_xpath('//*[@id="searchPage"]/div/div/section[2]/div/div[1]').click()
        driver.find_element_by_xpath('//*[@id="searchPage"]/div/div/section[2]/div/div[1]/div/div/div[4]/button').click()
        time.sleep(short_wait_time)
        liked = driver.find_element_by_xpath('//*[@id="main"]/div/nav[1]/div[2]')
        if liked.text == "Save to your Liked Songs":
            liked.click()
            if log:
                print("    " + str(count) + ". " + song + " added to likes songs")
    except Exception as e:
        if log:
            print(song + " not found on spotify...")
            failed.append(song)
            driver.get("https://open.spotify.com/search")
    count += 1


print("", flush=True)
print("Itunes2Spotify completed in: " + str(time.time() - start_time))
print("------- Failures -------")
index = 1
for fail in failed:
    print(str(index) + ". " + fail)
    index += 1
