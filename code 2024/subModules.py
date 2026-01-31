from class_dict import MainAppendices, SubAppendices
import time
import re


class eventLog:
    def __init__(self):
        self.participantsData = None
        self.getSessionDetails = True
        self.recentPacketData = None
        self.sendLobbyInfo = True
        self.doFinalClassification = True
        self.skips = 0
        self.backLog = []

        self.endDataLogging = False
        current_time = time.strftime("%H-%M-%S", time.localtime())
        print(f"Creating file {current_time}.csv")
        self.myLogFile = open(f"{current_time}.csv", "a")
        self.myLogFile.write(
            "Event String Code,Lap,Sector,Distance around lap,Message\n"
        )

    def getNameID(self, index):
        if self.participantsData:
            userData = self.participantsData.m_participants[index]

            if userData.m_driverId == 14:
                userData.m_name = "PEREZ"

            text = f"[ID:{index}-"
            if userData.m_name != "Player":
                text += f"{userData.m_name}-"
            team = MainAppendices.Teams[userData.m_teamId]
            text += f"{team}-"
            if userData.m_nationality != 0:
                nationality = MainAppendices.Nationality[userData.m_nationality]
                text += f"{nationality}-"
            text += f"{userData.m_raceNumber}]"
            return text
        else:
            return f"[ID:{index}]"

    def getPenID(self, index, mode):
        if mode == "pen":
            return f"[{MainAppendices.PenaltyType[index]}]"
        elif mode == "inf":
            return f"[{MainAppendices.InfringmentType[index]}]"

    def getSCID(self, index, mode):
        if mode == "sc":
            return f"[{SubAppendices.safetyCarType[index]}]"
        elif mode == "evt":
            return f"[{SubAppendices.eventType[index]}]"

    def writeToFile(self, text, ESC=None, idx=None):
        if ESC:
            print(f"[{ESC}] - {text}")
            if idx is not None and self.recentPacketData.LapData:
                tempData = self.recentPacketData.LapData.m_lapData[idx]
                subData = f"[{ESC}],{tempData.m_currentLapNum},{tempData.m_sector+1},{tempData.m_lapDistance},"
            else:
                subData = f"[{ESC}],NA,NA,NA,"
            # subData = f"[{ESC}],NA,NA,NA,"
            # print("----- Error occured, probally no useable packets -----")
        else:
            subData = f"[{ESC}],NA,NA,NA,"
            print(text)
            text = text.strip("\n")
        self.myLogFile.write(subData)

        text += "\n"
        self.myLogFile.write(text)

    def LogData(self, packetID, data):
        self.recentPacketData = data
        if packetID == 9:
            self.getSessionDetails = True
            self.sendLobbyInfo = True
            self.skips = 0

        if packetID == 8:
            if self.doFinalClassification:

                def updateTyresValues(tyreStint, tyreType):
                    for x in range(tyreStint.count(0)):
                        tyreStint.remove(0)
                    if tyreType == "Actual":
                        for i, v in enumerate(tyreStint):
                            tyreName = SubAppendices.actualTyreCompound[v]
                            tyreStint[i] = tyreName
                    elif tyreType == "Visual":
                        for i, v in enumerate(tyreStint):
                            tyreName = SubAppendices.visualTyreCompound[v]
                            tyreStint[i] = tyreName
                    return tyreStint

                sessionDetails = self.recentPacketData.SessionData
                current_time = time.strftime("%H-%M-%S", time.localtime())
                fileName = f"{sessionDetails.m_trackId}-{sessionDetails.m_sessionType}__{current_time}"
                finalClassificationFile = open(f"{fileName}.csv", "a")

                if sessionDetails.m_sessionType in [9, 14]:
                    finalClassificationFile.write(
                        "Position,User,Best Lap Time,Total Lap Time,Result Status,Visual Tyre Compound,Actual Tyre Compound\n"
                    )

                elif sessionDetails.m_sessionType in [15, 16, 17]:
                    finalClassificationFile.write(
                        "Position,User,Best Lap Time,Total Lap Time,Laps Completed,Result Status,Grid Position,Points,Total Penalties,Penalty Count,Pit Stop Count,Stints Completed,Visual Tyre Compound,Actual Tyre Compound\n"
                    )

                self.doFinalClassification = False
                newData = self.recentPacketData.FinalClassificationData
                grid = {}
                index = 0
                for userData in newData.m_classificationData:
                    if userData.m_resultStatus != 0:
                        userData.participantIndex = index
                        grid[userData.m_position] = userData
                    if len(grid) == newData.m_numCars:
                        break
                    index += 1

                print()
                for racePosisition in range(newData.m_numCars):
                    userData = grid[racePosisition + 1]

                    position = userData.m_position
                    userName = self.getNameID(userData.participantIndex)
                    lapsCompleted = userData.m_numLaps
                    startPosition = userData.m_gridPosition
                    points = userData.m_points
                    pitStopCount = userData.m_numPitStops
                    resultsStatus = SubAppendices.resultStatus[userData.m_resultStatus]
                    bestLapTime = userData.m_bestLapTimeInMs
                    totalRaceTime = userData.m_totalRaceTime
                    totalPenalties = userData.m_penaltiesTime
                    penaltyCount = userData.m_numPenalties
                    stintsCompleted = userData.m_numTyreStints
                    actualTyreCompound = updateTyresValues(
                        userData.m_tyreStintsActual, "Actual"
                    )
                    visualTyreCompound = updateTyresValues(
                        userData.m_tyreStintsVisual, "Visual"
                    )

                    if sessionDetails.m_sessionType in [9, 14]:
                        finalClassificationText = f"{position},{userName},{bestLapTime},{totalRaceTime},{resultsStatus},{'-'.join(visualTyreCompound)},{'-'.join(actualTyreCompound)}\n"

                    elif sessionDetails.m_sessionType in [15, 16, 17]:
                        finalClassificationText = f"{position},{userName},{bestLapTime},{totalRaceTime},{lapsCompleted},{resultsStatus},{startPosition},{points},{totalPenalties},{penaltyCount},{pitStopCount},{stintsCompleted},{'-'.join(visualTyreCompound)},{'-'.join(actualTyreCompound)}\n"

                    finalClassificationFile.write(finalClassificationText)
                    print(finalClassificationText[:-1])
                self.writeToFile("----- Final Classifications in new file -----")
                finalClassificationFile.close()
                print()

                if self.endDataLogging:
                    print("Session end, closing and creating new file")
                    self.myLogFile.close()
                    current_time = time.strftime("%H-%M-%S", time.localtime())
                    print(f"Creating file {current_time}.csv")
                    self.myLogFile = open(f"{current_time}.csv", "a")
                    self.myLogFile.write(
                        "Event String Code,Lap,Sector,Distance around lap,Message\n"
                    )
                    self.endDataLogging = False

        if packetID == 1:
            if self.getSessionDetails and self.skips == 2:
                self.getSessionDetails = False
                sessionDetails = self.recentPacketData.SessionData

                if self.sendLobbyInfo:
                    self.sendLobbyInfo = False

                    self.writeToFile("\n-----------[Track Info]-----------")
                    trackId = MainAppendices.Tracks[sessionDetails.m_trackId]

                    trackLength = sessionDetails.m_trackLength
                    pitSpeedLimit = sessionDetails.m_pitSpeedLimit
                    self.writeToFile(f"Track Id        - [{trackId}]")
                    self.writeToFile(f"Track Length    - [{trackLength} Metres]")
                    self.writeToFile(f"Pit Speed Limit - [{pitSpeedLimit} KPH]")
                    self.writeToFile("----------------------------------\n")

                    self.writeToFile(
                        "----------------------[Session Setup]----------------------"
                    )
                    sessionSetupList = [
                        "m_equalCarPerformance",
                        "m_recoveryMode",
                        "m_surfaceType",
                        "m_lowFuelMode",
                        "m_raceStarts",
                        "m_tyreTemperature",
                        "m_pitLaneTyreSim",
                        "m_carDamage",
                        "m_carDamageRate",
                        "m_collisions",
                        "m_collisionsOffForFirstLapOnly",
                        "m_mpUnsafePitRelease",
                        "m_mpOffForGriefing",
                        "m_cornerCuttingStringency",
                        "m_parcFermeRules",
                        "m_pitStopExperience",
                        "m_safetyCar",
                        "m_safetyCarExperience",
                        "m_formationLap",
                        "m_formationLapExperience",
                        "m_redFlags",
                        "m_affectsLicenceLevelMP",
                    ]
                    longestWord = len(max(sessionSetupList, key=len)) + 3
                    aiDifficulty = sessionDetails.m_aiDifficulty
                    self.writeToFile(
                        f"AI Difficulty{' '*(longestWord-13)} - [{aiDifficulty}]"
                    )
                    for x in sessionSetupList:
                        valueText = x[2:]
                        displayText = " ".join(
                            re.findall("[a-zA-Z][^A-Z]*", valueText)
                        ).title()
                        value = getattr(SubAppendices, valueText)[
                            getattr(sessionDetails, x)
                        ]
                        self.writeToFile(
                            f"{displayText}{' '*(longestWord-len(displayText))} - [{value}]"
                        )
                    self.writeToFile(
                        "-----------------------------------------------------------\n"
                    )

                    self.writeToFile("-------[Other Info]-------")
                    networkGame = SubAppendices.networkGame[
                        sessionDetails.m_networkGame
                    ]
                    self.writeToFile(f"Network Game - [{networkGame}]")
                    self.writeToFile("--------------------------")

                self.writeToFile("\n----------[Session Info]----------")
                formula = SubAppendices.FormulaType[sessionDetails.m_formula]
                gameMode = MainAppendices.GameModes[sessionDetails.m_gameMode]
                sessionType = MainAppendices.SessionType[sessionDetails.m_sessionType]
                totalLaps = sessionDetails.m_totalLaps
                sessionLength = SubAppendices.sessionLength[
                    sessionDetails.m_sessionLength
                ]
                ruleSet = MainAppendices.Rulesets[sessionDetails.m_ruleSet]
                currentWeather = SubAppendices.weather[sessionDetails.m_weather]
                timeOfDay = sessionDetails.m_timeOfDay
                time2 = f"{timeOfDay//60}:{timeOfDay%60}"
                self.writeToFile(f"Formula         - [{formula}]")
                self.writeToFile(f"Session Type    - [{sessionType}]")
                self.writeToFile(f"Session Length  - [{sessionLength}]")
                self.writeToFile(f"Total Laps      - [{totalLaps}]")
                self.writeToFile(f"Game Mode       - [{gameMode}]")
                self.writeToFile(f"Rule Set        - [{ruleSet}]")
                self.writeToFile(f"Time Of Day     - [{time2}]")
                self.writeToFile(f"Current weather - [{currentWeather}]")
                self.writeToFile("----------------------------------\n")

                # m_numWeatherForecastSamples = Packet.m_numWeatherForecastSamples
                # m_weatherForecastSamples = allWeatherSamples
                # m_forecastAccuracy = Packet.m_forecastAccuracy

                # assists
                # steeringAssist = sessionDetails.m_steeringAssist
                # brakingAssist = sessionDetails.m_brakingAssist
                # gearboxAssist = sessionDetails.m_gearboxAssist
                # pitAssist = sessionDetails.m_pitAssist
                # pitReleaseAssist = sessionDetails.m_pitReleaseAssist
                # ersAssist = sessionDetails.m_ersAssist
                # drsAssist = sessionDetails.m_drsAssist
                # dynamicRacingLine = sessionDetails.m_dynamicRacingLine
                # dynamicRacingLineType = sessionDetails.m_dynamicRacingLineType

                weekendStructure = sessionDetails.m_weekendStructure
                for x in range(weekendStructure.count(0)):
                    weekendStructure.remove(0)
                if not weekendStructure:
                    self.endDataLogging = True
                elif sessionDetails.m_sessionType == weekendStructure[-1]:
                    self.endDataLogging = True

            # m_numSafetyCarPeriods = Packet.m_numSafetyCarPeriods
            # m_numVirtualSafetyCarPeriods = Packet.m_numVirtualSafetyCarPeriods
            # m_numRedFlagPeriods = Packet.m_numRedFlagPeriods
            #
            #
            # m_affectsLicenceLevelSolo = Packet.m_affectsLicenceLevelSolo
            #
            # weekendStructure = expand(Packet.m_weekendStructure)
            # m_numSessionsInWeekend = Packet.m_numSessionsInWeekend
            else:
                self.skips += 1

        if packetID == 3:
            newData = self.recentPacketData.EventData
            eventStringCode = newData.m_eventStringCode
            self.participantsData = self.recentPacketData.ParticipantsData

            # print(eventStringCode)
            match eventStringCode:
                case "SSTA":
                    logText = "Session has started"
                    self.doFinalClassification = True
                    self.writeToFile(logText, eventStringCode)

                case "SEND":
                    self.getSessionDetails = True
                    self.skips = 0
                    logText = "Session has ended"
                    self.writeToFile(logText, eventStringCode)

                case "FTLP":  # only if racing
                    TempData = newData.m_eventDetails["fastestLap"]
                    vehicleIndex = self.getNameID(TempData.vehicleIdx)
                    lapTime = TempData.lapTime
                    logText = f"User {vehicleIndex} set fastest lap with [{lapTime}]"
                    self.writeToFile(logText, eventStringCode, TempData.vehicleIdx)

                case "RTMT":
                    TempData = newData.m_eventDetails["retirement"]
                    vehicleIndex = self.getNameID(TempData.vehicleIdx)
                    logText = f"User {vehicleIndex} has retired"
                    self.writeToFile(logText, eventStringCode, TempData.vehicleIdx)

                case "DRSE":
                    logText = f"DRS has been enabled"
                    self.writeToFile(logText, eventStringCode)

                case "DRSD":
                    logText = f"DRS has been disabled"
                    self.writeToFile(logText, eventStringCode)

                case "TMPT":
                    TempData = newData.m_eventDetails["teamMateInPits"]
                    vehicleIndex = self.getNameID(TempData.vehicleIdx)
                    logText = f"Teammate of user {vehicleIndex} has entered the pits"
                    self.writeToFile(logText, eventStringCode, TempData.vehicleIdx)

                case "CHQF":  # only if racing
                    logText = f"Chequered flag is waving"
                    self.writeToFile(logText, eventStringCode)

                case "RCWN":  # only if racing
                    TempData = newData.m_eventDetails["raceWinner"]
                    vehicleIndex = self.getNameID(TempData.vehicleIdx)
                    logText = f"User {vehicleIndex} has won the race"
                    self.writeToFile(logText, eventStringCode, TempData.vehicleIdx)

                case "PENA":
                    TempData = newData.m_eventDetails["penalty"]
                    lapNumber = TempData.lapNum
                    vehicleIndex1 = self.getNameID(TempData.vehicleIdx)
                    penValue = f"Lap [{lapNumber}] user {vehicleIndex1}"

                    if TempData.time != 255:
                        timePenalty = TempData.time
                        penValue += f" gained [{timePenalty} sec] penalty"
                    if TempData.placesGained not in [0, 255]:
                        placesGained = TempData.placesGained
                        penValue += f" and gained [{placesGained}] places"
                    if TempData.otherVehicleIdx != 255:
                        vehicleIndex2 = self.getNameID(TempData.otherVehicleIdx)
                        penValue += f" against {vehicleIndex2}"

                    infringementType = self.getPenID(TempData.infringementType, "inf")
                    penaltyType = self.getPenID(TempData.penaltyType, "pen")
                    penValue += (
                        f" by doing {infringementType} and recieved {penaltyType}"
                    )
                    # print(penValue)
                    self.writeToFile(penValue, eventStringCode, TempData.vehicleIdx)

                case "SPTP":
                    TempData = newData.m_eventDetails["speedTrap"]
                    if bool(TempData.isOverallFastestInSession):
                        vehicleIndexOfFastestInSession = self.getNameID(
                            TempData.fastestVehicleIdxInSession
                        )
                        # vehicleIndexOfFastestInSession = TempData.fastestVehicleIdxInSession
                        fastestSpeedInSession = TempData.fastestSpeedInSession
                        logText = f"User {vehicleIndexOfFastestInSession} went fastest in the session with [{fastestSpeedInSession}] kph."
                        self.writeToFile(
                            logText,
                            eventStringCode,
                            TempData.fastestVehicleIdxInSession,
                        )
                    # if bool(TempData.isDriverFastestInSession):
                    #     print(f"user {TempData.vehicleIdx} set a faster speed with {TempData.speed} kph.")

                case "STLG":
                    TempData = newData.m_eventDetails["startLights"]
                    numberOfLight = TempData.numLights
                    logText = f"Start lights [{numberOfLight}]"
                    self.writeToFile(logText, eventStringCode)

                case "LGOT":
                    logText = f"Lights have gone out"
                    self.writeToFile(logText, eventStringCode)

                case "DTSV":
                    TempData = newData.m_eventDetails["driveThroughPenaltyServed"]
                    vehicleIndex = self.getNameID(TempData.vehicleIdx)
                    logText = f"User {vehicleIndex} is serving a drive through pen"
                    self.writeToFile(logText, eventStringCode, TempData.vehicleIdx)

                case "SGSV":
                    TempData = newData.m_eventDetails["stopGoPenaltyServed"]
                    vehicleIndex = self.getNameID(TempData.vehicleIdx)
                    logText = f"User {vehicleIndex} is serving a stop-go pen"
                    self.writeToFile(logText, eventStringCode, TempData.vehicleIdx)

                case "FLBK":
                    TempData = newData.m_eventDetails["flashback"]
                    logText = f"New session time {TempData.flashbackSessionTime}. new frame identifier {TempData.flashbackFrameIdentifier}"
                    self.writeToFile(logText, eventStringCode)

                case "BUTN":
                    pass

                case "RDFL":
                    logText = f"Red flag has been shown"
                    self.writeToFile(logText, eventStringCode)

                case "OVTK":

                    def newOvertake(overtakeData):
                        overtakingVehicleIndex = self.getNameID(
                            overtakeData.overtakingVehicleIdx
                        )
                        beingOvertakenVehicleIndex = self.getNameID(
                            overtakeData.beingOvertakenVehicleIdx
                        )
                        logText = f"User {overtakingVehicleIndex} has overtaken {beingOvertakenVehicleIndex}"
                        self.writeToFile(
                            logText, eventStringCode, overtakeData.overtakingVehicleIdx
                        )

                    TempData = newData.m_eventDetails["overtake"]
                    sessionDetails = self.recentPacketData.SessionData
                    if not sessionDetails:
                        self.backLog.append(TempData)
                    else:
                        for eventBackLog in self.backLog:
                            if sessionDetails.m_sessionType not in [9, 14]:
                                newOvertake(TempData)
                            self.backLog.remove(eventBackLog)
                        if sessionDetails.m_sessionType not in [9, 14]:
                            newOvertake(TempData)

                case "SCAR":
                    TempData = newData.m_eventDetails["safetyCar"]
                    safetyCarType = self.getSCID(TempData.safetyCarType, "sc")
                    eventType = self.getSCID(TempData.eventType, "evt")
                    logText = f"{safetyCarType} is {eventType}"
                    self.writeToFile(logText, eventStringCode)

                case "COLL":
                    TempData = newData.m_eventDetails["collision"]
                    vehicleIndex1 = self.getNameID(TempData.vehicle1Idx)
                    vehicleIndex2 = self.getNameID(TempData.vehicle2Idx)
                    logText = f"Collision between user {vehicleIndex1} and user {vehicleIndex2}"
                    self.writeToFile(logText, eventStringCode, TempData.vehicle1Idx)

                case _:
                    print("------- invalid event string code --------------")
