import re
from selenium import webdriver
import os
from urllib.request import urlretrieve
import time
import sys

user = str(input('Enter the Username : '))
url = "https://www.instagram.com/" + user
print(url)

try:
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.binary_location = "C:\\Program Files (x86)\\Google\\Chrome Beta\\Application\\chrome.exe"
    driver = webdriver.Chrome('chromedriver.exe', options=options)
    driver.get(url)
except:
    print("ChromeDriver Error");

try:
    photo_total = int(driver.find_element_by_class_name("g47SY").text.replace(".", "").replace(",", ""))
    username = driver.execute_script(
        "return document.title.split(\"(\")[0].substr(0,document.title.split(\"(\")[0].length-1)")
    tag = driver.execute_script(
        "return document.title.split(\"(\")[1].split(\")\")[0].substr(0,document.title.split(\"(\")[1].length-1)")
    print("Total number of posts : ", photo_total)
    print("Selected User : ", username)
except:
    print("Post Value Error")

imgLinks = []

try:
    last_height = driver.execute_script("return document.body.scrollHeight")
    while len(imgLinks) < photo_total:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except:
            print("Scroll Error")
        try:
            imgList = driver.find_elements_by_css_selector(".v1Nh3 a")
        except:
            print("Get Error")
        try:
            for idx, img in enumerate(imgList):
                link = img.get_property("href")
                if not link in imgLinks:
                    imgLinks.append(link)
                    print(link)
        except:
            print("Link Error")
except:
    print("Post Link Error")

pic_user_path = "C:\\Users\\jatin\\Desktop\\Stark\\Python\\" + username
try:
    os.mkdir(pic_user_path)
except:
    print("Directory for the user exists already")
captions = {}
for i in imgLinks:
    driver.get(i)

    # COMMENTS
    """
    while 1 == 1:
        print("Trying to get rid of annoying banner")
        if driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div/div/button'):
            driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div/div/button').click()
            break
    """    
    hasLoadMore = True
    while hasLoadMore:
        time.sleep(1)
        try:
            if driver.find_element_by_css_selector('#react-root > section > main > div > div > article > div.eo2As > div.KlCQn.EtaWk > ul > li.lnrre > button'):
                driver.find_element_by_css_selector('#react-root > section > main > div > div > article > div.eo2As > div.KlCQn.EtaWk > ul > li.lnrre > button').click()
        except:
            hasLoadMore = False
            print("No more comments to load")

    users_list = []
    try:
        users = driver.find_elements_by_class_name('_6lAjh')
        for user in users:
            users_list.append(user.text)
    except:
        print("Failed to load users")
    i = 0
    texts_list = []
    try:
        texts = driver.find_elements_by_class_name('C4VMK')
        for txt in texts:
            texts_list.append(txt.text.split(users_list[i])[1].replace("\r", " ").replace("\n", " "))
            i += 1
            comments_count = len(users_list)
    except:
        print("Failed to load comments")
            
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    try:
        for i in range(1, comments_count):
            user = users_list[i]
            text = texts_list[i]
            print("User ", user.translate(non_bmp_map))
            print("Text ", text.translate(non_bmp_map))
            idxs = [m.start() for m in re.finditer('@', text)]
            for idx in idxs:
                handle = text[idx:].split(" ")[0]
                print(handle)
    except:
        print("No comments Found....")

    # POSTS
    limg = []
    try:
        img_count = driver.execute_script(
            'return window._sharedData.entry_data.PostPage[0].graphql.shortcode_media.edge_sidecar_to_children.edges.length')
        print(img_count)

        for i in range(img_count):
            print("Executing Time : ", i)
            is_video = driver.execute_script(
                'return window._sharedData.entry_data.PostPage[0].graphql.shortcode_media.edge_sidecar_to_children.edges[' + str(
                    i) + '].node.is_video')
            if is_video:
                img_link = driver.execute_script(
                    'return window._sharedData.entry_data.PostPage[0].graphql.shortcode_media.edge_sidecar_to_children.edges[' + str(
                        i) + '].node.video_url')
            else:
                img_link = driver.execute_script(
                    'return window._sharedData.entry_data.PostPage[0].graphql.shortcode_media.edge_sidecar_to_children.edges[' + str(
                        i) + '].node.display_url')
            print(img_link)
            limg.append(img_link)

        for i in limg:
            print(i)
            s = i.split("/")
            name = s[-1].split("?")[0]
            path = pic_user_path + "/" + name
            if not os.path.isfile(path):
                urlretrieve(i, path)
            else:
                print("Picture Already Exists")
                # break
            print("Downloaded another image from the set")

    except:
        print("Single image in the post")
        try:
            img_link = driver.find_element_by_tag_name("video").get_attribute("src")
            is_video = True
        except:
            tag = driver.find_element_by_css_selector('meta[property="og:image"]')
            img_link = tag.get_property("content")
            is_video = False
        s = img_link.split("/")
        name = s[-1].split("?")[0]
        path = pic_user_path + "\\" + name
        if not os.path.isfile(path):
            urlretrieve(img_link, path)
        else:
            print("Picture Already Exists")
            # break
    try:
        captions[i] = driver.execute_script(
            "return window._sharedData.entry_data.PostPage[0].graphql.shortcode_media.edge_media_to_caption.edges[0].node.text")
    except:
        captions[i] = "No Caption"

print(captions)
