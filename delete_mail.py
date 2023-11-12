import imaplib
import email
from email.header import decode_header
# the constant file must be contain your username, password 
# and email server as variables
from constant import user_name, password, hotmail


def CleanMailBox(user, paswd):

    # connect to server and login
    imap = imaplib.IMAP4_SSL(hotmail)
    imap.login(user, paswd)

    # select the mail-folder and searching 
    # messages in selected mail-folder
    imap.select('INBOX')
    status, message = imap.search(None, 'All')

    msg = message[0].split(b' ')

    # iterating, fetching as tuple, also decoding and moving all messages 
    # to created - folder deleted messages
    for mail in msg:
        _, mess = imap.fetch(mail, '(RFC822)')
        for resp in mess:
            if isinstance(resp, tuple):
                mess = email.message_from_bytes(resp[1])
                subject = decode_header(mess['Subject'])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode()
                print('Deleting process...', subject)
        imap.store(mail, '+FLAGS', '\\Deleted')

    # cleaning deleted folder
    # close server and logout
    imap.expunge()
    imap.close()
    imap.logout()

if __name__ == '__main__':
    CleanMailBox(user_name, password)