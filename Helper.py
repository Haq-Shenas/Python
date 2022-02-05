from email.mime.text import MIMEText
import os
import pyautogui
import pyperclip
import time
from configparser import ConfigParser
# Import smtplib for the actual sending function
import smtplib
# Here are the email package modules we'll need
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
pyautogui.FAILSAFE = False
#Read config.ini file
config_object = ConfigParser()
config_object.read(".\config\config.ini")

#Get Defaultparameter
config = config_object["CONFIGURATION"]

TransorterExe = config["CommandString"]
passwordtxt = config["password"]
retrycount = config["retry"]
DB = config["DB"]
smtpserver = config["smtpserver"]
mailfrom = config["mailfrom"]
mailto = config["mailto"]

def start_transporter_session():
    osCommandString = TransorterExe
    os.system(osCommandString)


def type_unicode(word):
    for c in word:
        if c == '~' or c=='$' or c=='!':
            pyperclip.copy(c)
            pyautogui.hotkey("ctrl", "v")
        else:
            pyautogui.typewrite(c)

def transport_btn():
    print('Transportbtn wird gesucht...')	
    transport = pyautogui.locateCenterOnScreen('.\\buttons\\transport.png')
    while transport == None:
        transport= pyautogui.locateCenterOnScreen('.\\buttons\\transport.png')
        print('Transportbtn wird gesucht...' + str(transport))	
    pyautogui.click(transport)

def selectConnection():
    print('bitte warten...')	
    time.sleep(10)
    no = noUpdate()
    time.sleep(5)
    if no==None:
        print('connectiondropdown wird gesucht...')	
        connDropDown = pyautogui.locateCenterOnScreen('.\\dropdown\\connectiondropdown_2.png')
        while connDropDown == None:
            connDropDown= pyautogui.locateCenterOnScreen('.\\dropdown\\connectiondropdown_2.png')
            print('connectiondropdown wird gesucht...' + str(connDropDown))	
            if connDropDown==None:
                noUpdate()
                time.sleep(10)
        pyautogui.click(connDropDown)
    return no
def selectDBString():
    print(DB +' wird gesucht...')	
    result = None
    connStringWeiß = None
    connStringBlau = None
    while result == None:
        connStringWeiß = pyautogui.locateCenterOnScreen('.\\auswahl\\'+DB+'_weiß.png')
        if connStringWeiß != None:
            result = connStringWeiß
        else:
            connStringBlau = pyautogui.locateCenterOnScreen('.\\auswahl\\'+DB+'_blau.png')
            if connStringBlau != None:
                result = connStringBlau
        print(DB +' wird gesucht...' + str(result))	
        # if result==None:
        #     noUpdate()
    pyautogui.click(result)
    # pyautogui.hotkey('tab')
    # pyautogui.hotkey('tab')
    # pyautogui.hotkey('tab')
    # pyautogui.hotkey('tab')

def noUpdate():
    no = pyautogui.locateCenterOnScreen('.\\auswahl\\update_popup_nein.png')
    if no != None:
        pyautogui.click(no)
    return no
        
def update():
    ja = pyautogui.locateCenterOnScreen('.\\auswahl\\update_popup_ja.png')
    print('Ja_update wird gesucht...' + str(ja))	
    if ja != None:
        pyautogui.click(ja)

def open_btn():
    pyautogui.moveTo(100, 200)
    openbtn = pyautogui.locateCenterOnScreen('.\\buttons\\open.png')
    while openbtn == None:
        openbtn = pyautogui.locateCenterOnScreen('.\\buttons\\open.png')
        print("open wird gesucht..."+ str(openbtn))
    pyautogui.click(openbtn)

def weiter_btn():
    print("weiter wird gesucht...")
    weiter=None
    while weiter == None:
        weiter = pyautogui.locateCenterOnScreen('.\\buttons\\weiter.png')
        print("weiter wird gesucht..."+ str(weiter))
    pyautogui.click(weiter)

def ok_btn():
    okbtn = pyautogui.locateCenterOnScreen('.\\buttons\\connect_ok.png')
    print('connect wird gesucht...' +str(okbtn))
    pyautogui.click(okbtn)

def passworteingabe():
    no = selectConnection()
    if no==None:
        selectDBString()
        print('passworteingabe wird gesucht...')
        kennwort = pyautogui.locateCenterOnScreen('.\\fenster\\kennwort.png')
        while kennwort == None:
            pyautogui.click(0, 0)
            #pyautogui.hotkey('tab')
            kennwort = pyautogui.locateCenterOnScreen('.\\fenster\\kennwort.png')
            print('passworteingabe wird gesucht...' + str(kennwort))
            if kennwort == None:
                noUpdate()
                time.sleep(10)
        pyautogui.click(kennwort)
        type_unicode(passwordtxt)
    return no
def setCheckBox(checkbox):
    p = pyautogui.locateOnScreen('.\\checkbox\\'+ checkbox +'.png')
    while p == None:
        p = pyautogui.locateOnScreen('.\\checkbox\\'+ checkbox +'.png')
        print("checkbox "+checkbox+" wird gesucht und gesetzt..."+ str(p))
    pyautogui.click(p.left+(p.width/2)-(p.width/2)+3,p.top+(p.height/2))
    
def absoluteFilePaths(directory):
    filelist = []
    for root, dirs, files in os.walk(os.path.abspath(directory)):
        for file in files:
            print(os.path.join(root, file))
            filelist.append(os.path.join(root, file))
    return filelist
        
def filename_input(file):
    print('Filename Input wird gesucht...')	
    result = None
    filename_server = None
    filename = None
    while result == None:
        filename_server = pyautogui.locateCenterOnScreen('.\\fenster\\filename_server.png')
        if filename_server != None:
            result = filename_server
        else:
            filename = pyautogui.locateCenterOnScreen('.\\fenster\\filename.png')
            if filename != None:
                result = filename
        print('Filename Input wird gesucht...' + str(result))	
        # if result==None:
        #     noUpdate()
    pyautogui.write(file)

def analyzeLogFiles(filelist):
    errormessages = ["Transportvorgang abgeschlossen: \n"]
    errorCouter=0
    for file in filelist:
        if ".log" in file:
            # Read Log file
            f = open(file, "r") # List of log lines
            log_lines = f.read().split('\n')
            f.close()

            for i, log in enumerate(log_lines):
                for name in ["WARN (","ERROR ("]:
                    if name in log:
                        errormessages.append(name + ' is present in line ' + str(i + 1) + 'in '+ file)
                        errormessages.append(log)
                        errorCouter = errorCouter+1
    if errorCouter > 0:
        errormessages.insert(0,"Folgende Warnings/Errors sind aufgetreten:\n\n")
    else:
        errormessages.append("YUHU Es sind keine Fehler dabei aufgetreten :-)\n")
    return errormessages

def sendGoogleMail(pngfiles):
    #The mail addresses and password
    sender_address = 'tarigh.nejat@gmail.com'
    sender_pass = 'xdbacgbxfhsrussadx'
    # Create the container (outer) email message.
    msg = MIMEMultipart()
    msg['Subject'] = 'Transporter braucht Hilfe...'
    # me == the sender's email address
    # family = the list of all recipients' email addresses
    msg['From'] = 'tarigh.nejat@gmail.com'
    to = ["tarigh.nejat@bat.at", "tarigh.nejat@live.at","khato786@hotmail.com"]
    msg['To'] = ', '.join(to)
    msg.preamble = 'Transporter braucht Hilfe...'

    # Assume we know that the image files are all in PNG format
    for file in pngfiles:
        # Open the files in binary mode.  Let the MIMEImage class automatically
        # guess the specific image type.
        with open(file, 'rb') as fp:
            img = MIMEImage(fp.read())
        msg.attach(img)
        msg.attach(MIMEText('Manuelle Eingriff ist notwendig...','plain'))

    # Send the email via our own SMTP server.
    #Create SMTP session for sending the mail
    #s = smtplib.SMTP('mxgwcl.mdcs.at',25)
    s = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    s.starttls() #enable security
    s.login(sender_address, sender_pass) #login with mail_id and password
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()
    print("Google Email wurder gesendet...")
    
def sendMail(pngfiles=[],content=None,subject='Transporter braucht Hilfe...'):
    
    # Create the container (outer) email message.
    msg = MIMEMultipart()
    msg['Subject'] = subject
    # me == the sender's email address
    # family = the list of all recipients' email addresses
    msg['From'] = mailfrom
    to = [mailto]#["tarigh.nejat@bat.at","philipp.hanschitz@bat.at"]
    msg['To'] = ', '.join(to)
    msg.preamble = subject

    # Assume we know that the image files are all in PNG format
    for file in pngfiles:
        # Open the files in binary mode.  Let the MIMEImage class automatically
        # guess the specific image type.
        with open(file, 'rb') as fp:
            img = MIMEImage(fp.read())
        msg.attach(img)
    if content!=None:    
        msg.attach(MIMEText('\n'.join([str(item) for item in content]),'plain'))
    # Send the email via our own SMTP server.
    #Create SMTP session for sending the mail
    s = smtplib.SMTP(smtpserver)
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()
    print("Info Email wurder gesendet...")

def next_step(file):
    isFertig = False
    anzahl = 1
    result=None
    mailsend = False
    while True:
        result=None
        fertig=None
        weiter=None
        verbrindungtrennen = None
        try:
            pyautogui.moveTo(100, 200)
            anzahl = anzahl+1
            fertig= pyautogui.locateCenterOnScreen('.\\buttons\\fertig.png')
            weiter= pyautogui.locateCenterOnScreen('.\\buttons\\weiter.png')
            verbrindungtrennen = pyautogui.locateCenterOnScreen('.\\fenster\\verbindung_trennen.png')
            waitForDBQueue = pyautogui.locateCenterOnScreen('.\\fenster\\warten_db_queue.png')
            #Hilfe holen
            if verbrindungtrennen != None:
                print('Verbindungstrennung notwendig, Info-Email wird an den Entwickler verschickt...')	
                screenshotFileName = file.replace('.zip','_Hilfe.png')
                pyautogui.screenshot(screenshotFileName)
                try:
                    if not mailsend:
                        sendMail([screenshotFileName])
                        mailsend = True
                except:
                    print("ERROR: sendMail fehlgeschlagen...")
                    break
            if waitForDBQueue != None:
                print("Warten auf DB Queue wird überprungen (STRG,f)...")
                pyautogui.click(waitForDBQueue)
                pyautogui.hotkey('ctrl','f')

            if fertig != None:
                result=fertig
                print(file + " wurde erfolgreich importiert!")
                pyautogui.screenshot(file.replace('zip','png'))
                isFertig = True
                mailsend = False
                break
            if weiter != None:
                result=weiter
                pyautogui.screenshot(file.replace('.zip',time.strftime("%Y%m%d-%H%M%S")+'.png'))
                mailsend = False
                break
            if anzahl<=int(retrycount):
                print("Weiter/Fertig Button wird gesucht...: "+ str(anzahl))
                time.sleep(5)

            else:
                #um hilfe bitten => mail senden
                screenshotFileName = file.replace('.zip','_Hilfe.png')
                pyautogui.screenshot(screenshotFileName)
                try:
                    sendMail([screenshotFileName],'Bitte überprüfen ob manuelle Eingriff notwendig ist...')
                    break
                except:
                    print("ERROR: sendMail fehlgeschlagen...")
                    break
        except OSError:
            print("OSError...")
            sendMail([],'SESSION Disconnected')
            time.sleep(300)
    pyautogui.click(result)
    return isFertig
        


