import re
from selenium import webdriver
import os
from urllib.request import urlretrieve
import time
import sys
import json

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)


def login_insta():
    driver.find_element_by_name("username").send_keys(uname)
    driver.find_element_by_name("password").send_keys(pwd)
    driver.find_element_by_css_selector("button[type='submit']").click()

def login_fb():
    driver.find_element_by_class_name("KPnG0").click()
    driver.find_element_by_name("email").send_keys(uname)
    driver.find_element_by_name("pass").send_keys(pwd)
    driver.find_element_by_css_selector("button[type='submit']").click()


user = str(input('Enter the Username : '))
url = "https://www.instagram.com/accounts/login"
print(url)

try:
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.binary_location = "C:\\Program Files (x86)\\Google\\Chrome Beta\\Application\\chrome.exe"
    driver = webdriver.Chrome('chromedriver.exe', options=options)
    driver.get(url)
except:
    print("ChromeDriver Error");


login_insta()

curr_url=url
while(curr_url != "https://www.instagram.com/"):
    print("Still Loading")
    curr_url=driver.execute_script("return document.URL")
driver.find_element_by_xpath("/html/body/div[3]/div/div/div[3]/button[2]").click()


url = "https://www.instagram.com/" + user
driver.get(url)



def followers_list():
    follows=driver.find_element_by_class_name("_5f5mN")
    if(follows.text=="Follow"):
        print("You do not follow this user")
        ch=str(input("Should i follow this account ? (Y/N) : "))
        if(ch=='y' or ch=='Y'):
            follows.click()
    x=driver.find_element_by_xpath("//*[@id=\"react-root\"]/section/main/div/header/section/ul/li[2]/a/span")
    x.click()
    foll_list=driver.find_elements_by_class_name("wo9IH")
    for i in foll_list:
        print(i.text.split()[0])


try:
    photo_total = int(driver.find_element_by_class_name("g47SY").text.replace(".", "").replace(",", ""))
    username = driver.execute_script(
        "return document.title.split(\"(\")[0].substr(0,document.title.split(\"(\")[0].length-1)")
    taghandle = driver.execute_script(
        "return document.title.split(\"(\")[1].split(\")\")[0]")
    followers=driver.find_element_by_xpath("//*[@id=\"react-root\"]/section/main/div/header/section/ul/li[2]/a/span").get_attribute("title")
    print("Number of Followers : ",followers)
    print("Total number of posts : ", photo_total)
    print("Selected User : ", username)
    print("Insta Handle : ",taghandle)
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
posts={}
posts["User"]=username.translate(non_bmp_map)
posts["Handle"]="@"+user
for i in imgLinks:
    post={}
    try:
        driver.get(i)
    except:
        print("Cant Load Post")
        
    # COMMENTS
    hasLoadMore = True
    while hasLoadMore:
        time.sleep(1)
        try:
            if driver.find_element_by_css_selector(
                    '#react-root > section > main > div > div > article > div.eo2As > div.KlCQn.EtaWk > ul > li.lnrre > button'):
                driver.find_element_by_css_selector(
                    '#react-root > section > main > div > div > article > div.eo2As > div.KlCQn.EtaWk > ul > li.lnrre > button').click()
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

    
    try:
        for i in range(1, comments_count):
            user = users_list[i].translate(non_bmp_map)
            text = texts_list[i].translate(non_bmp_map)
            print("User ", user)
            print("Text ", text)
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
            "return window._sharedData.entry_data.PostPage[0].graphql.shortcode_media.edge_media_to_caption.edges[0].node.text").translate(non_bmp_map)
    except:
        captions[i] = "No Caption"
    try:
        try:
            post["Link"]=i.translate(non_bmp_map)
        except:
            print("LINK IN JSON ERROR")
        try:
            post["Image Name"]=path.translate(non_bmp_map)
        except:
            print("IMAGE NAME IN JSON ERROR")
        try:
            post["Caption"]=captions[i].translate(non_bmp_map)
        except:
            print("CAPTION IN JSON ERROR")
        try:
            if(users_list and texts_list):
                post["Comments"]=list(zip(users_list,texts_list))
                posts[name]=post
            else:
                post["Comments"]=[]
        except:
            print("COMMENTS IN JSON ERROR")
    except:
        print("Creating Dictionary Error")
        
filename=username+".json"

with open(filename, "w") as write_file:
    json.dump(posts, write_file,indent=4)
