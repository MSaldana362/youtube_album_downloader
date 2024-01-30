# YouTube Album Downloader
# Manuel Saldana


# Required installs for OS:
#   youtube-dl
#   id3v2
# Required installs for Python:
#   eyed3
#   pyqt5

# ---STEPS---
# Get URL, ARTIST, ALBUM, YEAR
# Create a directory for MP3s
# Copy Google search query (for album art search)
# Add info to TXT file
# Check if checkbox is checked (for track numbering)
# Download as MP3 files to directory


#   Loop through all files and change their metadata
#   Add track numbers if selected


from PyQt5.QtWidgets import *
from PyQt5 import uic

import os
import subprocess
import pyperclip as pc
import eyed3

class MyGUI(QMainWindow):

    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("downloader.ui", self)
        self.show()

        # Download push button (using type annotation)
        self.pushButton_download: QPushButton = self.findChild(QPushButton, "pushButton_download")
        self.pushButton_download.clicked.connect(lambda: self.download_yt())

    def download_yt(self):

        print("\nBeginning...\n")

        # Collect info from user input
        my_url, my_artist, my_album, my_year = self.get_info()

        # Set directory name and create
        my_dir = f"{my_artist} - {my_album} ({my_year})"
        os.mkdir(my_dir)

        # Create search string and copy to clipboard (for album art search)
        search = f"site:spotify.com: {my_artist} {my_album}"
        pc.copy(search)
        print(f"\nCopied to clipboard: {search}\n")

        # Check if info.txt exists
        if not os.path.isfile('./info.txt'):
            print("The 'info.txt' file does not exist. Creating file...")
            f = open("info.txt", "x")
            f.close()
        # Append to info.txt
        print("Adding to 'info.txt'...")
        f = open("info.txt","a")
        f.write("-----\n")
        f.write(f"{my_dir}\n")
        f.write(f"{my_url}\n")
        f.write("\n")
        f.close()

        # Check if checkbox is checked (to enable track numbering)
        self.checkBox_number: QCheckBox = self.findChild(QCheckBox, "checkBox_number")
        enable_numbering = self.checkBox_number.isChecked()
        if enable_numbering:
            print("Tracks will be numbered after download...")
        else:
            print("Tracks will not be numbered...")

        # Execute youtube-dl to download videos to mp3
        # self.youtubedl_mp3(my_url,my_dir)

        # Run...

    def youtubedl_mp3(self,yt_url,yt_dir):

        print("Downloading mp3 files using youtube-dl...\n")
        
        # Create command for youtube-dl
        # Download to mp3 format using specified output
        yt_cmd = f'youtube-dl -i --extract-audio --audio-format mp3 -o "{yt_dir}/%(title)s.%(ext)s" "{yt_url}"'

        # Execute youtube-dl command
        os.system(yt_cmd)

    def get_info(self):

        # Use type hints
        self.lineEdit_url: QLineEdit = self.findChild(QLineEdit, "lineEdit_url")
        self.lineEdit_artist: QLineEdit = self.findChild(QLineEdit, "lineEdit_artist")
        self.lineEdit_album: QLineEdit = self.findChild(QLineEdit, "lineEdit_album")
        self.lineEdit_year: QLineEdit = self.findChild(QLineEdit, "lineEdit_year")

        # Get information from QT elements
        url = self.lineEdit_url.text()
        artist = self.lineEdit_artist.text()
        album = self.lineEdit_album.text()
        year = self.lineEdit_year.text()

        # Print information
        print("USER INFO:")
        print("\tURL:\t",url)
        print("\tALBUM:\t",album)
        print("\tARTIST:\t",artist)
        print("\tYEAR:\t",year)

        # Return info
        return url, artist, album, year



def main():
    app = QApplication([])
    window = MyGUI()
    app.exec()

if __name__ == "__main__":
    main()
