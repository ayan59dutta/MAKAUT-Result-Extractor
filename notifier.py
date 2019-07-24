from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

path = 'C:/Makaut-Result-Extractor/'

def send_email(roll_no, semester_no, email_id):

    fp = list(map(lambda x: x.strip(' \n'), open(path + 'gmail_credentials.txt')))
    if len(fp) < 2:
        return
    username = fp[0].strip(' \n')
    password = fp[1].strip(' \n')
    fp.close()

    subject = 'MAKAUT semester marksheet for ' + roll_no
    body = 'Hello!\n\nHere is your marksheet for semester number '+semester_no+'. Please visit www.makautexam.net for the original copy.\n\nThank You.'

    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = email_id
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'UTF-8'))
    
    part = MIMEBase('application', 'octet-stream')
    filename = path + roll_no + '_' + semester_no + '.txt'
    with open(filename, 'rb') as fp:
        part.set_payload(fp.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="'+filename+'"')
    msg.attach(part)

    smtpSession = SMTP('smtp.gmail.com', 587)
    smtpSession.starttls()
    smtpSession.login(username, password)
    smtpSession.send_message(msg, username, email_id)
    smtpSession.quit()
