import urllib.request, urllib.error, urllib.parse
import http.client as httplib
import smtplib, ssl
import filecmp
import os
import shutil
import time
from datetime import datetime, date

messageToSend = """\
Subject: Notification from the \"Notifier Bot\" 

Hello there :)
Just wanted to tell you that one or more new announcements were upload on : http://www.ice.uniwa.gr/announcements-all/.

Have a nice day or night.
"""

url = "http://www.ice.uniwa.gr/announcements-all/"                                      # URL of the site we want to be updated
oldPagePath = "C:/Users/.../oldPage/"
newPagePath = "C:/.../"
port = 465                                                                              # Port for TLS, if port is zero, or not specified, .SMTP_SSL() will use the standard port for SMTP over SSL (port 465)
senderMail = "yourMail"
password = "yourPassword"                                                               # Password of "senderMail"
receiverMail = "..."
announcements_div_class = "col-lg-12 col-md-12 col-sm-12 col-xs-12 single_post_row"     # Thats the name of the div class where announcements are "stored"

def checkInternet() :
    conn = httplib.HTTPConnection("www.google.com", timeout = 5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False

def notifierBot() :
    linesOf_div_block = 0                                                               # We know from the html file we downloaded that every announcements div class is 10 lines
    find_div = False

    response = urllib.request.urlopen(url)                                              # We request and read 
    webContent = response.read()                                                        # the html page

    f = open(newPagePath + "page.html", "wb")                                           # We save the html page 
    f.write(webContent)                                                                 # on a file and after that
    f.close()                                                                           # we close the file
    
    fileWith_divs = open(newPagePath + "fileWith_divs.txt", "w", encoding = "UTF-8")    # Open the file with "UTF-8" to make sure that we don't get errors from read the file
    with open(newPagePath + "page.html", "r", encoding = "UTF-8") as page :
        for line in page :
            if announcements_div_class in line :
                find_div = True
            if (find_div) :
                fileWith_divs.write(line)
                linesOf_div_block += 1
                if (linesOf_div_block == 10) : 
                    find_div = False
                    linesOf_div_block = 0
                    fileWith_divs.write("\n")
    fileWith_divs.close()

    if not (filecmp.cmp(oldPagePath + "fileWith_divs.txt", newPagePath + "fileWith_divs.txt")) :    # If old html page (old announcements) are differnt with the new html page (new announcements)
        context = ssl.create_default_context()                                                      # The default context of ssl validates the host name and its certificates and optimizes the security of the connection

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server :                  # Here our "server" will login to "accfornotificationszzz@gmail.com" mail and send our mail
            server.login(senderMail, password)                                                      #
            server.sendmail(senderMail, receiverMail, messageToSend)                                # Send the final mail

        os.remove(oldPagePath + "fileWith_divs.txt")
        shutil.move(newPagePath + "fileWith_divs.txt", oldPagePath + "fileWith_divs.txt")
    else :
        os.remove(newPagePath + "fileWith_divs.txt")
    os.remove(newPagePath + "page.html")

while (True) :
    try :
        if (checkInternet) :
            notifierBot()
    except :
        logFile = open("C:/Users/.../NotifierBot/logFileOf_notifierBot.txt", "a")                   # Only in case that we don't have internet
        now = datetime.now()                                                                        # we write dates info and a internet error
        today = date.today()                                                                        # to "logFileOf_notifierBot.txt"

        nowFormater = now.strftime("%H:%M:%S")
        todayFormated = today.strftime("%d/%m/%y")

        logFile.write(todayFormated)
        logFile.write(" ")
        logFile.write(nowFormater)
        logFile.write("\n")
        logFile.write("No internet connection found.\n\n")
        logFile.close()
    time.sleep(3600)                                                                    # We are "saying" to our script to sleep for 1 hour (3600 sec) before it start run again
