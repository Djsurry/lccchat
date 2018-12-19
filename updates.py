import sendgrid, sched, time
import os, sqlite3
from sendgrid.helpers.mail import *
key = open("key.txt").read().replace("\n", "")
def sendEmail():
    conn = sqlite3.connect("/var/www/lccchat/lccchat/lccchat.db")
    c = conn.cursor()
    l = [n[0] for n in c.execute("SELECT * FROM updates")]
    msg = 'People Who have signed up for updates: '
    for i in l:
        msg += i
        msg += ", "
    sg = sendgrid.SendGridAPIClient(apikey=key)
    from_email = Email("dsurry@wearelcc.ca")
    to_email = Email("alal2@wearelcc.ca")
    subject = "People who have singed up for updates"
    content = Content("text/plain",msg)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    conn.close()
s = sched.scheduler(time.time, time.sleep)
s.enter(60*60*24*7, 1, sendEmail)
s.run()
