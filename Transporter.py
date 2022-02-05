from distutils.command.config import config
from distutils.log import error
import threading
from Helper import sendMail,weiter_btn, sendMail,analyzeLogFiles, setCheckBox,next_step, filename_input, passworteingabe,start_transporter_session,transport_btn,absoluteFilePaths,open_btn
from configparser import ConfigParser
import pyautogui

pyautogui.FAILSAFE = False
#Read config.ini file
config_object = ConfigParser()
config_object.read(".\config\config.ini")

#Get Defaultparameter
config = config_object["CONFIGURATION"]
Transportfoler = config["Transportfoler"]
DB = config["DB"]
logging = config["logging"]
no = None
input("Haben Sie die Configurationsparam gesichert und ins Transportverzeichis als vorletztes Paket zum einspielen definiert?")
list = absoluteFilePaths(Transportfoler)
for file in list:
    if ".zip" in file:
        rdc = threading.Thread(target=start_transporter_session)
        rdc.start()
        transport_btn()
        weiter_btn()
        no = passworteingabe()
        if no==None:
            next_step(file)
            #prüfen ob file bereits importiert ist
            filename_input(file)
            open_btn()
            setCheckBox('objekte_einzeln')
            if bool(logging):
                setCheckBox('protokoll')
            while True:
                isfertig = next_step(file)
                if rdc.is_alive() == False or isfertig:
                    break
                else:
                    print("Transportvorgang läuft...")
        else:   
            print('Aktualisierung notwendig!, bitte den Transportvorgang beenden (STRG+C, oder Fenster Schließen) und nach der Aktualisierung erneut starten')	
            break
    else:
        continue
if no==None:
    logList = absoluteFilePaths(Transportfoler)
    errormessages = analyzeLogFiles(logList)
    sendMail([],errormessages,'Transport in DB='+DB+' abgeschlossen')
else:
    print('Aktualisierung notwendig!')	