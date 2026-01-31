import sys
from Appendices2 import *

def expand(packet, tyre=False):
    tempList=[]
    tempDict={}
    tyres = ["RL", "RR", "FL", "FR"]
    if tyre:
        for x in range(len(packet)):
            name = f"{tyre}_{tyres[x]}"
            tempDict[name] = round(packet[x],5)
        return tempDict
    else:
        for x in range(len(packet)):
            tempList.append(packet[x])

        return tempList

def split(value):
    involved=[]
    lst = [1]
    while len(lst) <= 31:
        lst.append(int(lst[-1:][0])*2)
    for x in reversed(lst):
        newValue=value-x
        if value-x<0:
            continue
        value=newValue
        involved.append(x)
    if involved:
        return involved
    return [0]

def ingest_Header(header):
    data = {"m_packetFormat":header.m_packetFormat,
            "m_gameYear":header.m_gameYear,
            "m_gameMajorVersion":header.m_gameMajorVersion,
            "m_gameMinorVersion":header.m_gameMinorVersion,
            "m_packetVersion":header.m_packetVersion,
            "m_packetId":header.m_packetId,
            "m_sessionUID":header.m_sessionUID,
            "m_sessionTime":round(header.m_sessionTime,5),
            "m_frameIdentifier":header.m_frameIdentifier,
            "m_overallFrameIdentifier":header.m_overallFrameIdentifier,
            "m_playerCarIndex":header.m_playerCarIndex,
            "m_secondaryPlayerCarIndex":header.m_secondaryPlayerCarIndex
            }
    return data

def ingest_MotionData(Packet, m_header):
    m_header=ingest_Header(m_header)
    carMotionData=expand(Packet.m_carMotionData)
    allCarData=[]
    for x in carMotionData:
        motionData = {
                "m_worldPositionX":round(x.m_worldPositionX,5),
                "m_worldPositionY":round(x.m_worldPositionY,5),
                "m_worldPositionZ":round(x.m_worldPositionZ,5),
                "m_worldVelocityX":round(x.m_worldVelocityX,5),
                "m_worldVelocityY":round(x.m_worldVelocityY,5),
                "m_worldVelocityZ":round(x.m_worldVelocityZ,5),
                "m_worldForwardDirX":x.m_worldForwardDirX,
                "m_worldForwardDirY":x.m_worldForwardDirY,
                "m_worldForwardDirZ":x.m_worldForwardDirZ,
                "m_worldRightDirX":x.m_worldRightDirX,
                "m_worldRightDirY":x.m_worldRightDirY,
                "m_worldRightDirZ":x.m_worldRightDirZ,
                "m_gForceLateral":round(x.m_gForceLateral,5),
                "m_gForceLongitudinal":round(x.m_gForceLongitudinal,5),
                "m_gForceVertical":round(x.m_gForceVertical,5),
                "m_yaw":round(x.m_yaw,5),
                "m_pitch":round(x.m_pitch,5),
                "m_roll":round(x.m_roll,5)}
        allCarData.append(motionData)
    data = {"m_header":m_header,
            "m_carMotionData":allCarData}
    return data

def ingest_sessiondata(Packet, m_header):
    m_header=ingest_Header(m_header)
    marshalZones=expand(Packet.m_marshalZones)
    weatherForecastSample=expand(Packet.m_weatherForecastSamples)
    allMarshalZones=[]
    for x in marshalZones:
        marshalZone = {
                "m_zoneStart":round(x.m_zoneStart,5),
                "m_zoneFlag":x.m_zoneFlag}
        allMarshalZones.append(marshalZone)
    allWeatherSamples=[]
    for x in weatherForecastSample:
        weatherSample = {
                "m_sessionType":x.m_sessionType,
                "m_timeOffset":x.m_timeOffset,
                "m_weather":x.m_weather,
                "m_trackTemperature":x.m_trackTemperature,
                "m_trackTemperatureChange":x.m_trackTemperatureChange,
                "m_airTemperature":x.m_airTemperature,
                "m_airTemperatureChange":x.m_airTemperatureChange,
                "m_rainPercentage":x.m_rainPercentage}
        allWeatherSamples.append(weatherSample)
    data = {"m_header":m_header,
            "m_weather":Packet.m_weather,
            "m_trackTemperature":Packet.m_trackTemperature,
            "m_airTemperature":Packet.m_airTemperature,
            "m_totalLaps":Packet.m_totalLaps,
            "m_trackLength":Packet.m_trackLength,
            "m_sessionType":Packet.m_sessionType,
            "m_trackId":Packet.m_trackId,
            "m_formula":Packet.m_formula,
            "m_sessionTimeLeft":Packet.m_sessionTimeLeft,
            "m_sessionDuration":Packet.m_sessionDuration,
            "m_pitSpeedLimit":Packet.m_pitSpeedLimit,
            "m_gamePaused":Packet.m_gamePaused,
            "m_isSpectating":Packet.m_isSpectating,
            "m_spectatorCarIndex":Packet.m_spectatorCarIndex,
            "m_sliProNativeSupport":Packet.m_sliProNativeSupport,
            "m_numMarshalZones":Packet.m_numMarshalZones,
            "m_marshalZones":allMarshalZones,
            "m_safetyCarStatus":Packet.m_safetyCarStatus,
            "m_networkGame":Packet.m_networkGame,
            "m_numWeatherForecastSamples":Packet.m_numWeatherForecastSamples,
            "m_weatherForecastSamples":allWeatherSamples,
            "m_forecastAccuracy":Packet.m_forecastAccuracy,
            "m_aiDifficulty":Packet.m_aiDifficulty,
            "m_seasonLinkIdentifier":Packet.m_seasonLinkIdentifier,
            "m_weekendLinkIdentifier":Packet.m_weekendLinkIdentifier,
            "m_sessionLinkIdentifier":Packet.m_sessionLinkIdentifier,
            "m_pitStopWindowIdealLap":Packet.m_pitStopWindowIdealLap,
            "m_pitStopWindowLatestLap":Packet.m_pitStopWindowLatestLap,
            "m_pitStopRejoinPosition":Packet.m_pitStopRejoinPosition,
            "m_steeringAssist":Packet.m_steeringAssist,
            "m_brakingAssist":Packet.m_brakingAssist,
            "m_gearboxAssist":Packet.m_gearboxAssist,
            "m_pitAssist":Packet.m_pitAssist,
            "m_pitReleaseAssist":Packet.m_pitReleaseAssist,
            "m_ersAssist":Packet.m_ersAssist,
            "m_drsAssist":Packet.m_drsAssist,
            "m_dynamicRacingLine":Packet.m_dynamicRacingLine,
            "m_dynamicRacingLineType":Packet.m_dynamicRacingLineType,
            "m_gameMode":Packet.m_gameMode,
            "m_ruleSet":Packet.m_ruleSet,
            "m_timeOfDay":Packet.m_timeOfDay,
            "m_sessionLength":Packet.m_sessionLength,
            "m_speedUnitsLeadPlayer":Packet.m_speedUnitsLeadPlayer,
            "m_temperatureUnitsLeadPlayer":Packet.m_temperatureUnitsLeadPlayer,
            "m_speedUnitsSecondaryPlayer":Packet.m_speedUnitsSecondaryPlayer,
            "m_temperatureUnitsSecondaryPlayer":Packet.m_temperatureUnitsSecondaryPlayer,
            "m_numSafetyCarPeriods":Packet.m_numSafetyCarPeriods,
            "m_numVirtualSafetyCarPeriods":Packet.m_numVirtualSafetyCarPeriods,
            "m_numRedFlagPeriods":Packet.m_numRedFlagPeriods}
    return data

def ingest_lapdata(Packet, m_header):
    m_header=ingest_Header(m_header)
    lapData=expand(Packet.m_lapData)
    allLapData=[]
    for x in lapData:
        lap = {"m_lastLapTimeInMs":x.m_lastLapTimeInMs/1000,
                "m_currentLapTimeInMs":x.m_currentLapTimeInMs/1000,
                "m_sector1TimeInMs":x.m_sector1TimeInMs/1000,
                "m_sector1TimeMinutes":x.m_sector1TimeInMinutes,
                "m_sector2TimeInMs":x.m_sector2TimeInMs/1000,
                "m_sector2TimeMinutes":x.m_sector2TimeInMinutes,
                "m_deltaToCarInFrontInMS":x.m_deltaToCarInFrontInMS/1000,
                "m_deltaToRaceLeaderInMS":x.m_deltaToRaceLeaderInMS/1000,
                "m_lapDistance":round(x.m_lapDistance,5),
                "m_totalDistance":round(x.m_totalDistance,5),
                "m_safetyCarDelta":x.m_safetyCarDelta,
                "m_car_position":x.m_car_position,
                "m_currentLapNum":x.m_currentLapNum,
                "m_pitStatus":x.m_pitStatus,
                "m_numPitStops":x.m_numPitStops,
                "m_sector":x.m_sector,
                "m_currentLapInvalid":x.m_currentLapInvalid,
                "m_penalties":x.m_penalties,
                "m_totalWarnings":x.m_totalWarnings,
                "m_numUnservedDriveThroughPens":x.m_numUnservedDriveThroughPens,
                "m_numUnservedStopGoPens":x.m_numUnservedStopGoPens,
                "m_gridPosition":x.m_gridPosition,
                "m_driverStatus":x.m_driverStatus,
                "m_resultStatus":x.m_resultStatus,
                "m_pitLaneTimerActive":x.m_pitLaneTimerActive,
                "m_pitLaneTimeInLaneInMs":x.m_pitLaneTimeInLaneInMs/1000,
                "m_pitStopTimerInMs":x.m_pitStopTimerInMs/1000,
                "m_pitStopShouldServePen":x.m_pitStopShouldServePen}
        allLapData.append(lap)
    data = {"m_header":m_header,
            "m_lapData":allLapData,
            "m_timeTrialPBCarIdx":Packet.m_timeTrialPBCarIdx,
            "m_timeTrialRivalCarIdx":Packet.m_timeTrialRivalCarIdx}
    return data

def ingest_eventdata(Packet,m_header):
    m_header=ingest_Header(m_header)
    eventStringCode=[]
    for x in Packet.m_eventStringCode:
        eventStringCode.append(chr(x))
    eventStringCode="".join(eventStringCode)
    fastestLapData = Packet.m_eventDetails.fastestLap
    retirementData = Packet.m_eventDetails.retirement
    teammatePitData = Packet.m_eventDetails.teamMateInPits
    winnerData = Packet.m_eventDetails.raceWinner
    penaltyData = Packet.m_eventDetails.penalty
    speedTrapData = Packet.m_eventDetails.speedTrap
    startLightsData = Packet.m_eventDetails.startLights
    driveThroughData = Packet.m_eventDetails.driveThroughPenaltyServed
    stopGoData = Packet.m_eventDetails.stopGoPenaltyServed
    flashbackData = Packet.m_eventDetails.flashback
    buttonsData = Packet.m_eventDetails.buttons
    overtakeData = Packet.m_eventDetails.overtake

    if eventStringCode == "FTLP":
        eventDetailData = {"fastestLap":{"vehicleIdx":fastestLapData.vehicleIdx,
                                            "lapTime":round(fastestLapData.lapTime,3)}}
    elif eventStringCode == "RTMT":
        eventDetailData = {"retirement":{"vehicleIdx":retirementData.vehicleIdx}}
    elif eventStringCode == "TMPT":
        eventDetailData = {"teamMateInPits":{"vehicleIdx":teammatePitData.vehicleIdx}}
    elif eventStringCode == "RCWN":
        eventDetailData = {"raceWinner":{"vehicleIdx":winnerData.vehicleIdx}}
    elif eventStringCode == "PENA":
        eventDetailData = {"penalty":{"penaltyType":penaltyData.penaltyType,
                                        "infringementType":penaltyData.infringementType,
                                        "vehicleIdx":penaltyData.vehicleIdx,
                                        "otherVehicleIdx":penaltyData.otherVehicleIdx,
                                        "time":penaltyData.time,
                                        "lapNum":penaltyData.lapNum,
                                        "placesGained":penaltyData.placesGained}}
    elif eventStringCode == "SPTP":
        eventDetailData = {"speedTrap":{"vehicleIdx":speedTrapData.vehicleIdx,
                                        "speed":round(speedTrapData.speed,3),
                                        "isOverallFastestInSession":speedTrapData.isOverallFastestInSession,
                                        "isDriverFastestInSession":speedTrapData.isDriverFastestInSession,
                                        "fastestVehicleIdxInSession":speedTrapData.fastestVehicleIdxInSession,
                                        "fastestSpeedInSession":round(speedTrapData.fastestSpeedInSession,3)}}
    elif eventStringCode == "STLG":
        eventDetailData = {"startLights":{"numLights":startLightsData.numLights}}
    elif eventStringCode == "DTSV":
        eventDetailData = {"driveThroughPenaltyServed":{"vehicleIdx":driveThroughData.vehicleIdx}}
    elif eventStringCode == "SGSV":
        eventDetailData = {"stopGoPenaltyServed":{"vehicleIdx":stopGoData.vehicleIdx}}
    elif eventStringCode == "FLBK":
        eventDetailData = {"flashback":{"flashbackFrameIdentifier":flashbackData.flashbackFrameIdentifier,
                                        "flashbackSessionTime":flashbackData.flashbackSessionTime}}
    elif eventStringCode == "BUTN":
        eventDetailData = {"buttons":{"m_buttonStatus":[]}}
        for x in split(buttonsData.m_buttonStatus):
            eventDetailData['buttons']['m_buttonStatus'].append(x)
    elif eventStringCode == "OVTK":
        eventDetailData = {"overtake":{"overtakingVehicleIdx":overtakeData.overtakingVehicleIdx,
                                        "beingOvertakenVehicleIdx":overtakeData.beingOvertakenVehicleIdx}}
    else:
        eventDetailData = {"other":"True"}

    data = {"m_header":m_header,
            "m_eventStringCode":eventStringCode,
            "m_eventDetails":eventDetailData}
    return data

def ingest_participantsdata(Packet,m_header):
    m_header=ingest_Header(m_header)
    allParticipantsData=[]
    for x in Packet.m_participants:
        newName=[]
        name = expand(x.m_name)
        for i in name:
            newName.append(chr(i))
        name = "".join(newName)
        participantsData = {"m_aiControlled":x.m_aiControlled,
                            "m_driverId":x.m_driverId,
                            "m_networkId":x.m_networkId,
                            "m_teamId":x.m_teamId,
                            "m_myTeam":x.m_myTeam,
                            "m_raceNumber":x.m_raceNumber,
                            "m_nationality":x.m_nationality,
                            "m_name":name,
                            "m_yourTelemetry":x.m_yourTelemetry,
                            "m_showOnlineNames":x.m_showOnlineNames,
                            "m_platform":x.m_platform}
        allParticipantsData.append(participantsData)
    data = {"m_header":m_header,
            "m_numActiveCars":Packet.m_numActiveCars,
            "m_participants":allParticipantsData}
    return data

def ingest_carsetupdata(Packet,m_header):
    m_header=ingest_Header(m_header)
    allCarSetupData=[]
    for x in Packet.m_car_setups:
        carSetupData = {"m_frontWing":x.m_frontWing,
                        "m_rearWing":x.m_rearWing,
                        "m_onThrottle":x.m_onThrottle,
                        "m_offThrottle":x.m_offThrottle,
                        "m_frontCamber":x.m_frontCamber,
                        "m_rearCamber":x.m_rearCamber,
                        "m_frontToe":round(x.m_frontToe,2),
                        "m_rearToe":round(x.m_rearToe,2),
                        "m_frontSuspension":x.m_frontSuspension,
                        "m_rearSuspension":x.m_rearSuspension,
                        "m_frontAntiRollBar":x.m_frontAntiRollBar,
                        "m_rearAntiRollBar":x.m_rearAntiRollBar,
                        "m_frontSuspensionHeight":x.m_frontSuspensionHeight,
                        "m_rearSuspensionHeight":x.m_rearSuspensionHeight,
                        "m_brakePressure":x.m_brakePressure,
                        "m_brakeBias":x.m_brakeBias,
                        "m_rearLeftTyrePressure":x.m_rearLeftTyrePressure,
                        "m_rearRightTyrePressure":x.m_rearRightTyrePressure,
                        "m_frontLeftTyrePressure":round(x.m_frontLeftTyrePressure,5),
                        "m_frontRightTyrePressure":round(x.m_frontRightTyrePressure,5),
                        "m_ballast":x.m_ballast,
                        "m_fuelLoad":x.m_fuelLoad}
        allCarSetupData.append(carSetupData)
    data = {"m_header":m_header,
            "m_car_setups":allCarSetupData}
    return data

def ingest_cartelemetrydata(Packet,m_header):
    m_header=ingest_Header(m_header)
    allCarTelemetryData=[]
    for x in Packet.m_carTelemetryData:
        carTelemetryData = {"m_speed":x.m_speed,
                            "m_throttle":round(x.m_throttle,5),
                            "m_steer":round(x.m_steer,5),
                            "m_brake":round(x.m_brake,5),
                            "m_clutch":x.m_clutch,
                            "m_gear":x.m_gear,
                            "m_engineRpm":x.m_engineRpm,
                            "m_drs":x.m_drs,
                            "m_revLightsPercent":x.m_revLightsPercent,
                            "m_revLightsBitValue":x.m_revLightsBitValue,
                            "m_brakesTemperature":expand(x.m_brakesTemperature),
                            "m_tyresSurfaceTemperature":expand(x.m_tyresSurfaceTemperature),
                            "m_tyresInnerTemperature":expand(x.m_tyresInnerTemperature),
                            "m_engineTemperature":x.m_engineTemperature,
                            "m_tyresPressure":expand(x.m_tyresPressure),
                            "m_surfaceType":expand(x.m_surfaceType)}

        # carTelemetryData.update(expand(x.m_brakesTemperature,"m_brakesTemperature"))
        # carTelemetryData.update(expand(x.m_tyresSurfaceTemperature,"m_tyresSurfaceTemperature"))
        # carTelemetryData.update(expand(x.m_tyresInnerTemperature,"m_tyresInnerTemperature"))
        # carTelemetryData.update(expand(x.m_tyresPressure,"m_tyresPressure"))
        # carTelemetryData.update(expand(x.m_surfaceType,"m_surfaceType"))

        allCarTelemetryData.append(carTelemetryData)
    data = {"m_header":m_header,
            "m_carTelemetryData":allCarTelemetryData,
            "m_mfdPanelIndex":Packet.m_mfdPanelIndex,
            "m_mfdPanelIndexSecondaryPlayer":Packet.m_mfdPanelIndexSecondaryPlayer,
            "m_suggestedGear":Packet.m_suggestedGear}
    return data

def ingest_carstatusdata(Packet,m_header):
    m_header=ingest_Header(m_header)
    allCarStatusData=[]
    for x in Packet.m_carStatusData:
        carStatusData = {"m_tractionControl":x.m_tractionControl,
                        "m_antiLockBrakes":x.m_antiLockBrakes,
                        "m_fuelMix":x.m_fuelMix, # hidden
                        "m_frontBrakeBias":x.m_frontBrakeBias, # hidden
                        "m_pitLimiterStatus":x.m_pitLimiterStatus,
                        "m_fuelInTank":round(x.m_fuelInTank,5), # hidden
                        "m_fuelCapacity":x.m_fuelCapacity, # hidden
                        "m_fuelRemainingLaps":round(x.m_fuelRemainingLaps,5), # hidden
                        "m_maxRpm":x.m_maxRpm,
                        "m_idleRpm":x.m_idleRpm,
                        "m_maxGears":x.m_maxGears,
                        "m_drsAllowed":x.m_drsAllowed,
                        "m_drsActivationDistance":x.m_drsActivationDistance,
                        "m_actualTyreCompound":x.m_actualTyreCompound,
                        "m_visualTyreCompound":x.m_visualTyreCompound,
                        "m_tyresAgeLaps":x.m_tyresAgeLaps,
                        "m_vehicleFiaFlags":x.m_vehicleFiaFlags,
                        "m_enginePowerICE":round(x.m_enginePowerICE,5),
                        "m_enginePowerMGUK":round(x.m_enginePowerMGUK,5),
                        "m_ersStoreEnergy":x.m_ersStoreEnergy, # hidden
                        "m_ersDeployMode":x.m_ersDeployMode, # hidden
                        "m_ersHarvestedThisLapMguk":round(x.m_ersHarvestedThisLapMguk,5), # hidden
                        "m_ersHarvestedThisLapMguh":round(x.m_ersHarvestedThisLapMguh,5), # hidden
                        "m_ersDeployedThisLap":round(x.m_ersDeployedThisLap,5), # hidden
                        "m_networkPaused":x.m_networkPaused}
        allCarStatusData.append(carStatusData)
    data = {"m_header":m_header,
            "m_carStatusData":allCarStatusData}
    return data

def ingest_finalclassificationdata(Packet,m_header,mode):
    m_header=ingest_Header(m_header)
    allClassificationData=[]
    for x in Packet.m_classificationData:
        classificationData = {"m_sessionType":mode,
                            "m_position":x.m_position,
                            "m_numLaps":x.m_numLaps,
                            "m_gridPosition":x.m_gridPosition,
                            "m_points":x.m_points,
                            "m_numPitStops":x.m_numPitStops,
                            "m_resultStatus":x.m_resultStatus,
                            "m_bestLapTimeInMs":x.m_bestLapTimeInMs/1000,
                            "m_totalRaceTime":round(x.m_totalRaceTime,5),
                            "m_penaltiesTime":x.m_penaltiesTime,
                            "m_numPenalties":x.m_numPenalties,
                            "m_numTyreStints":x.m_numTyreStints,
                            "m_tyreStintsActual":expand(x.m_tyreStintsActual),
                            "m_tyreStintsVisual":expand(x.m_tyreStintsVisual),
                            "tyreStintsEndLaps":expand(x.tyreStintsEndLaps)}
        allClassificationData.append(classificationData)
    data = {"m_header":m_header,
            "m_numCars":Packet.m_numCars,
            "m_classificationData":allClassificationData}
    return data

def ingest_lobbyinfodata(Packet,m_header):
    m_header=ingest_Header(m_header)
    allLobbyInfoData=[]
    for x in Packet.m_lobbyPlayers:
        newName=[]
        name = expand(x.m_name)
        for i in name:
            newName.append(chr(i))
        name = "".join(newName)
        lobbyInfoData = {"m_aiControlled":x.m_aiControlled,
                            "m_teamId":x.m_teamId,
                            "m_nationality":x.m_nationality,
                            "m_platform":x.m_platform,
                            "m_name":name,
                            "m_carNumber":x.m_carNumber,
                            "m_readyStatus":x.m_readyStatus}
        allLobbyInfoData.append(lobbyInfoData)
    data = {"m_header":m_header,
            "m_numPlayers":Packet.m_numPlayers,
            "m_lobbyPlayers":allLobbyInfoData}
    return data

def ingest_cardamagedata(Packet,m_header):
    m_header=ingest_Header(m_header)
    allCarDamageData=[]
    for x in Packet.m_carDamageData:
        carDamageData = {"m_tyresWear":expand(x.m_tyresWear),
                            "m_tyresDamage":expand(x.m_tyresDamage),
                            "m_brakesDamage":expand(x.m_brakesDamage),
                            "m_frontLeftWingDamage":x.m_frontLeftWingDamage, # hidden
                            "m_frontRightWingDamage":x.m_frontRightWingDamage, # hidden
                            "m_rearWingDamage":x.m_rearWingDamage, # hidden
                            "m_floorDamage":x.m_floorDamage, # hidden
                            "m_diffuserDamage":x.m_diffuserDamage, # hidden
                            "m_sidepodDamage":x.m_sidepodDamage, # hidden
                            "m_drsFault":x.m_drsFault, # hidden
                            "m_ersFault":x.m_ersFault,
                            "m_gearBoxDamage":x.m_gearBoxDamage, # hidden
                            "m_engineDamage":x.m_engineDamage, # hidden
                            "m_engineMguhwear":x.m_engineMguhwear, # hidden
                            "m_engineEswear":x.m_engineEswear, # hidden
                            "m_engineCewear":x.m_engineCewear, # hidden
                            "m_engineIcewear":x.m_engineIcewear, # hidden
                            "m_engineMgukwear":x.m_engineMgukwear, # hidden
                            "m_engineTcwear":x.m_engineTcwear, # hidden
                            "m_engineBlown":x.m_engineBlown,
                            "m_engineSeized":x.m_engineSeized}

        # carDamageData.update(expand(x.m_tyresWear,"m_tyresWear")) # hidden
        # carDamageData.update(expand(x.m_tyresDamage,"m_tyresDamage")) # hidden
        # carDamageData.update(expand(x.m_brakesDamage,"m_brakesDamage")) # hidden

        allCarDamageData.append(carDamageData)
    data = {"m_header":m_header,
            "m_carDamageData":allCarDamageData}
    return data

def ingest_sessionhistorydata(Packet,m_header):
    m_header=ingest_Header(m_header)
    allLapHistoryData=[]
    allTyreStintHistoryData=[]
    for x in Packet.m_lapHistoryData:
        lapHistoryData = {"m_lapTimeInMs":x.m_lapTimeInMs/1000,
                            "m_sector1TimeInMs":x.m_sector1TimeInMs/1000,
                            "m_sector1TimeMinutes":x.m_sector1TimeMinutes,
                            "m_sector2TimeInMs":x.m_sector2TimeInMs/1000,
                            "m_sector2TimeMinutes":x.m_sector2TimeMinutes,
                            "m_sector3TimeInMs":x.m_sector3TimeInMs/1000,
                            "m_sector3TimeMinutes":x.m_sector3TimeMinutes,
                            "m_lapValidBitFlags":x.m_lapValidBitFlags}
        allLapHistoryData.append(lapHistoryData)
    for x in Packet.m_tyreStintsHistoryData:
        tyreStintHistoryData = {"m_endLap":x.m_endLap,
                            "m_tyreActualCompound":x.m_tyreActualCompound,
                            "m_tyreVisualCompound":x.m_tyreVisualCompound}
        allTyreStintHistoryData.append(tyreStintHistoryData)
    data = {"m_header":m_header,
            "m_carIdx":Packet.m_carIdx,
            "m_numLaps":Packet.m_numLaps,
            "m_numTyreStints":Packet.m_numTyreStints,
            "m_bestLapTimeLapNum":Packet.m_bestLapTimeLapNum,
            "m_bestSector1LapNum":Packet.m_bestSector1LapNum,
            "m_bestSector2LapNum":Packet.m_bestSector2LapNum,
            "m_bestSector3LapNum":Packet.m_bestSector3LapNum,
            "m_lapHistoryData":allLapHistoryData,
            "m_tyreStintsHistoryData":allTyreStintHistoryData}
    return data

def ingest_tyresetdata(Packet,m_header):
    m_header=ingest_Header(m_header)
    allTyreSetData=[]
    for x in Packet.m_tyreSetData:
        tyreSetData = {"m_actualTyreCompound":x.m_actualTyreCompound,
                       "m_visualTyreCompound":x.m_visualTyreCompound,
                       "m_wear":x.m_wear,
                       "m_available":x.m_available,
                       "m_recommendedSession":x.m_recommendedSession,
                       "m_lifeSpan":x.m_lifeSpan,
                       "m_usableLife":x.m_usableLife,
                       "m_lapDeltaTime":x.m_lapDeltaTime,
                       "m_fitted":x.m_fitted}

        allTyreSetData.append(tyreSetData)
    data = {"m_header":m_header,
            "m_carIdx":Packet.m_carIdx,
            "m_tyreSetData":allTyreSetData,
            "m_fittedIdx":Packet.m_fittedIdx}
    return data

def ingest_motionexdata(Packet, m_header):
    m_header=ingest_Header(m_header)
    data = {"m_header":m_header,
            "m_suspensionPosition":expand(Packet.m_suspensionPosition),
            "m_suspensionVelocity":expand(Packet.m_suspensionVelocity),
            "m_suspensionAcceleration":expand(Packet.m_suspensionAcceleration),
            "m_wheelSpeed":expand(Packet.m_wheelSpeed),
            "m_wheelSlipRatio":expand(Packet.m_wheelSlipRatio),
            "m_wheelSlipAngle":expand(Packet.m_wheelSlipAngle),
            "m_wheelLatForce":expand(Packet.m_wheelLatForce),
            "m_wheelLongForce":expand(Packet.m_wheelLongForce),
            "m_heightOfCOGAboveGround":Packet.m_heightOfCOGAboveGround,
            "m_localVelocityX":Packet.m_localVelocityX,
            "m_localVelocityY":Packet.m_localVelocityY,
            "m_localVelocityZ":Packet.m_localVelocityZ,
            "m_angularVelocityX":Packet.m_angularVelocityX,
            "m_angularVelocityY":Packet.m_angularVelocityY,
            "m_angularVelocityZ":Packet.m_angularVelocityZ,
            "m_angularAccelerationX":Packet.m_angularAccelerationX,
            "m_angularAccelerationY":Packet.m_angularAccelerationY,
            "m_angularAccelerationZ":Packet.m_angularAccelerationZ,
            "m_frontWheelsAngle":Packet.m_frontWheelsAngle,
            "m_wheelVertForce":expand(Packet.m_wheelVertForce)}
    return data




