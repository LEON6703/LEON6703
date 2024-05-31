import import_csv as xlsx
import pathlib
import glob
import xlsx_path
import pandas as pd


customer_name = input("Bitte Kunden Nachnamen eintragen: ")
customer_mail = input("Bitte die Kunden Email angeben: ")
cc = input("Bitte den Vertrieblichenansprechpartner angeben (und weitere für cc): ")



directory = xlsx_path.getting_xlsx()
attention = xlsx.imp_csv("Sonderkonfiguration", directory)
print(f"Warnung! : {attention} ")

#setup
apn_name = xlsx.imp_csv("apn_name", directory)
ip_ugw = xlsx.imp_csv("local_ip\nlocal_gre", directory)
ip_customer = xlsx.imp_csv("remote_ip/\nremote_gre", directory)
ip_range = xlsx.imp_csv("iprange", directory)
ip_range_mask = xlsx.imp_csv("iprange_mask", directory)
ip_acl = xlsx.extract_acl_dest_values(directory)
customer_company = xlsx.imp_csv("customer_name", directory)

proposal = xlsx.imp_csv("ike_proposal", directory)
#-- Abfrage welches Proposal genutzt wird und daraus folgend welche IKE Version
if proposal == "25" or proposal == "26":
    ike_version = 1
else:
    ike_version = 2
subject = f"Neueinrichtung IP VPN M2M-Service-Portal 3.0 Kunde: {customer_company}; APN: {apn_name} (IPV4 only)"

def mail_gen_text():
    text_body = f"Sehr geehrter {customer_name},"
    text_body += "\nnach meinen Informationen konfigurieren Sie den IPSec-Router."
    text_body += "\nVon unserer Seite wurde Ihr IPSec-Tunnel schon soweit eingerichtet."
    

    text_body += f"\n\nAPN-Name: {apn_name}"
    text_body += "\n\nHier die Daten der Konfiguration:"
    text_body += f"\nBei Ihrer Anschlatung handelt es sich um IKEv{ike_version}:"
    text_body += f"\nIP-Adresse Telekomseitig: {ip_ugw}"
    text_body += f"\nIP-Adresse Kundenseitig : {ip_customer}"
    text_body += f"\nClient IP-Adressbereich : {ip_range} /{ip_range_mask}"
    text_body += f"\n\nDer PSK wird von mir per SMS/verschlüsselter Mail verschickt."
    text_body += f"\n\nPolicy-ACL: "
    text_body += f"\n{ip_acl}"
    text_body += f"\nBitte melden Sie sich nach der Einrichtung auf Ihrer Seite, um mit mir einen gemeinsamen Termin zur Prüfung Ihres Tunnels zu finden."
    text_body += f"\nOhne diesen Einrichtungstest wird der Tunnel nicht in den Betrieb gehen!"

    if proposal == 25:
        prop_25 = "\n\nNun die IPSec Parameter für Ihren Tunnel:"
        prop_25 += f"\nIKEv{ike_version}" 
        prop_25 += "\nParameter	                          Phase I	    Phase II"
        prop_25 +="\nDiffie-Hellman Group / PFS:  Group 14        None"
        prop_25 +="\nEncryption (authentication)   AES256	       AES256"
        prop_25 +="\nEncryption (integrity)	            n/a	                  x"
        prop_25 +="\nHash algorithm	                       SHA2-256	      SHA2-256"
        prop_25 +="\nExchange Mode	                     Main	         x"
        prop_25 +="\nKey Lifetime / SA-Lifetime	86400 sec	3600 sec"
        prop_25 +="\nEncryption Protocol Mode      x          	     ESP Tunnel"
        text_body += prop_25
    if proposal == 26:
        prop_26 = "\nNun die IPSec Parameter für Ihren Tunnel:"
        prop_26 += f"\nIKEv{ike_version}" 
        prop_26 += "\nParameter	                          Phase I	    Phase II"
        prop_26 +="\nDiffie-Hellman Group / PFS:  Group 14        Group 14"
        prop_26 +="\nEncryption (authentication)   AES256	       AES256"
        prop_26 +="\nEncryption (integrity)	            n/a	                  x"
        prop_26 +="\nHash algorithm	                       SHA2-256	      SHA2-256"
        prop_26 +="\nExchange Mode	                     Main	         x"
        prop_26 +="\nKey Lifetime / SA-Lifetime	28800 sec	3600 sec"
        prop_26 +="\nEncryption Protocol Mode      x          	     ESP Tunnel"
        text_body += prop_26
    if proposal == 15:
        prop_15 = "\nNun die IPSec Parameter für Ihren Tunnel:"
        prop_15 += f"\nIKEv{ike_version}" 
        prop_15 += "\nParameter	                          Phase I	                Phase II"
        prop_15 +="\nDiffie-Hellman Group / PFS:  Group 14                    None"
        prop_15 +="\nEncryption (authentication)   AES256	                  AES256"
        prop_15 +="\nEncryption (integrity)	            HMAC-SHA2-256      x"
        prop_15 +="\nHash algorithm	                       SHA2-256	                 SHA2-256"
        prop_15 +="\nExchange Mode	                     n/a	                      x"
        prop_15 +="\nKey Lifetime / SA-Lifetime	28800 sec	          3600 sec"
        prop_15 +="\nEncryption Protocol Mode      x          	                ESP Tunnel"
        text_body += prop_15   
    if proposal == 16:
        prop_16 = "\nNun die IPSec Parameter für Ihren Tunnel:"
        prop_16 += f"\nIKEv{ike_version}" 
        prop_16 += "\nParameter	                          Phase I	                Phase II"
        prop_16 +="\nDiffie-Hellman Group / PFS:  Group 14                   Group 14"
        prop_16 +="\nEncryption (authentication)   AES256	                  AES256"
        prop_16 +="\nEncryption (integrity)	            HMAC-SHA2-256      x"
        prop_16 +="\nHash algorithm	                       SHA2-256	                 SHA2-256"
        prop_16 +="\nExchange Mode	                     n/a	                      x"
        prop_16 +="\nKey Lifetime / SA-Lifetime	28800 sec	          3600 sec"
        prop_16 +="\nEncryption Protocol Mode      x          	                ESP Tunnel"
        text_body += prop_16  
    if proposal == 11:
        prop_11 = "\nNun die IPSec Parameter für Ihren Tunnel:"
        prop_11 += f"\nIKEv{ike_version}" 
        prop_11 += "\nParameter	                          Phase I	                Phase II"
        prop_11 +="\nDiffie-Hellman Group / PFS:  Group 16                   Group 16"
        prop_11 +="\nEncryption (authentication)   AES256	                  AES256"
        prop_11 +="\nEncryption (integrity)	            SHA2-256                  x"
        prop_11 +="\nHash algorithm	                       SHA2-256	                 SHA2-256"
        prop_11 +="\nExchange Mode	                     Main	                   x"
        prop_11 +="\nKey Lifetime / SA-Lifetime	28800 sec	          3600 sec"
        prop_11 +="\nEncryption Protocol Mode      x          	                ESP Tunnel"
        text_body += prop_11      
    if proposal == 12:
        prop_12 = "\nNun die IPSec Parameter für Ihren Tunnel:"
        prop_12 += f"IKEv{ike_version}" 
        prop_12 += "\nParameter	                          Phase I	                Phase II"
        prop_12 +="\nDiffie-Hellman Group / PFS:   Group 16                  Group 16"
        prop_12 +="\nEncryption (authentication)   AES256	                  AES256"
        prop_12 +="\nEncryption (integrity)	            HMAC-SHA2-256     x"
        prop_12 +="\nHash algorithm	                       SHA2-256	                 SHA2-256"
        prop_12 +="\nExchange Mode	                     n/a	                     x"
        prop_12 +="\nKey Lifetime / SA-Lifetime	28800 sec	          3600 sec"
        prop_12 +="\nEncryption Protocol Mode      x          	                ESP Tunnel"
        text_body += prop_12 
    
    return text_body

#------------------Main
mail_gen_text()
