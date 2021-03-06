import os
import zipfile

# Handle UI / Initialization
import pandas
import requests
from tqdm import tqdm

from GenerateDB import GenerateDB


# Populate destinyDB.json on first run. Decodes hashes from manifest and sorts them into the
# appropriate tables
# to get information, use SQLite database worldContent to get hashes
# Use pydest Async Loading in order to decode hashes.
# Only decode on first startup. You may also delete manifest once the user has
# generated the database of relevant items.
# UI:
# Engram Type
# Possible Items
# Season Checklist
# Lock by Class


class dbOps:

    def __init__(self):
        self.initializationRun()


    dlProgress = 0

    manifestPath = "Manifest.content"
    databasePath = "bin/database.dat"
    watermarksPath = "bin/watermark-to-season.json"
    currentVersion = "104343.22.04.19.2301-1-bnet.44031"

    db = GenerateDB()

    def get_manifest(self):
        manifest_url = 'http://www.bungie.net/Platform/Destiny2/Manifest/'
        HEADERS = {"x-api-key": "941d92034e1b4563a6eefd80dc6786f8"}
        # get the manifest location from the json
        r = requests.get(manifest_url, headers=HEADERS)
        print("\nGrabbing ", manifest_url)

        manifest = r.json()
        print("\nGot it!")
        mani_url = 'http://www.bungie.net' + manifest['Response']['mobileWorldContentPaths']['en']
        r = requests.get(mani_url, stream=True)

        # Download the file, write it to 'MANZIP'
        with open("MANZIP", "wb") as zip:
            manifest_Size = int(r.headers.get('content-length', 0))
            print(manifest_Size)
            block_Size = 1024
            progress_bar = tqdm(total=manifest_Size, unit='iB', unit_scale=True)
            print("\nHang tight while I grab the Destiny Database for you...")
            print("The program will launch when I'm done!")
            for data in r.iter_content(block_Size):
                progress_bar.update(len(data))
                self.dlProgress += len(data)
                zip.write(data)
            progress_bar.close()
        if manifest_Size != 0 and progress_bar.n != manifest_Size:
            print("ERROR, something went wrong")
        print("\nDownload Complete! Launching program now..")

        # Extract the file contents, and rename the extracted file
        # to 'Manifest.content'
        with zipfile.ZipFile('MANZIP') as zip:
            name = zip.namelist()
            zip.extractall()
        os.rename(name[0], 'Manifest.content')
        print('Unzipped!')

        if os.path.exists("MANZIP"):
            os.remove("MANZIP")

        if os.path.exists("world_sql_content_13b84b23c9f2eb57c71ac6633ffd8c3f.content"):
            os.remove("world_sql_content_13b84b23c9f2eb57c71ac6633ffd8c3f.content")

    def initializationRun(self):
        if os.path.exists(self.databasePath):
            print("Program Has Started!")
            print("Check the file \"Inventory.txt\" found in the directory with the exe for your rolls!")
            self.db.destinyDict = pandas.read_pickle(self.databasePath)
        else:
            print("Files Missing. One moment....")
            if os.path.exists(self.manifestPath):
                self.db.generateDictionaries()
            else:
                self.get_manifest()
                self.db.generateDictionaries()

        if os.path.exists(self.manifestPath):
            os.remove(self.manifestPath)

