from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
import os
import sys
chrome_driver = os.path.join('chromedriver')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')               # headless
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')

dict={}

def page(index,info):
    url ="https://www.thingiverse.com/thing:"+str(index)
    driver = webdriver.Chrome(chrome_driver, options=chrome_options)

    driver.get(url)
    print(url)
    time.sleep(5)
    
    taglists=[]
    tags=driver.find_element(By.CSS_SELECTOR,".Contents__widgetBody--3w2JG").find_elements(By.TAG_NAME,"a")
    for tag in tags:
        taglists.append(tag.text)
    info.append(taglists)
    
    
    return comment(index,info)
        
    
def comment(index,info):
    url ="https://www.thingiverse.com/thing:"+str(index)+"/comments"
    driver = webdriver.Chrome(chrome_driver, options=chrome_options)
    driver.get(url)
    print(url)
    time.sleep(5)

    values=driver.find_elements(By.CSS_SELECTOR,".MetricButton__metric--FqxBi")
    comments = int(values[2].text)
    makes = int(values[3].text)
    remixes = int(values[4].text)
    apps = int(values[5].text)
    date= ' '.join(driver.find_element(By.CSS_SELECTOR,".ThingTitle__createdBy--1fCKx").text.split(" ")[2:]) 
    info.append(comments)
    
    try:
        mores= driver.find_elements(By.CSS_SELECTOR, '.Button__md--cjz0D')
        for i in mores:
            if i.text=="View More Comments":
                i.click()
                time.sleep(5)
    except:
        pass
        
    cmts=driver.find_elements(By.CSS_SELECTOR,".ThingCommentsList__commentContainer--EjmOU")
    commentList=[]
    for c in cmts:
        inp=[]
        tempcmt=""
        for t in c.find_elements(By.TAG_NAME,"p"):
            tempcmt+=t.text
        
        inp.append(tempcmt)
        try:
            replie =  c.find_elements(By.CSS_SELECTOR,".LinkButton__linkButton--U_cBr")
            for w in replie:
                if w.text=="View Replies":
                    #print("View Replies")
                    w.click()
                    time.sleep(5)
                    cocmts = c.find_elements(By.CSS_SELECTOR,".ThingCommentsList__commentContainer--EjmOU")
                    for coco in cocmts:
                        tempcocmt=""
                        for t in coco.find_elements(By.TAG_NAME,"p"):
                            tempcocmt+=t.text
                        inp.append(tempcocmt)
        except:
            print("no replie")
        commentList.append(inp)
    info.append(commentList)
    
    info.append(makes)
    info.append(remixes)
    info.append(apps)
    info.append(date)
    #print(inp)
    return info
    
    
        
def getlists(x,writer):
    

    idx=1
    while True:
        
        try:
            print(idx)
            url = "https://www.thingiverse.com/search?page=" + str(idx) + "&per_page=20&sort=popular&type=things&q=&category_id="+str(x) 
            
            driver = webdriver.Chrome(chrome_driver, options=chrome_options)
            driver.get(url)
            print(url)
            time.sleep(5)
            
            elements = driver.find_elements(By.CSS_SELECTOR,".SearchResult__searchResultItem--14-Vi")
            for element in elements:
                image=element.find_element(By.CSS_SELECTOR,".ThingCardBody__cardBodyWrapper--ba5pu").find_element(By.TAG_NAME,"img").get_dom_attribute("src")
                src=element.find_element(By.CSS_SELECTOR,".ThingCardBody__cardBodyWrapper--ba5pu").get_dom_attribute("href")
                printModelId =src.split(":")[2]
                
                if printModelId in dict:
                    print("crashed!")
                    #return
                else:
                    dict[printModelId]=True
                like=int(element.find_element(By.CSS_SELECTOR,".ThingCardActions__rightActionsContainer--O1YxM").find_element(By.CSS_SELECTOR,".CardActionItem__text--2Zg-W").text)
                title = element.find_element(By.CSS_SELECTOR,".ThingCardHeader__cardNameWrapper--3xgAZ").text
                name = element.find_element(By.CSS_SELECTOR,".ThingCardHeader__avatarWrapper--1Jliv").get_dom_attribute("href").split(".com/")[1]
                info=[]
                
                info.append(title)
                info.append(name)
                info.append(like)

                try:
                        info=page(printModelId,info)

                        info.append(src)
                        info.append(printModelId)
                        info.append(image)
                        print("build success")
                        
                except Exception as e:
                        ck=True
                        print("build faild",e)
                try:
                        #print(info)
                        writer.writerow(info)
                        print("write success")
                except Exception as e:
                        print("write faild",e)
                        ck=True
        except e:
            print(e)
        
        idx+=1
        if idx>500:
            break
            
            

f = open("Scans & Replicas.csv", "w")
writer=csv.writer(f)
column=["title","name","likes","tags","commentsCount","comments","makes","remixes","apps","date","url","id","img"]
writer.writerow(column)
            
getlists(145,writer)
