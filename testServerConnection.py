import os
from ftplib import FTP_TLS

ftp_host = '10.73.220.213'
ftp_port = 21

ftp = FTP_TLS()

# set passive mode
ftp.set_pasv(True)

ftp.set_pasv(True)
ftp.connect(ftp_host, ftp_port)
ftp.login(os.environ.get(ACCOUNT_NAME), os.environ.get(KEY_PHRASE))

# set up secure data connection
ftp.prot_p()

ftp.quit()
