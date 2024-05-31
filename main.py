import send 
import import_csv as xlsx
import mail_text
import xlsx_path
import sys
#------------------------------------------Settings

directory = xlsx_path.getting_xlsx()
# Sammeln aller Daten für jeden Statuswert
def mail_formatting():
    # Zusammenführen der Daten zu einem Textkörper für die E-Mail
    body = mail_text.mail_gen_text()
    customer_email = mail_text.customer_mail
    cc = mail_text.cc
       
    send.send_email(mail_text.subject, body, customer_email, cc)


#------------------------------------Main 
mail_formatting()
sys.exit()
