from class_dict.Appendices1 import *
from class_dict.Appendices2 import *
from collections import defaultdict


class sessionData():
    def __init__(self):
        self.allSessionData = {"sessionData": [], "marshalZoneData":[], "weatherForecastData":[]}

        self.allEventData = {"eventData": []}

        self.allLobbyInfo = {"lobbyInfo": [], "numPlayers":[]}

        self.allPlayerData = {}

        self.allParticipantData = {"numActiveCars":[]}

    def updateSession(self, data):
        #self.allSessionData["header"].append(data["m_header"].copy())
        data.pop("m_header")
        data.pop("m_marshalZones")
        data.pop("m_weatherForecastSamples")
        self.allSessionData["sessionData"].append(data)
    def updateOtherSession(self,data):
        self.allSessionData["marshalZoneData"].append(data["m_marshalZones"][:data["m_numMarshalZones"]-1])
        self.allSessionData["weatherForecastData"].append(data["m_weatherForecastSamples"][:data["m_numWeatherForecastSamples"]-1])

    def updateEvent(self,data):
        #self.allEventData["header"].append(data["m_header"].copy())
        data.pop("m_header")
        self.allEventData["eventData"].append(data)

    def updateLobby(self,data):
        self.allLobbyInfo["lobbyInfo"].append(data)
    def updateOtherLobby(self,data):
        self.allLobbyInfo["numPlayers"].append(data)

    def updateUserData(self, data):
        self.allPlayerData[int(data["playerCarIndex"])] = data

    def updateOtherParticipants(self,data):
        self.allParticipantData["numActiveCars"].append(data)

    def toJsonFormat(self):
        data = {"allSessionData":self.allSessionData,
                "allEventData":self.allEventData,
                "allLobbyInfo":self.allLobbyInfo,
                "allPlayerData":self.allPlayerData}
        return data


class createPlayer():
    def __init__(self,data):
        self.playerCarIndex = data["carIndex"]
        self.currentPlayers = False

        self.allParticipantData = {"participantData":[]}

        self.allMotionData = {"motionData": [], "carMotionData": []}

        self.allLapData={"lapData": []}

        self.allSetupData = {"setupData":[]}

        self.allTelemetryData = {"telemetryData":[], "mfdPanel":[], "suggestGear":[]}

        self.allStatusData={"statusData":[]}

        self.allFinalClassificationData={"practiceData":{"finalClassificationData":[]},
                                        "qualyData":{"finalClassificationData":[]},
                                        "raceData":{"finalClassificationData":[]}}

        self.allDamageData={"damageData":[]}

        self.allHistoryData={"historyData":[], "lapHistoryData":[], "tyreStintHistoryData":[]}

    def currentPlayer(self):
        self.currentPlayers = True

    def updateParticipants(self,data):
        self.aiControlled = AiControlled[data["m_aiControlled"]]
        self.driverId = Drivers[data["m_driverId"]] # constant
        self.myTeam = MyTeamFlag[data["m_myTeam"]]
        self.name = data["m_name"]

        self.nationality = Nationality[data["m_nationality"]] # constant
        self.networkId = data["m_networkId"]
        self.raceNumber = data["m_raceNumber"] # constant
        self.teamId = Teams[data["m_teamId"]] # constant
        self.yourTelemetry = UdpStatus[data["m_yourTelemetry"]]

    def updateLobbyInfo(self,data):
        self.carNumber = data["m_carNumber"]
        self.readyStatus = data["m_readyStatus"]


    def updateCarMotion(self,data):
        self.allMotionData["carMotionData"].append(data)
    def updateMotion(self,data):
        data.pop("m_carMotionData")
        data.pop("m_header")
        self.allMotionData["motionData"].append(data)

    def updateLap(self,data):
        self.allLapData["lapData"].append(data)

    def updateSetup(self,data):
        self.allSetupData["setupData"].append(data)

    def updateTelemetry(self,data):
        self.allTelemetryData["telemetryData"].append(data)

    def updateOtherTelemetry(self,data):
        self.allTelemetryData["mfdPanel"].append({"m_mfdPanelIndex":data["m_mfdPanelIndex"],"m_mfdPanelIndexSecondaryPlayer":data["m_mfdPanelIndexSecondaryPlayer"]})
        self.allTelemetryData["suggestGear"].append(data["m_suggestedGear"])

    def updateStatus(self,data):
        if self.yourTelemetry == "public":
            self.allStatusData["statusData"].append(data)

    def updateFinal(self,mode,data):
        if mode in [1, 2, 3, 4]:
            self.allFinalClassificationData["practiceData"]["finalClassificationData"].append(data)
        elif mode in [5, 6, 7, 8, 9]:
            self.allFinalClassificationData["qualyData"]["finalClassificationData"].append(data)
        elif mode in [10, 11, 12]:
            self.allFinalClassificationData["raceData"]["finalClassificationData"].append(data)

    def getFinal(self,mode):
        if mode in [1, 2, 3, 4]:
            return self.allFinalClassificationData["practiceData"]["finalClassificationData"]
        elif mode in [5, 6, 7, 8, 9]:
            return self.allFinalClassificationData["qualyData"]["finalClassificationData"]
        elif mode in [10, 11, 12]:
            return self.allFinalClassificationData["raceData"]["finalClassificationData"]

    def updateDamage(self,data):
        if self.yourTelemetry == "public":
            self.allDamageData["damageData"].append(data)

    def updateHistory(self,data):
        self.allHistoryData["lapHistoryData"].append(data["m_lapHistoryData"].copy())
        self.allHistoryData["tyreStintHistoryData"].append(data["m_tyreStintsHistoryData"].copy())

        data.pop("m_header")
        data.pop("m_lapHistoryData")
        data.pop("m_tyreStintsHistoryData")
        self.allHistoryData["historyData"].append(data)

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

                "allMotionData":self.allMotionData,
                "allLapData":self.allLapData,
                "allSetupData":self.allSetupData,
                "allTelemetryData":self.allTelemetryData,
                "allStatusData":self.allStatusData,
                "allFinalClassificationData":self.allFinalClassificationData,
                "allDamageData":self.allDamageData,
                "allHistoryData":self.allHistoryData}
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


