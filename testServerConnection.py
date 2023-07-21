from ftplib import FTP_TLS

ftp_host = '10.73.220.213'
ftp_port = 21

ftp = FTP_TLS()
ftp.set_pasv(True)
ftp.connect(ftp_host, ftp_port)
ftp.login(getpass('Enter username: '), getpass('Enter password: '))

# set up secure data connection
ftp.prot_p()

ftp.quit()
