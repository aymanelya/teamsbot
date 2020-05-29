from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from playsound import playsound
from time import sleep
from threading import Timer
from secrets import *
import re
import os
import sys
import requests
import platform 

def clearscreen():
    plt = platform.system()
    if plt == "Windows":
        os.system("cls")
    else:
        os.system("clear")   

class bot():
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("use-fake-ui-for-media-stream")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.minimize_window()
    
    def checkteam(self,teamname):
        #searchteam
        self.driver.find_element_by_xpath('//*[@id="left-rail-header-filter-input"]').send_keys(teamname)
        teamxpath = "team-"+teamname+"-h3"
        sleep(2)
        clickteam = self.driver.find_element_by_xpath('//*[@data-tid="'+teamxpath+'"]')
        print("TEAM FOUND, SELECTING CHANNEL...")
        while True:
            try:
                clickteam.click()
                sleep(2)
                #generalchannel
                self.driver.find_element_by_xpath('//*[@class="truncate highlighted-channel"]').click()
                sleep(2)
                #ignorenotif
                self.driver.find_element_by_xpath('//*[@id="toast-container"]/div/div/div[2]/div/button[2]').click()
                print("GENERAL CHANNEL SELECTED")
                break
            except:
                print("GENERAL CHANNEL NOT SELECTED YET")


    def checkmessages(self):
        #chatpannel
        self.driver.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/calling-screen/div/div[2]/meeting-panel-components')
        senders = []
        messages = []
        times = []
        msgsender = self.driver.find_elements_by_xpath('//*[@data-tid="threadBodyDisplayName"]') #returns list of elements of names that sent messages
        for i in msgsender:
            senders.append(i.get_attribute('innerHTML').strip())
            
            
        msgcontent = self.driver.find_elements_by_xpath('//*[@data-tid="messageBodyContent"]')#returns list of elements of messages content
        for i in msgcontent:
            res= re.findall(r'<div>(.*?)</div>',str(i.get_attribute('innerHTML').strip()))[0]
            messages.append(res)
            
        msgtime = self.driver.find_elements_by_xpath('//*[@data-tid="messageTimeStamp"]')
        for i in msgtime:
            times.append(i.get_attribute('innerHTML').strip())
            
        alldata = []
        for i in list(range(len(senders))):
            alldata.append({"Sender":senders[i],"Message":messages[i],"Time":times[i]})
        return alldata
    
    def markpresent(self):
        try:
            inputmsg = self.driver.find_element_by_xpath('//*[@data-tid="ckeditor-replyConversation"]')
            inputmsg.send_keys("Présent")
            #sendmsg
            self.driver.find_element_by_xpath('//*[@id="send-message-button"]').click()
        except:
            print("!  ERROR : problem sending present message   ! ")
        
    def checkparticipants(self):
        self.showparticipants()
        sleep(2)
        nbr = 0
        inmeeting = self.driver.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/calling-screen/div/div[2]/meeting-panel-components/calling-roster/div/div[3]/div/div[1]/accordion/div/accordion-section[2]/div/calling-roster-section/div/div[1]/button')
        if "Currently in this meeting" in inmeeting.get_attribute('aria-label'):
            nbr = nbr + int(inmeeting.get_attribute('aria-label').split("Currently in this meeting ")[1])
            return nbr
        else:
            nbr = nbr + int(inmeeting.get_attribute('aria-label').split("Attendees ")[1])
            presenters = self.driver.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/calling-screen/div/div[2]/meeting-panel-components/calling-roster/div/div[3]/div/div[1]/accordion/div/accordion-section[1]/div/calling-roster-section/div/div[1]/button')
            nbr = nbr + int(presenters.get_attribute('aria-label').split("Presenters ")[1])
            return nbr
    def showparticipants(self):
        while True:
            try:
                participantsbtn = self.driver.find_element_by_xpath('//*[@id="roster-button"]')
                participantsbtn.click()
            except:
                actions = ActionChains(self.driver) 
                actions.send_keys(Keys.TAB)
                actions.perform()
            else:
                break

    def showchat(self):
        while True:
            try:
                chatbtn = self.driver.find_element_by_xpath('//*[@id="chat-button"]')
                chatbtn.click()
            except:
                actions = ActionChains(self.driver) 
                actions.send_keys(Keys.TAB)
                actions.perform()
            else:
                break

    def watchmessages(self,closestud):
        sleep(900)
        print("Waiting for others to type present at least 3 times...")
        presentmsgs = ["Present","Presente","Présent","Présente"]
        nbrpresent = 0
        maxnbrpresent = 0
        breaking = False
        while True:
            if (self.watchparticipants()):
                break
            messagelist = self.checkmessages()
            for message in messagelist:
                if not message["Message"].islower():
                    message["Message"]=message["Message"].lower().title()
                else:
                    message["Message"]=message["Message"].title()
                if message["Message"] in presentmsgs:
                    nbrpresent+=1
                    if nbrpresent > 3:
                        if message["Sender"] in closestud:
                            print(message["Sender"]+ " just said Present, I'm marking you present too right now...")
                            self.markpresent()
                            breaking= True
                            break
            if nbrpresent > maxnbrpresent:
                maxnbrpresent = nbrpresent
                print("Number of student typed 'present' : "+str(maxnbrpresent))
            nbrpresent = 0
            if breaking == True:
                print("Marked Present Successfully, I will get off the call once there's less than 5 participants in the meeting...")
                break
            
    
    def watchparticipants(self):
        self.showparticipants()
        sleep(2)
        nbrparticipants = self.checkparticipants()
        if nbrparticipants < 6:
            #endcallbtn
            self.driver.find_element_by_xpath('//*[@data-tid="call-hangup"]').click()
            sleep(6)
            self.driver.quit()
            print("I just got off the meeting, number of participants left : "+str(nbrparticipants))
            return True
        return False
                

    
    def loadteam(self):
        #wait for msteams and default team to load
        while True:
            try:
                filterbtn = self.driver.find_element_by_xpath('//*[@id="left-rail-header"]/div[2]/button')
                print("DONE LOADING, SELECTING TEAM NOW...")
                filterbtn.click()
                sleep(3)
                break
            except:
                print("TEAM STILL LOADING...")
                sleep(5)
                
                
    
    def waitformeeting(self):
        while True:
            try:
                joinbtn = self.driver.find_element_by_xpath('//*[@title="Join call with video"]')
                joinbtn.click()
                print("Meeting is available, joining now...")
                sleep(2)
                break
            except:
                sleep(60)
                print("Waiting for meeting to start...")
                
                
    def joinmeeting(self):
        while True:
            try:
                mic = self.driver.find_element_by_xpath('//*[@id="preJoinAudioButton"]/div/button/span[1]')
                if 'Mute microphone' in mic.get_attribute('outerHTML'):
                    mic.click()
                    print("I muted your microphone")
   
                cam = self.driver.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[2]/toggle-button[1]/div/button/span[1]')
                if 'Turn camera off' in cam.get_attribute('outerHTML'):
                    cam.click()
                    print("I turned off your Camera")

                sleep(2)
                #joinbtn2
                self.driver.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[1]/div/div/button').click()
                break
            except:
                print('Team Still Loading...')
                sleep(2)
        part = self.checkparticipants()
        print("Joined meeting,number of participants: "+str(part))
        self.showchat()
        sleep(2)          

    def login(self,user,pwd):
        self.driver.maximize_window()
        self.driver.get('https://teams.microsoft.com/')
        sleep(2)


        loginuser = self.driver.find_element_by_xpath('//*[@id="i0116"]')
        loginuser.send_keys(user)
        sleep(2)
        #loginbtn1
        self.driver.find_element_by_xpath('//*[@id="i0281"]/div/div/div[1]/div[2]/div[2]/div/div/div/div[4]/div/div/div/div').click()
        sleep(2)
        
        loginpass = self.driver.find_element_by_xpath('//*[@id="i0118"]')
        loginpass.send_keys(pwd)
        sleep(2)
        #loginbtn
        self.driver.find_element_by_xpath('//*[@id="i0281"]/div/div/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[2]/div/div/div/div').click()
        sleep(2)
        try:
            #staybtn
            self.driver.find_element_by_xpath('/html/body/div/form/div[1]/div/div[1]/div[2]/div/div[2]/div/div[3]/div[2]/div/div/div[2]').click()
        except:
            sleep(2)
 

def errorAlert():
    clearscreen()
    print("ERROR, PLEASE CHECK YOUR INTERNET AND RESTART THE SCRIPT")
    print("you can stop it using ctrl+c")
    while True:
        playsound("alarm.mp3")

def checkdate():
    URL = "http://worldtimeapi.org/api/timezone/Africa/Casablanca"
    weekdays = ["Sunday","Monday","Tuesday","Wednesday","Thursday", "Friday", "Saturday"]
    r = requests.get(url = URL) 
    data = r.json()
    day = weekdays[data["day_of_week"]]
    data = data["datetime"].split("T")
    data[1] = data[1].split(":")
    time = data[1][0]+":"+data[1][1]
    return [day,time]

def checktime():
    now = checkdate()
    today = now[0]
    timenow = now[1].split(":")
    nowminutes = int(timenow[0])*60 + int(timenow[1])
    team = ""
    todaytimes = []
    for i in calendar[today]:
        temp = i.split(":")
        todaytimes.append(int(temp[0])*60 + int(temp[1]))
    for i in range(len(todaytimes)):
        if(nowminutes < todaytimes[0]):
            print("Too early for your first class")
            break
        elif(nowminutes > todaytimes[len(todaytimes)-1]+120):
            print("No more classes for today")
            break
        elif(nowminutes > todaytimes[len(todaytimes)-1]):
            minutetokey = '{:02d}:{:02d}'.format(*divmod(todaytimes[len(todaytimes)-1], 60))
            team = calendar[today][minutetokey]
            print("You're a little late to your last class: "+team)
            break
        elif(nowminutes > todaytimes[i] and nowminutes < todaytimes[i+1]):
            minutetokey = '{:02d}:{:02d}'.format(*divmod(todaytimes[i], 60))
            team = calendar[today][minutetokey]
            print("You're a little late to your class: "+team)
            break
        else:
            minutetokey = '{:02d}:{:02d}'.format(*divmod(todaytimes[i], 60))
            team = calendar[today][minutetokey]
            print("Class right now: "+team)
            break
    sleep(3)
    return team


def autorun():
    while True:
        team = checktime()
        if(team == ""):
            print("Checking again in 10 minutes")
            sleep(600)
            clearscreen()
        else:
            main(team)


def main(teamname):
    try:
        clearscreen()
        print("Running the script for team '"+teamname+"'")
        b = bot()
        b.login(user,pwd)
        b.loadteam()
        b.checkteam(teamname)
        b.waitformeeting()
        b.joinmeeting()
        b.watchmessages(closestud)
        b.watchparticipants()
    except:
        errorAlert()


autorun()