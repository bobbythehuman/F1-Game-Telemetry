from class_dict.Appendices1 import *
from class_dict.Appendices2 import *
from collections import defaultdict


class sessionData():
    def __init__(self):
        self.allSessionData = {"sessionData": []}

        self.allEventData = {"eventData": []}

        self.allLobbyInfo = {"lobbyInfo": [], "numPlayers":[]}

        self.allPlayerData = {}

        self.allParticipantData = {"participantData":[]}

    def updateSession(self, data):
        self.allSessionData["sessionData"].append(data)

    def updateEvent(self, data):
        self.allEventData["eventData"].append(data)

    def updateLobby(self, data):
        self.allLobbyInfo["lobbyInfo"].append(data)

    def updateUserData(self, data):
        self.allPlayerData[int(data["carIndex"])] = data

    def updateParticipants(self, data):
        self.allParticipantData["participantData"].append(data)

    def toJsonFormat(self):
        data = {"allSessionData":self.allSessionData,
                "allEventData":self.allEventData,
                "allLobbyInfo":self.allLobbyInfo,
                "allPlayerData":self.allPlayerData,
                "allParticipantData":self.allParticipantData}
        return data


class createPlayer():
    def __init__(self, data):
        self.playerCarIndex = data["carIndex"]
        self.currentPlayers = False

        # self.allParticipantData = {"participantData":[]}

        self.allMotionData = {"carMotionData": []}

        self.allLapData = {"lapData": []}

        self.allSetupData = {"setupData":[]}

        self.allTelemetryData = {"telemetryData":[]}

        self.allStatusData = {"statusData":[]}

        self.allFinalClassificationData = {"practiceData":{"finalClassificationData":[]},
                                            "qualyData":{"finalClassificationData":[]},
                                            "raceData":{"finalClassificationData":[]},
                                            "other":{"finalClassificationData":[]}}

        self.allDamageData = {"damageData":[]}

        self.allHistoryData = {"historyData":[]}

        self.allTyreSetData = {"tyreSetData":[]}

        self.driverId = Drivers[data["m_driverId"]] # constant
        self.myTeam = MyTeamFlag[data["m_myTeam"]] # constant
        self.nationality = Nationality[data["m_nationality"]] # constant
        self.raceNumber = data["m_raceNumber"] # constant
        self.teamId = Teams[data["m_teamId"]] # constant
        self.platform = Platform[data["m_platform"]] # constant

        self.overtaking = 0
        self.overtaken = 0

    def currentPlayer(self):
        self.currentPlayers = True
        self.allMotionExData = {"motionExData":[]}

        self.allLapData["otherLapData"] = {"m_timeTrialPBCarIdx":[], "m_timeTrialRivalCarIdx":[]}

        self.allTelemetryData["otherTelemetryData"] = {"m_mfdPanelIndex":[], "m_mfdPanelIndexSecondaryPlayer":[], "m_suggestedGear":[]}

    def updateParticipants(self,data):
        self.aiControlled = AiControlled[data["m_aiControlled"]]
        self.name = data["m_name"]
        self.networkId = data["m_networkId"]
        self.yourTelemetry = UdpStatus[data["m_yourTelemetry"]]
        self.showOnlineNames = AssistSwitch[data["m_showOnlineNames"]]

    def updateLobbyInfo(self,data):
        self.carNumber = data["m_carNumber"]
        self.readyStatus = data["m_readyStatus"]

    def updateCarMotion(self, data):
        self.allMotionData["carMotionData"].append(data)

    def updateLap(self, data):
        self.allLapData["lapData"].append(data)

    def updateOtherLap(self, data):
        self.allLapData["otherLapData"]["m_timeTrialPBCarIdx"].append(data["m_timeTrialPBCarIdx"])
        self.allLapData["otherLapData"]["m_timeTrialRivalCarIdx"].append(data["m_timeTrialRivalCarIdx"])

    def updateSetup(self, data):
        self.allSetupData["setupData"].append(data)

    def updateTelemetry(self, data):
        self.allTelemetryData["telemetryData"].append(data)

    def updateOtherTelemetry(self, data):
        self.allTelemetryData["otherTelemetryData"]["m_mfdPanelIndex"].append(data["m_mfdPanelIndex"])
        self.allTelemetryData["otherTelemetryData"]["m_mfdPanelIndexSecondaryPlayer"].append(data["m_mfdPanelIndexSecondaryPlayer"])
        self.allTelemetryData["otherTelemetryData"]["m_suggestedGear"].append(data["m_suggestedGear"])

    def updateStatus(self, data):
        if self.yourTelemetry == "public":
            self.allStatusData["statusData"].append(data)

    def updateFinal(self, mode, data):
        if mode in [1, 2, 3, 4]:
            self.allFinalClassificationData["practiceData"]["finalClassificationData"].append(data)
        elif mode in [5, 6, 7, 8, 9]:
            self.allFinalClassificationData["qualyData"]["finalClassificationData"].append(data)
        elif mode in [10, 11, 12]:
            self.allFinalClassificationData["raceData"]["finalClassificationData"].append(data)
        else:
            self.allFinalClassificationData["other"]["finalClassificationData"].append(data)

    def getFinal(self, mode):
        if mode in [1, 2, 3, 4]:
            return self.allFinalClassificationData["practiceData"]["finalClassificationData"]
        elif mode in [5, 6, 7, 8, 9]:
            return self.allFinalClassificationData["qualyData"]["finalClassificationData"]
        elif mode in [10, 11, 12]:
            return self.allFinalClassificationData["raceData"]["finalClassificationData"]
        else:
            return self.allFinalClassificationData["other"]["finalClassificationData"]

    def updateDamage(self, data):
        if self.yourTelemetry == "public":
            self.allDamageData["damageData"].append(data)

    def updateHistory(self, data):
        self.allHistoryData["historyData"].append(data)

    def updateTyreSet(self, data):
        self.allTyreSetData["tyreSetData"].append(data)

    def updateMotionEx(self, data):
        self.allMotionExData["motionExData"].append(data)

    def toJsonFormat(self):
        data = {"playerCarIndex":self.playerCarIndex,
                "currentPlayers":self.currentPlayers,
                "aiControlled":self.aiControlled,
                "driverId":self.driverId,
                "myTeam":self.myTeam,
                "name":self.name,
                "nationality":self.nationality,
                "networkId":self.networkId,
                "raceNumber":self.raceNumber,
                "teamId":self.teamId,
                "yourTelemetry":self.yourTelemetry,
                "platform":self.platform,
                "showOnlineNames":self.showOnlineNames,

                "allMotionData":self.allMotionData,
                "allLapData":self.allLapData,
                "allSetupData":self.allSetupData,
                "allTelemetryData":self.allTelemetryData,
                "allStatusData":self.allStatusData,
                "allFinalClassificationData":self.allFinalClassificationData,
                "allDamageData":self.allDamageData,
                "allHistoryData":self.allHistoryData,
                "allTyreSetData":self.allTyreSetData,
                "allMotionExData":self.allMotionExData}
        return data

    def compressJson(self):
        def compressLoop(_array):
            def get_group(s):
                num = []
                last = ""
                for x in s:
                    if x != last:
                        num.append((x,1))
                    else:
                        value = num[-1]
                        num[-1] = (value[0], value[1]+1)
                    last = x
                return num
            def compressData(_data):
                _output = []
                _groups = get_group(_data)
                for _group in _groups:
                    _output.append(f"{_group[0]}x{_group[1]}")
                return _output
            _dict = defaultdict(list)
            _list = []
            if type(_array) in [dict, defaultdict]:
                for _key, _value in _array.items():
                    if _value:
                        _dict[_key] = compressLoop(_value)
                    else:
                        _dict[_key] = []
                return _dict
            elif type(_array[0]) in [dict, defaultdict, list]:
                for _item in _array:
                    _list.append(compressLoop(_item))
                return _list
            else:
                return compressData(_array)

        def arrangeDataLoop(_array):
            def arrange(_data):
                _dict = defaultdict(list)
                _list = []
                for _item in _data:
                    for _key, _value in _item.items():
                        _dict[_key].append(_value)
                return _dict
            _dict = defaultdict(list)
            _list = []
            if type(_array) in [dict, defaultdict]:
                for _key, _value in _array.items():
                    if type(_value) in [dict, defaultdict, list]:
                        _dict[_key] = arrangeDataLoop(_value)
                    else:
                        return True
                return _dict
            elif type(_array) == list:
                for _item in _array:
                    if type(_item) in [dict, defaultdict]:
                        _dateList = arrangeDataLoop(_item)
                        if _dateList is True:
                            _list = arrange(_array)
                            break
                    elif type(_item) == list:
                        _list.append(arrangeDataLoop(_item))
                    else:
                        return _array
                return _list

        data = {"playerCarIndex":self.playerCarIndex,
                "currentPlayers":self.currentPlayers,
                "aiControlled":self.aiControlled,
                "driverId":self.driverId,
                "myTeam":self.myTeam,
                "name":self.name,
                "nationality":self.nationality,
                "networkId":self.networkId,
                "raceNumber":self.raceNumber,
                "teamId":self.teamId,
                "yourTelemetry":self.yourTelemetry,

                "allMotionData":compressLoop(arrangeDataLoop(self.allMotionData)),
                "allLapData":compressLoop(arrangeDataLoop(self.allLapData)),
                "allSetupData":compressLoop(arrangeDataLoop(self.allSetupData)),
                "allTelemetryData":compressLoop(arrangeDataLoop(self.allTelemetryData)),
                "allStatusData":compressLoop(arrangeDataLoop(self.allStatusData)),
                "allFinalClassificationData":self.allFinalClassificationData,
                "allDamageData":compressLoop(arrangeDataLoop(self.allDamageData)),
                "allHistoryData":compressLoop(arrangeDataLoop(self.allHistoryData))}
        return data


class createPlayer_sort():
    def __init__(self, data):
        self.playerCarIndex = data["carIndex"]
        self.currentPlayers = False

        # self.allParticipantData = {"participantData":[]}

        self.allMotionData = {"carMotionData": {}} # update

        self.allLapData = {"lapData": {}} # update

        self.allSetupData = {"setupData": {}} # update

        self.allStatusData = {"statusData": {}} # update

        self.allTelemetryData = {"telemetryData":{}} # small change

        self.allDamageData = {"damageData":{}} # small change



        self.allFinalClassificationData = {"practiceData":{"finalClassificationData":[]},
                                            "qualyData":{"finalClassificationData":[]},
                                            "raceData":{"finalClassificationData":[]},
                                            "other":{"finalClassificationData":[]}}



        self.allHistoryData = {"historyData":[]}

        self.allTyreSetData = {"tyreSetData":[]}

        self.driverId = Drivers[data["m_driverId"]] # constant
        self.myTeam = MyTeamFlag[data["m_myTeam"]] # constant
        self.nationality = Nationality[data["m_nationality"]] # constant
        self.raceNumber = data["m_raceNumber"] # constant
        self.teamId = Teams[data["m_teamId"]] # constant
        self.platform = Platform[data["m_platform"]] # constant

    def currentPlayer(self):
        self.currentPlayers = True
        self.allMotionExData = {"motionExData":{}} # small change

        self.allLapData["otherLapData"] = {"m_timeTrialPBCarIdx":[], "m_timeTrialRivalCarIdx":[]}

        self.allTelemetryData["otherTelemetryData"] = {"m_mfdPanelIndex":[], "m_mfdPanelIndexSecondaryPlayer":[], "m_suggestedGear":[]}

    def updateParticipants(self, data):
        self.aiControlled = AiControlled[data["m_aiControlled"]]
        self.name = data["m_name"]
        self.networkId = data["m_networkId"]
        self.yourTelemetry = UdpStatus[data["m_yourTelemetry"]]
        self.showOnlineNames = AssistSwitch[data["m_showOnlineNames"]]

    def updateLobbyInfo(self, data):
        self.carNumber = data["m_carNumber"]
        self.readyStatus = data["m_readyStatus"]

    def updateCarMotion(self, data):
        for info in data.keys():
            if info in self.allMotionData["carMotionData"].keys():
                self.allMotionData["carMotionData"][info].append(data[info])
            else:
                self.allMotionData["carMotionData"][info] = [data[info]]

    def updateLap(self, data):
        for info in data.keys():
            if info in self.allLapData["lapData"].keys():
                self.allLapData["lapData"][info].append(data[info])
            else:
                self.allLapData["lapData"][info] = [data[info]]

    def updateOtherLap(self, data):
        self.allLapData["otherLapData"]["m_timeTrialPBCarIdx"].append(data["m_timeTrialPBCarIdx"])
        self.allLapData["otherLapData"]["m_timeTrialRivalCarIdx"].append(data["m_timeTrialRivalCarIdx"])

    def updateSetup(self, data):
        for info in data.keys():
            if info in self.allSetupData["setupData"].keys():
                self.allSetupData["setupData"][info].append(data[info])
            else:
                self.allSetupData["setupData"][info] = [data[info]]

    def updateTelemetry(self, data):
        # self.allTelemetryData["telemetryData"].append(data)

        for info in data.keys():
            if info in self.allTelemetryData["telemetryData"].keys():
                self.allTelemetryData["telemetryData"][info].append(data[info])
            else:
                self.allTelemetryData["telemetryData"][info] = [data[info]]

    def updateOtherTelemetry(self, data):
        self.allTelemetryData["otherTelemetryData"]["m_mfdPanelIndex"].append(data["m_mfdPanelIndex"])
        self.allTelemetryData["otherTelemetryData"]["m_mfdPanelIndexSecondaryPlayer"].append(data["m_mfdPanelIndexSecondaryPlayer"])
        self.allTelemetryData["otherTelemetryData"]["m_suggestedGear"].append(data["m_suggestedGear"])

    def updateStatus(self, data):
        if self.yourTelemetry == "public":
            for info in data.keys():
                if info in self.allStatusData["statusData"].keys():
                    self.allStatusData["statusData"][info].append(data[info])
                else:
                    self.allStatusData["statusData"][info] = [data[info]]

    def updateFinal(self, mode, data):
        if mode in [1, 2, 3, 4]:
            self.allFinalClassificationData["practiceData"]["finalClassificationData"].append(data)
        elif mode in [5, 6, 7, 8, 9]:
            self.allFinalClassificationData["qualyData"]["finalClassificationData"].append(data)
        elif mode in [10, 11, 12]:
            self.allFinalClassificationData["raceData"]["finalClassificationData"].append(data)
        else:
            self.allFinalClassificationData["other"]["finalClassificationData"].append(data)

    def getFinal(self, mode):
        if mode in [1, 2, 3, 4]:
            return self.allFinalClassificationData["practiceData"]["finalClassificationData"]
        elif mode in [5, 6, 7, 8, 9]:
            return self.allFinalClassificationData["qualyData"]["finalClassificationData"]
        elif mode in [10, 11, 12]:
            return self.allFinalClassificationData["raceData"]["finalClassificationData"]
        else:
            return self.allFinalClassificationData["other"]["finalClassificationData"]

    def updateDamage(self, data):
        if self.yourTelemetry == "public":
            # self.allDamageData["damageData"].append(data)

            for info in data.keys():
                if info in self.allDamageData["damageData"].keys():
                    self.allDamageData["damageData"][info].append(data[info])
                else:
                    self.allDamageData["damageData"][info] = [data[info]]

    def updateHistory(self, data):
        self.allHistoryData["historyData"].append(data)

    def updateTyreSet(self, data):
        self.allTyreSetData["tyreSetData"].append(data)

    def updateMotionEx(self, data):
        # self.allMotionExData["motionExData"].append(data)

        for info in data.keys():
            if info in self.allMotionExData["motionExData"].keys():
                self.allMotionExData["motionExData"][info].append(data[info])
            else:
                self.allMotionExData["motionExData"][info] = [data[info]]

    def toJsonFormat(self):
        data = {"playerCarIndex":self.playerCarIndex,
                "currentPlayers":self.currentPlayers,
                "aiControlled":self.aiControlled,
                "driverId":self.driverId,
                "myTeam":self.myTeam,
                "name":self.name,
                "nationality":self.nationality,
                "networkId":self.networkId,
                "raceNumber":self.raceNumber,
                "teamId":self.teamId,
                "yourTelemetry":self.yourTelemetry,
                "platform":self.platform,
                "showOnlineNames":self.showOnlineNames,

                "allMotionData":self.allMotionData,
                "allLapData":self.allLapData,
                "allSetupData":self.allSetupData,
                "allTelemetryData":self.allTelemetryData,
                "allStatusData":self.allStatusData,
                "allFinalClassificationData":self.allFinalClassificationData,
                "allDamageData":self.allDamageData,
                "allHistoryData":self.allHistoryData,
                "allTyreSetData":self.allTyreSetData,
                "allMotionExData":self.allMotionExData}
        return data
