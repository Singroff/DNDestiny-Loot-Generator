import json
import pickle
import sqlite3


# noinspection PyGlobalUndefined,PyRedeclaration


class GenerateDB:
    dlProgress = 0
    manifestPath = "Manifest.content"
    databasePath = "bin/database.dat"
    watermarksPath = "bin/watermark-to-season.json"

    weapon_Types = {"Hand Cannon", "Scout Rifle", "Sniper Rifle", "Submachine Gun",
                    "Auto Rifle", "Sidearm", "Rocket Launcher", "Machine Gun",
                    "Fusion Rile", "Linear Fusion Rifle", "Shotgun", "Grenade Launcher",
                    "Sword"}

    destinyDict = {}

    # {Item Name: {Type, Rarity, Description, Lore}}
    # Parse "class type" in returned json
    # Titan - 0
    # Hunter - 1
    # Warlock - 2
    # Weapon - 3

    def generateDictionaries(self):  # Move the items
        conDefault = sqlite3.connect("Manifest.content")
        cursorDefault = conDefault.cursor()
        # You were overthinking this way too hard. Now just build dictionaries and learn to make a pickle.
        for row in cursorDefault.execute(
                "select * from DestinyInventoryItemDefinition where json not like \"%Ornament%\""):
            jsonT = json.loads(row[1])
            if jsonT['displayProperties']['name'] == "Classified":
                pass
            else:
                try:
                    # May need to separate this whole thing into it's own method
                    if jsonT['itemTypeDisplayName'] in self.weapon_Types:
                        # print(jsonT['displayProperties']['name'])
                        self.destinyDict[jsonT['displayProperties']['name']] = {"type": jsonT['itemTypeDisplayName'],
                                                                                "Rarity": jsonT['inventory'][
                                                                                    'tierTypeName'],
                                                                                "HashCode": row[0], "classType": 3,
                                                                                "season": self.getSeason(jsonT),
                                                                                "icon": [
                                                                                    jsonT['displayProperties']['icon']],
                                                                                "screenshot": jsonT['screenshot'],
                                                                                "damage type": jsonT[
                                                                                    'defaultDamageType']}
                    elif jsonT['classType'] == 0:
                        # print(jsonT['displayProperties']['name'])
                        self.destinyDict[jsonT['displayProperties']['name']] = {"type": jsonT['itemTypeDisplayName'],
                                                                                "Rarity": jsonT['inventory'][
                                                                                    'tierTypeName'],
                                                                                "HashCode": row[0], "classType": 0,
                                                                                "season": self.getSeason(jsonT),
                                                                                "icon": [
                                                                                    jsonT['displayProperties']['icon']],
                                                                                "screenshot": jsonT['screenshot'],
                                                                                "armor tier": 'Heavy'}
                    elif jsonT['classType'] == 1:
                        # print(jsonT['displayProperties']['name'])
                        self.destinyDict[jsonT['displayProperties']['name']] = {"type": jsonT['itemTypeDisplayName'],
                                                                                "Rarity": jsonT['inventory'][
                                                                                    'tierTypeName'],
                                                                                "HashCode": row[0], "classType": 1,
                                                                                "season": self.getSeason(jsonT),
                                                                                "icon": [
                                                                                    jsonT['displayProperties']['icon']],
                                                                                "screenshot": jsonT['screenshot'],
                                                                                "armor tier": 'Medium'}
                    elif jsonT['classType'] == 2:
                        # print(jsonT['displayProperties']['name'])
                        self.destinyDict[jsonT['displayProperties']['name']] = {"type": jsonT['itemTypeDisplayName'],
                                                                                "Rarity": jsonT['inventory'][
                                                                                    'tierTypeName'],
                                                                                "HashCode": row[0], "classType": 2,
                                                                                "season": self.getSeason(jsonT),
                                                                                "icon": [
                                                                                    jsonT['displayProperties']['icon']],
                                                                                "screenshot": jsonT['screenshot'],
                                                                                "armor tier": 'Light'}
                except:
                    # This is the safe version of adding an item. No icon + No Screenshot. Stops errors if item
                    # doesn't have an icon.
                    if jsonT['itemTypeDisplayName'] in self.weapon_Types:
                        # print(jsonT['displayProperties']['name'])
                        self.destinyDict[jsonT['displayProperties']['name']] = {"type": jsonT['itemTypeDisplayName'],
                                                                                "Rarity": jsonT['inventory'][
                                                                                    'tierTypeName'],
                                                                                "HashCode": row[0], "classType": 3,
                                                                                "season": self.getSeason(jsonT),
                                                                                "Damage Type": jsonT[
                                                                                    'defaultDamageType']}
                    elif jsonT['classType'] == 0:
                        # print(jsonT['displayProperties']['name'])
                        self.destinyDict[jsonT['displayProperties']['name']] = {"type": jsonT['itemTypeDisplayName'],
                                                                                "Rarity": jsonT['inventory'][
                                                                                    'tierTypeName'],
                                                                                "HashCode": row[0], "classType": 0,
                                                                                "season": self.getSeason(jsonT),
                                                                                "armor tier": 'Heavy'}
                    elif jsonT['classType'] == 1:
                        # print(jsonT['displayProperties']['name'])
                        self.destinyDict[jsonT['displayProperties']['name']] = {"type": jsonT['itemTypeDisplayName'],
                                                                                "Rarity": jsonT['inventory'][
                                                                                    'tierTypeName'],
                                                                                "HashCode": row[0], "classType": 1,
                                                                                "season": self.getSeason(jsonT),
                                                                                "armor tier": 'Medium'}
                    elif jsonT['classType'] == 2:
                        # print(jsonT['displayProperties']['name'])
                        self.destinyDict[jsonT['displayProperties']['name']] = {"type": jsonT['itemTypeDisplayName'],
                                                                                "Rarity": jsonT['inventory'][
                                                                                    'tierTypeName'],
                                                                                "HashCode": row[0], "classType": 2,
                                                                                "season": self.getSeason(jsonT),
                                                                                "armor tier": 'Light'}

        # BEFORE closing cursor, be sure to create entries for engrams to add to file

        conDefault.close()

        with open(self.databasePath, 'wb') as handle:
            pickle.dump(self.destinyDict, handle)
            handle.close()

        # for key in self.destinyDict:
        #     print("The weapon is called " + key + ", it is a  " + self.destinyDict[key][
        #         'type'] + " and it is of rarity " +
        #           self.destinyDict[key]['Rarity'] + " with a hashcode of " + str(
        #         self.destinyDict[key]['HashCode']) + ".")

    def getSeason(self, item):
        if 'quality' in item:
            watermarkFile = open(self.watermarksPath)
            watermarkIcon = item['quality']['displayVersionWatermarkIcons'][0]
            allWatermarks = json.load(watermarkFile)
            if watermarkIcon in allWatermarks:
                watermarkFile.close()
                return allWatermarks[watermarkIcon]
            else:
                watermarkFile.close()
                return 1
        else:
            return 1
