import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from threading import Timer
from secrets import *


class bot():
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("use-fake-ui-for-media-stream")
        self.driver = webdriver.Chrome(options=chrome_options)
    
    def checkteam(self,teamname):
        searchteam = self.driver.find_element_by_xpath('//*[@id="left-rail-header-filter-input"]').send_keys(teamname)
        teamxpath = "team-"+teamname+"-h3"
        sleep(2)
        clickteam = self.driver.find_element_by_xpath('//*[@data-tid="'+teamxpath+'"]')
        print("TEAM FOUND, SELECTING CHANNEL...")
        while True:
            try:
                clickteam.click()
                sleep(2)
                generalchannel = self.driver.find_element_by_xpath('//*[@class="truncate highlighted-channel"]').click()
                sleep(2)
                ignorenotif = self.driver.find_element_by_xpath('//*[@id="toast-container"]/div/div/div[2]/div/button[2]').click()
                print("GENERAL CHANNEL SELECTED")
                break
            except:
                print("GENERAL CHANNEL NOT SELECTED YET")


    def checkmessages(self):
        chatpannel = self.driver.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/calling-screen/div/div[2]/meeting-panel-components')
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
            sendmsg = self.driver.find_element_by_xpath('//*[@id="send-message-button"]').click()
        except:
            print("/!\  ERROR : problem sending present message   /!\ ")
        
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
        sleep(2)
        print("Waiting for others to type present at least 3 times...")
        presentmsgs = ["Present","Presente","Présent","Présente"]
        nbrpresent = 0
        maxnbrpresent = 0
        breaking = False

        while True:
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
                            print(message["Sender"]+ "just said Present, I'm marking you present too right now...")
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
    
    def endcall(self):
        endcallbtn = self.driver.find_element_by_xpath('//*[@data-tid="call-hangup"]').click()
        print("I just got off the meeting, the call lasted more than 1h50min ")
        self.driver.quit()
        exit()
        
    
    def watchparticipants(self):
        self.showparticipants()
        sleep(2)
        t = Timer(6600.0, self.endcall) 
        t.start()
        while True:
            nbrparticipants = self.checkparticipants()
            if nbrparticipants < 5:
                endcallbtn = self.driver.find_element_by_xpath('//*[@data-tid="call-hangup"]').click()
                sleep(10)
                print("I just got off the meeting, number of participants left : "+str(nbrparticipants))
                self.driver.quit() 
                exit()
    
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
                sleep(5)
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
                joinbtn2 = self.driver.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[1]/div/div/button').click()
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
        loginbtn1 = self.driver.find_element_by_xpath('//*[@id="i0281"]/div/div/div[1]/div[2]/div[2]/div/div/div/div[4]/div/div/div/div').click()
        sleep(2)
        
        loginpass = self.driver.find_element_by_xpath('//*[@id="i0118"]')
        loginpass.send_keys(pwd)
        sleep(2)
        loginbtn = self.driver.find_element_by_xpath('//*[@id="i0281"]/div/div/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[2]/div/div/div/div').click()
        sleep(2)
        try:
            staybtn = self.driver.find_element_by_xpath('/html/body/div/form/div[1]/div/div[1]/div[2]/div/div[2]/div/div[3]/div[2]/div/div/div[2]').click()
        except:
            sleep(2)
        
teamname=selectteam()        
b = bot()
b.login(user,pwd)
b.loadteam()
b.checkteam(teamname)
b.waitformeeting()
b.joinmeeting()
b.watchmessages(closestud)
b.watchparticipants()
