import ctypes

def to_json(*args, **kwargs):
    kwargs.setdefault('indent', 2)
    kwargs['sort_keys'] = True
    kwargs['ensure_ascii'] = False
    kwargs['separators'] = (',', ': ')
    return json.dumps(*args, **kwargs)

class PacketMixin():
    def get_value(self, field):
        return self._format_type(getattr(self, field))

    def pack(self):
        return bytes(self)

    @classmethod
    def size(cls):
        return ctypes.sizeof(cls)

    @classmethod
    def unpack(cls, buffer):
        return cls.from_buffer_copy(buffer)

    def to_dict(self):
        return {k: self.get_value(k) for k, _ in self._fields_}

    def to_json(self):
        return to_json(self.to_dict())

    def _format_type(self, value):
        class_name = type(value).__name__
        if class_name == 'float':
            return round(value, 3)
        if class_name == 'bytes':
            return value.decode()
        if isinstance(value, ctypes.Array):
            return self._format_array_type(value)
        if hasattr(value, 'to_dict'):
            return value.to_dict()
        return value

    def _format_array_type(self, value):
        results = []
        for item in value:
            if isinstance(item, Packet):
                results.append(item.to_dict())
            else:
                results.append(item)
        return results

class Packet(ctypes.LittleEndianStructure, PacketMixin):
    _pack_ = 1
    def __repr__(self):
        return self.to_json()

### Packet Header

class PacketHeader(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_packetFormat',              ctypes.c_uint16), # 2023
        ('m_gameYear',                  ctypes.c_uint8),  # Game year - last two digits e.g. 23
        ('m_gameMajorVersion',          ctypes.c_uint8),  # Game major version - "X.00"
        ('m_gameMinorVersion',          ctypes.c_uint8),  # Game minor version - "1.XX"
        ('m_packetVersion',             ctypes.c_uint8),  # Version of this packet type, all start from 1
        ('m_packetId',                  ctypes.c_uint8),  # Identifier for the packet type, see below
        ('m_sessionUID',                ctypes.c_uint64), # Unique identifier for the session
        ('m_sessionTime',               ctypes.c_float),  # Session timestamp
        ('m_frameIdentifier',           ctypes.c_uint32), # Identifier for the frame the data was retrieved on
        ('m_overallFrameIdentifier',    ctypes.c_uint32), # Overall identifier for the frame the data was retrieved on, doesn't go back after flashbacks
        ('m_playerCarIndex',            ctypes.c_uint8),  # Index of player's car in the array
        ('m_secondaryPlayerCarIndex',   ctypes.c_uint8),  # Index of secondary player's car in the array (splitscreen), 255 if no second player
    ]

### Motion Packet -- Rate as specified in menus -- 1349 bytes

class CarMotionData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_worldPositionX',        ctypes.c_float), # World space X position
        ('m_worldPositionY',        ctypes.c_float), # World space Y position
        ('m_worldPositionZ',        ctypes.c_float), # World space Z position
        ('m_worldVelocityX',        ctypes.c_float), # Velocity in world space X
        ('m_worldVelocityY',        ctypes.c_float), # Velocity in world space Y
        ('m_worldVelocityZ',        ctypes.c_float), # Velocity in world space Z
        ('m_worldForwardDirX',      ctypes.c_int16), # World space forward X direction (normalised)
        ('m_worldForwardDirY',      ctypes.c_int16), # World space forward Y direction (normalised)
        ('m_worldForwardDirZ',      ctypes.c_int16), # World space forward Z direction (normalised)
        ('m_worldRightDirX',        ctypes.c_int16), # World space right X direction (normalised)
        ('m_worldRightDirY',        ctypes.c_int16), # World space right Y direction (normalised)
        ('m_worldRightDirZ',        ctypes.c_int16), # World space right Z direction (normalised)
        ('m_gForceLateral',         ctypes.c_float), # Lateral G-Force component
        ('m_gForceLongitudinal',    ctypes.c_float), # Longitudinal G-Force component
        ('m_gForceVertical',        ctypes.c_float), # Vertical G-Force component
        ('m_yaw',                   ctypes.c_float), # Yaw angle in radians
        ('m_pitch',                 ctypes.c_float), # Pitch angle in radians
        ('m_roll',                  ctypes.c_float), # Roll angle in radians
    ]

class PacketMotionData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header',            PacketHeader),       # Header
        ('m_carMotionData',     CarMotionData * 22), # Data for all cars on track
    ]

### Session Packet -- 2 per second -- 753 bytes

class MarshalZone(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_zoneStart',     ctypes.c_float), # Fraction (0..1) of way through the lap the marshal zone starts
        ('m_zoneFlag',      ctypes.c_int8),  # ZoneFlag in Appendices1
    ]

class WeatherForecastSample(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_sessionType',               ctypes.c_uint8), # SessionType in Appendices1
        ('m_timeOffset',                ctypes.c_uint8), # Time in minutes the forecast is for
        ('m_weather',                   ctypes.c_uint8), # Weather in Appendices1
        ('m_trackTemperature',          ctypes.c_int8),  # Track temp. in degrees Celsius
        ('m_trackTemperatureChange',    ctypes.c_int8),  # Track temp. TempChange in Appendices1
        ('m_airTemperature',            ctypes.c_int8),  # Air temp. in degrees celsius
        ('m_airTemperatureChange',      ctypes.c_int8),  # Air temp. TempChange in Appendices1
        ('m_rainPercentage',            ctypes.c_uint8), # Rain percentage (0-100)
    ]

class PacketSessionData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header',                            PacketHeader),               # Header

        ('m_weather',                           ctypes.c_uint8),             # Weather in Appendices1

        ('m_trackTemperature',                  ctypes.c_int8),              # Track temp. in degrees celsius
        ('m_airTemperature',                    ctypes.c_int8),              # Air temp. in degrees celsius
        ('m_totalLaps',                         ctypes.c_uint8),             # Total number of laps in this race
        ('m_trackLength',                       ctypes.c_uint16),            # Track length in metres
        ('m_sessionType',                       ctypes.c_uint8),             # SessionType in Appendices1
        ('m_trackId',                           ctypes.c_int8),              # Tracks in Appendices2
        ('m_formula',                           ctypes.c_uint8),             # FormulaType in Appendices1

        ('m_sessionTimeLeft',                   ctypes.c_uint16),            # Time left in session in seconds
        ('m_sessionDuration',                   ctypes.c_uint16),            # Session duration in seconds
        ('m_pitSpeedLimit',                     ctypes.c_uint8),             # Pit speed limit in kilometres per hour
        ('m_gamePaused',                        ctypes.c_uint8),             # Whether the game is paused
        ('m_isSpectating',                      ctypes.c_uint8),             # Whether the player is spectating
        ('m_spectatorCarIndex',                 ctypes.c_uint8),             # Index of the car being spectated
        ('m_sliProNativeSupport',               ctypes.c_uint8),             # SLI Pro support, Activeness in Appendices1
        ('m_numMarshalZones',                   ctypes.c_uint8),             # Number of marshal zones to follow
        ('m_marshalZones',                      MarshalZone * 21),           # List of marshal zones – max 21
        ('m_safetyCarStatus',                   ctypes.c_uint8),             # SafetyCarStatus in Appendices1

        ('m_networkGame',                       ctypes.c_uint8),             # NetworkStatus in Appendices1
        ('m_numWeatherForecastSamples',         ctypes.c_uint8),             # Number of weather samples to follow
        ('m_weatherForecastSamples',            WeatherForecastSample * 64), # Array of weather forecast samples
        ('m_forecastAccuracy',                  ctypes.c_uint8),             # ForcastAccuracy in Appendices1
        ('m_aiDifficulty',                      ctypes.c_uint8),             # AI Difficulty rating – 0-110

        ('m_seasonLinkIdentifier',              ctypes.c_uint32),            # Identifier for season - persists across saves
        ('m_weekendLinkIdentifier',             ctypes.c_uint32),            # Identifier for weekend - persists across saves
        ('m_sessionLinkIdentifier',             ctypes.c_uint32),            # Identifier for session - persists across saves
        ('m_pitStopWindowIdealLap',             ctypes.c_uint8),             # Ideal lap to pit on for current strategy (player)
        ('m_pitStopWindowLatestLap',            ctypes.c_uint8),             # Latest lap to pit on for current strategy (player)
        ('m_pitStopRejoinPosition',             ctypes.c_uint8),             # Predicted position to rejoin at (player)

        ('m_steeringAssist',                    ctypes.c_uint8),             # AssistSwitch in Appendices1
        ('m_brakingAssist',                     ctypes.c_uint8),             # BrakingAssist in Appendices1
        ('m_gearboxAssist',                     ctypes.c_uint8),             # GearboxAssist in Appendices1
        ('m_pitAssist',                         ctypes.c_uint8),             # AssistSwitch in Appendices1
        ('m_pitReleaseAssist',                  ctypes.c_uint8),             # AssistSwitch in Appendices1
        ('m_ersAssist',                         ctypes.c_uint8),             # AssistSwitch in Appendices1
        ('m_drsAssist',                         ctypes.c_uint8),             # AssistSwitch in Appendices1
        ('m_dynamicRacingLine',                 ctypes.c_uint8),             # RacinglineAssist in Appendices1
        ('m_dynamicRacingLineType',             ctypes.c_uint8),             # RacinglineType in Appendices1
        ('m_gameMode',                          ctypes.c_uint8),             # GameModes in Appendices2
        ('m_ruleSet',                           ctypes.c_uint8),             # Rulesets in Appendices2
        ('m_timeOfDay',                         ctypes.c_uint32),            # Local time of day - minutes since midnight
        ('m_sessionLength',                     ctypes.c_uint8),             # SessionLength in Appendices1

        ('m_speedUnitsLeadPlayer',              ctypes.c_uint8),             # SpeedUnits in Appendices1
        ('m_temperatureUnitsLeadPlayer',        ctypes.c_uint8),             # TempUnits in Appendices1
        ('m_speedUnitsSecondaryPlayer',         ctypes.c_uint8),             # SpeedUnits in Appendices1
        ('m_temperatureUnitsSecondaryPlayer',   ctypes.c_uint8),             # TempUnits in Appendices1
        ('m_numSafetyCarPeriods',               ctypes.c_uint8),             # Number of safety cars called during session
        ('m_numVirtualSafetyCarPeriods',        ctypes.c_uint8),             # Number of virtual safety cars called
        ('m_numRedFlagPeriods',                 ctypes.c_uint8),             # Number of red flags called during session

        ('m_equalCarPerformance',               ctypes.c_uint8),             # 0 = Off, 1 = On
        ('m_recoveryMode',                      ctypes.c_uint8),             # 0 = None, 1 = Flashbacks, 2 = Auto-recovery
        ('m_flashbackLimit',                    ctypes.c_uint8),             # 0 = Low, 1 = Medium, 2 = High, 3 = Unlimited
        ('m_surfaceType',                       ctypes.c_uint8),             # 0 = Simplified, 1 = Realistic
        ('m_lowFuelMode',                       ctypes.c_uint8),             # 0 = Easy, 1 = Hard
        ('m_raceStarts',                        ctypes.c_uint8),             # 0 = Manual, 1 = Assisted
        ('m_tyreTemperature',                   ctypes.c_uint8),             # 0 = Surface only, 1 = Surface & Carcass
        ('m_pitLaneTyreSim',                    ctypes.c_uint8),             # 0 = On, 1 = Off
        ('m_carDamage',                         ctypes.c_uint8),             # 0 = Off, 1 = Reduced, 2 = Standard, 3 = Simulation
        ('m_carDamageRate',                     ctypes.c_uint8),             # 0 = Reduced, 1 = Standard, 2 = Simulation
        ('m_collisions',                        ctypes.c_uint8),             # 0 = Off, 1 = Player-to-Player Off, 2 = On
        ('m_collisionsOffForFirstLapOnly',      ctypes.c_uint8),             # 0 = Disabled, 1 = Enabled
        ('m_mpUnsafePitRelease',                ctypes.c_uint8),             # 0 = On, 1 = Off (Multiplayer)
        ('m_mpOffForGriefing',                  ctypes.c_uint8),             # 0 = Disabled, 1 = Enabled (Multiplayer)

        ('m_cornerCuttingStringency',           ctypes.c_uint8),             # 0 = Regular, 1 = Strict
        ('m_parcFermeRules',                    ctypes.c_uint8),             # 0 = Off, 1 = On
        ('m_pitStopExperience',                 ctypes.c_uint8),             # 0 = Automatic, 1 = Broadcast, 2 = Immersive
        ('m_safetyCar',                         ctypes.c_uint8),             # 0 = Off, 1 = Reduced, 2 = Standard, 3 = Increased
        ('m_safetyCarExperience',               ctypes.c_uint8),             # 0 = Broadcast, 1 = Immersive
        ('m_formationLap',                      ctypes.c_uint8),             # 0 = Off, 1 = On
        ('m_formationLapExperience',            ctypes.c_uint8),             # 0 = Broadcast, 1 = Immersive
        ('m_redFlags',                          ctypes.c_uint8),             # 0 = Off, 1 = Reduced, 2 = Standard, 3 = Increased
        ('m_affectsLicenceLevelSolo',           ctypes.c_uint8),             # 0 = Off, 1 = On
        ('m_affectsLicenceLevelMP',             ctypes.c_uint8),             # 0 = Off, 1 = On
        ('m_numSessionsInWeekend',              ctypes.c_uint8),             # Number of session in following array
        ('m_weekendStructure',                  ctypes.c_uint8 * 12),        # List of session types to show weekend structure

        ('m_sector2LapDistanceStart',           ctypes.c_float),             # Distance in m around track where sector 2 starts
        ('m_sector3LapDistanceStart',           ctypes.c_float),             # Distance in m around track where sector 3 starts
    ]

### Lap Data Packet -- Rate as specified in menus -- 1285 bytes

class LapData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_lastLapTimeInMs',               ctypes.c_uint32), # Last lap time in milliseconds
        ('m_currentLapTimeInMs',            ctypes.c_uint32), # Current time around the lap in milliseconds
        ('m_sector1TimeInMs',               ctypes.c_uint16), # Sector 1 time in milliseconds
        ('m_sector1TimeInMinutes',          ctypes.c_uint8),  # Sector 1 whole minute part
        ('m_sector2TimeInMs',               ctypes.c_uint16), # Sector 2 time in milliseconds
        ('m_sector2TimeInMinutes',          ctypes.c_uint8),  # Sector 2 whole minute part
        ('m_deltaToCarInFrontMSPart',       ctypes.c_uint16), # Time delta to car in front milliseconds part
        ('m_deltaToCarInFrontMinutesPart',  ctypes.c_uint8),  # Time delta to car in front whole minute part
        ('m_deltaToRaceLeaderMSPart',       ctypes.c_uint16), # Time delta to race leader milliseconds part
        ('m_deltaToRaceLeaderMinutesPart',  ctypes.c_uint8),  # Time delta to race leader whole minute part
        ('m_lapDistance',                   ctypes.c_float),  # Distance vehicle is around current lap in metres - can, be negative if line not crossed yet
        ('m_totalDistance',                 ctypes.c_float),  # Total distance travelled in session in metres - can, be negative if line not crossed yet
        ('m_safetyCarDelta',                ctypes.c_float),  # Delta in seconds for safety car
        ('m_car_position',                  ctypes.c_uint8),  # Car race position
        ('m_currentLapNum',                 ctypes.c_uint8),  # Current lap number
        ('m_pitStatus',                     ctypes.c_uint8),  # PitStatus in Appendices1
        ('m_numPitStops',                   ctypes.c_uint8),  # Number of pit stops taken in this race
        ('m_sector',                        ctypes.c_uint8),  # Sector in Appendices1
        ('m_currentLapInvalid',             ctypes.c_uint8),  # Current lap invalid - LapInvalidStatus in Appendices1
        ('m_penalties',                     ctypes.c_uint8),  # Accumulated time penalties in seconds to be added
        ('m_totalWarnings',                 ctypes.c_uint8),  # Accumulated number of warnings issued
        ('m_cornerCuttingWarnings',         ctypes.c_uint8),  # Accumulated number of corners cutting warnings issued
        ('m_numUnservedDriveThroughPens',   ctypes.c_uint8),  # Num drive through pens left to serve
        ('m_numUnservedStopGoPens',         ctypes.c_uint8),  # Num stop go pens left to serve
        ('m_gridPosition',                  ctypes.c_uint8),  # Grid position the vehicle started the race in
        ('m_driverStatus',                  ctypes.c_uint8),  # Status of driver - DriverStatus in Appendices1

        ('m_resultStatus',                  ctypes.c_uint8),  # Result status - ResultStatus in Appendices1

        ('m_pitLaneTimerActive',            ctypes.c_uint8),  # Pit lane timing, Activeness in Appendices1
        ('m_pitLaneTimeInLaneInMs',         ctypes.c_uint16), # If active, the current time spent in the pit lane in ms
        ('m_pitStopTimerInMs',              ctypes.c_uint16), # Time of the actual pit stop in ms
        ('m_pitStopShouldServePen',         ctypes.c_uint8),  # Whether the car should serve a penalty at this stop
        ('m_speedTrapFastestSpeed',         ctypes.c_float), # Time of the actual pit stop in ms
        ('m_speedTrapFastestLap',           ctypes.c_uint8),  # Whether the car should serve a penalty at this stop
    ]

class PacketLapData(ctypes.LittleEndianStructure):
    _fields_ = [
        ('m_header',                PacketHeader),   # Header
        ('m_lapData',               LapData * 22),   # Lap data for all cars on track
        ('m_timeTrialPBCarIdx',     ctypes.c_uint8), # Index of Personal Best car in time trial (255 if invalid)
        ('m_timeTrialRivalCarIdx',  ctypes.c_uint8), # Index of Rival car in time trial (255 if invalid)
    ]

### Event Packet -- When the event occurs -- 45 bytes

class FastestLap(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('vehicleIdx', ctypes.c_uint8), # Vehicle index of car achieving fastest lap
        ('lapTime',    ctypes.c_float)  # Lap time is in seconds
    ]

class Retirement(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('vehicleIdx', ctypes.c_uint8) # Vehicle index of car retiring
    ]

class TeamMateInPits(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('vehicleIdx', ctypes.c_uint8) # Vehicle index of team mate
    ]

class RaceWinner(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('vehicleIdx', ctypes.c_uint8) # Vehicle index of the race winner
    ]

class Penalty(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('penaltyType',         ctypes.c_uint8), # PenaltyType in Appendices2
        ('infringementType',    ctypes.c_uint8), # InfringmentType in Appendices2
        ('vehicleIdx',          ctypes.c_uint8), # Vehicle index of the car the penalty is applied to
        ('otherVehicleIdx',     ctypes.c_uint8), # Vehicle index of the other car involved
        ('time',                ctypes.c_uint8), # Time gained, or time spent doing action in seconds
        ('lapNum',              ctypes.c_uint8), # Lap the penalty occurred on
        ('placesGained',        ctypes.c_uint8)  # Number of places gained by this
    ]

class SpeedTrap(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('vehicleIdx',                  ctypes.c_uint8), # Vehicle index of the vehicle triggering speed trap
        ('speed',                       ctypes.c_float), # Top speed achieved in kilometres per hour
        ('isOverallFastestInSession',   ctypes.c_uint8), # Overall fastest speed in InSession in Appendices1
        ('isDriverFastestInSession',    ctypes.c_uint8), # Fastest speed for driver InSession in Appendices1
        ('fastestVehicleIdxInSession',  ctypes.c_uint8), # Vehicle index of the vehicle that is the fastest in this session
        ('fastestSpeedInSession',       ctypes.c_float)  # Speed of the vehicle that is the fastest in this session
    ]

class StartLIghts(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('numLights', ctypes.c_uint8) # Number of lights showing
    ]

class DriveThroughPenaltyServed(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('vehicleIdx', ctypes.c_uint8) # Vehicle index of the vehicle serving drive through
    ]

class StopGoPenaltyServed(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('vehicleIdx', ctypes.c_uint8) # Vehicle index of the vehicle serving stop go
    ]

class Flashback(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('flashbackFrameIdentifier',  ctypes.c_uint32), # Frame identifier flashed back to
        ('flashbackSessionTime',      ctypes.c_float)  # Session time flashed back to
    ]

class Buttons(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_buttonStatus', ctypes.c_uint32), # Bit flags specifying which buttons are being pressed currently - ButtonFlags in Appendices2
    ]

class Overtake(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('overtakingVehicleIdx',        ctypes.c_uint8), # Vehicle index of the vehicle overtaking
        ('beingOvertakenVehicleIdx',    ctypes.c_uint8)  # Vehicle index of the vehicle being overtaken
    ]

class SafetyCar(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('safetyCarType',   ctypes.c_uint8), # 0 = No Safety Car, 1 = Full Safety Car, 2 = Virtual Safety Car, 3 = Formation Lap Safety Car
        ('eventType',       ctypes.c_uint8)  # 0 = Deployed, 1 = Returning, 2 = Returned, 3 = Resume Race
    ]

class Collision(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('vehicle1Idx',     ctypes.c_uint8), # Vehicle index of the first vehicle involved in the collision
        ('vehicle2Idx',     ctypes.c_uint8)  # Vehicle index of the second vehicle involved in the collision
    ]

class EventDataDetails(ctypes.Union, PacketMixin):
    _pack_ = 1
    _fields_ = [
        ('m_fastestLap',                  FastestLap),
        ('m_retirement',                  Retirement),
        ('m_teamMateInPits',              TeamMateInPits),
        ('m_raceWinner',                  RaceWinner),
        ('m_penalty',                     Penalty),
        ('m_speedTrap',                   SpeedTrap),
        ('m_startLights',                 StartLIghts),
        ('m_driveThroughPenaltyServed',   DriveThroughPenaltyServed),
        ('m_stopGoPenaltyServed',         StopGoPenaltyServed),
        ('m_flashback',                   Flashback),
        ('m_buttons',                     Buttons),
        ('m_overtake',                    Overtake),
        ('m_safetyCar',                   SafetyCar),
        ('m_collision',                   Collision)
    ]

class PacketEventData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header',            PacketHeader),          # Header
        ('m_eventStringCode',   ctypes.c_uint8 * 4),    # Event string code, EventStringCode in Appendices2
        ('m_eventDetails',      EventDataDetails),      # Event details - should be interpreted differently for each type
    ]

### Participants Packet -- Every 5 seconds -- 1350 bytes

class ParticipantData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_aiControlled',      ctypes.c_uint8),        # Whether the vehicle is AiControlled in Appendices1
        ('m_driverId',          ctypes.c_uint8),        # Driver id - Drivers in Appendices2
        ('m_networkId',         ctypes.c_uint8),        # Network id – unique identifier for network players
        ('m_teamId',            ctypes.c_uint8),        # Team id - Teams in Appendices2
        ('m_myTeam',            ctypes.c_uint8),        # My team flag – MyTeamFlag in Appendices1
        ('m_raceNumber',        ctypes.c_uint8),        # Race number of the car
        ('m_nationality',       ctypes.c_uint8),        # Nationality of the driver
        ('m_name',              ctypes.c_char * 48),    # Name of participant in UTF-8 format – null terminated, Will be truncated with … (U+2026) if too long
        ('m_yourTelemetry',     ctypes.c_uint8),        # The player's UDP setting, UdpStatus in Appendices1
        ('m_showOnlineNames',   ctypes.c_uint8),        # The player's show online names setting, AssistSwitch in Appendices1
        ('m_techLevel',         ctypes.c_uint16),       # F1 World tech level
        ('m_platform',          ctypes.c_uint8),        # Platform in Appendices1
    ]

class PacketParticipantsData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header',            PacketHeader),          # Header
        ('m_numActiveCars',     ctypes.c_uint8),        # Number of active cars in the data – should match number of cars on HUD
        ('m_participants',      ParticipantData * 22),
    ]

### Car Setups Packet -- 2 per second -- 1133 bytes

class CarSetupData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_frontWing',                 ctypes.c_uint8), # Front wing aero
        ('m_rearWing',                  ctypes.c_uint8), # Rear wing aero
        ('m_onThrottle',                ctypes.c_uint8), # Differential adjustment on throttle (percentage)
        ('m_offThrottle',               ctypes.c_uint8), # Differential adjustment off throttle (percentage)
        ('m_frontCamber',               ctypes.c_float), # Front camber angle (suspension geometry)
        ('m_rearCamber',                ctypes.c_float), # Rear camber angle (suspension geometry)
        ('m_frontToe',                  ctypes.c_float), # Front toe angle (suspension geometry)
        ('m_rearToe',                   ctypes.c_float), # Rear toe angle (suspension geometry)
        ('m_frontSuspension',           ctypes.c_uint8), # Front suspension
        ('m_rearSuspension',            ctypes.c_uint8), # Rear suspension
        ('m_frontAntiRollBar',          ctypes.c_uint8), # Front anti-roll bar
        ('m_rearAntiRollBar',           ctypes.c_uint8), # Front anti-roll bar
        ('m_frontSuspensionHeight',     ctypes.c_uint8), # Front ride height
        ('m_rearSuspensionHeight',      ctypes.c_uint8), # Rear ride height
        ('m_brakePressure',             ctypes.c_uint8), # Brake pressure (percentage)
        ('m_brakeBias',                 ctypes.c_uint8), # Brake bias (percentage)
        ('m_engineBraking',             ctypes.c_uint8), # Engine braking (percentage)
        ('m_rearLeftTyrePressure',      ctypes.c_float), # Rear left tyre pressure (PSI)
        ('m_rearRightTyrePressure',     ctypes.c_float), # Rear right tyre pressure (PSI)
        ('m_frontLeftTyrePressure',     ctypes.c_float), # Front left tyre pressure (PSI)
        ('m_frontRightTyrePressure',    ctypes.c_float), # Front right tyre pressure (PSI)
        ('m_ballast',                   ctypes.c_uint8), # Ballast
        ('m_fuelLoad',                  ctypes.c_float), # Fuel load
    ]

class PacketCarSetupData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header',                PacketHeader),      # Header
        ('m_car_setups',            CarSetupData * 22),
        ('m_nextFrontWingValue',    ctypes.c_float)     # Value of front wing after next pit stop - player only
    ]

### Car Telemetry Packet -- Rate as specified in menus -- 1352 bytes

class CarTelemetryData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_speed',                     ctypes.c_uint16),       # Speed of car in kilometres per hour
        ('m_throttle',                  ctypes.c_float),        # Amount of throttle applied (0.0 to 1.0)
        ('m_steer',                     ctypes.c_float),        # Steering (-1.0 (full lock left) to 1.0 (full lock right))
        ('m_brake',                     ctypes.c_float),        # Amount of brake applied (0.0 to 1.0)
        ('m_clutch',                    ctypes.c_uint8),        # Amount of clutch applied (0 to 100)
        ('m_gear',                      ctypes.c_int8),         # Gear selected (1-8, N=0, R=-1)
        ('m_engineRpm',                 ctypes.c_uint16),       # Engine RPM
        ('m_drs',                       ctypes.c_uint8),        # AssistSwitch in Appendices1
        ('m_revLightsPercent',          ctypes.c_uint8),        # Rev lights indicator (percentage)
        ('m_revLightsBitValue',         ctypes.c_uint16),       # Rev lights (bit 0 = leftmost LED, bit 14 = rightmost LED)
        ('m_brakesTemperature',         ctypes.c_uint16 * 4),   # Brakes temperature (celsius)
        ('m_tyresSurfaceTemperature',   ctypes.c_uint8 * 4),    # Tyres surface temperature (celsius)
        ('m_tyresInnerTemperature',     ctypes.c_uint8 * 4),    # Tyres inner temperature (celsius)
        ('m_engineTemperature',         ctypes.c_uint16),       # Engine temperature (celsius)
        ('m_tyresPressure',             ctypes.c_float * 4),    # Tyres pressure (PSI)
        ('m_surfaceType',               ctypes.c_uint8 * 4),    # Driving surface, SurfaceType in Appendices2
    ]

class PacketCarTelemetryData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header',                        PacketHeader),      # Header
        ('m_carTelemetryData',              CarTelemetryData * 22),
        ('m_mfdPanelIndex',                 ctypes.c_uint8),    # Index of MFD panel open - MfdPanel  in Appendices1, May vary depending on game mode
        ('m_mfdPanelIndexSecondaryPlayer',  ctypes.c_uint8),    # See above
        ('m_suggestedGear',                 ctypes.c_int8),     # Suggested gear for the player (1-8), 0 if no gear suggested
    ]

### Car Status Packet -- Rate as specified in menus -- 1239 bytes

class CarStatusData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_tractionControl',           ctypes.c_uint8),     # Traction control - TractionStatus in Appendices1
        ('m_antiLockBrakes',            ctypes.c_uint8),    # AssistSwitch in Appendices1
        ('m_fuelMix',                   ctypes.c_uint8),    # Fuel mix - FuelMix in Appendices1
        ('m_frontBrakeBias',            ctypes.c_uint8),    # Front brake bias (percentage)
        ('m_pitLimiterStatus',          ctypes.c_uint8),    # Pit limiter status - AssistSwitch in Appendices1
        ('m_fuelInTank',                ctypes.c_float),    # Current fuel mass
        ('m_fuelCapacity',              ctypes.c_float),    # Fuel capacity
        ('m_fuelRemainingLaps',         ctypes.c_float),    # Fuel remaining in terms of laps (value on MFD)
        ('m_maxRpm',                    ctypes.c_uint16),   # Cars max RPM, point of rev limiter
        ('m_idleRpm',                   ctypes.c_uint16),   # Cars idle RPM
        ('m_maxGears',                  ctypes.c_uint8),    # Maximum number of gears
        ('m_drsAllowed',                ctypes.c_uint8),    # DrsAllowed in Appendices1
        ('m_drsActivationDistance',     ctypes.c_uint16),   # 0 = DRS not available, non-zero - DRS will be available in [X] metres

        ('m_actualTyreCompound',        ctypes.c_uint8),    # ActualTyres in Appendices1

        ('m_visualTyreCompound',        ctypes.c_uint8),    # VisualTyres in Appendices1

        ('m_tyresAgeLaps',              ctypes.c_uint8),    # Age in laps of the current set of tyres
        ('m_vehicleFiaFlags',           ctypes.c_int8),     # VehicleFlag in Appendices1

        ('m_enginePowerICE',            ctypes.c_float),    # Engine power output of ICE (W)
        ('m_enginePowerMGUK',            ctypes.c_float),    # Engine power output of MGU-K (W)
        ('m_ersStoreEnergy',            ctypes.c_float),    # ERS energy store in Joules
        ('m_ersDeployMode',             ctypes.c_uint8),    # ERS deployment mode, DeployMode in Appendices1

        ('m_ersHarvestedThisLapMguk',   ctypes.c_float),    # ERS energy harvested this lap by MGU-K
        ('m_ersHarvestedThisLapMguh',   ctypes.c_float),    # ERS energy harvested this lap by MGU-H
        ('m_ersDeployedThisLap',        ctypes.c_float),    # ERS energy deployed this lap
        ('m_networkPaused',             ctypes.c_uint8),    # Whether the car is paused in a network game
    ]

class PacketCarStatusData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header',        PacketHeader),  # Header
        ('m_carStatusData', CarStatusData * 22),
    ]

### Final Classification Packet -- Once at the end of a race -- 1020 bytes

class FinalClassificationData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_position',          ctypes.c_uint8),        # Finishing position
        ('m_numLaps',           ctypes.c_uint8),        # Number of laps completed
        ('m_gridPosition',      ctypes.c_uint8),        # Grid position of the car
        ('m_points',            ctypes.c_uint8),        # Number of points scored
        ('m_numPitStops',       ctypes.c_uint8),        # Number of pit stops made
        ('m_resultStatus',      ctypes.c_uint8),        # Result status - ResultStatus in Appendices1

        ('m_bestLapTimeInMs',   ctypes.c_uint32),       # Best lap time of the session in milliseconds
        ('m_totalRaceTime',     ctypes.c_double),       # Total race time in seconds without penalties
        ('m_penaltiesTime',     ctypes.c_uint8),        # Total penalties accumulated in seconds
        ('m_numPenalties',      ctypes.c_uint8),        # Number of penalties applied to this driver
        ('m_numTyreStints',     ctypes.c_uint8),        # Number of tyres stints up to maximum
        ('m_tyreStintsActual',  ctypes.c_uint8 * 8),    # Actual tyres used by this driver
        ('m_tyreStintsVisual',  ctypes.c_uint8 * 8),    # Visual tyres used by this driver
        ('tyreStintsEndLaps',   ctypes.c_uint8 * 8),    # The lap number stints end on
    ]

class PacketFinalClassificationData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header',                PacketHeader),      # Header
        ('m_numCars',               ctypes.c_uint8),    # Number of cars in the final classification
        ('m_classificationData',    FinalClassificationData * 22),
    ]

### Lobby Info Packet -- Two every second when in the lobby -- 1306 bytes

class LobbyInfoData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_aiControlled',      ctypes.c_uint8),        # Whether the vehicle is AI (1) or Human (0) controlled
        ('m_teamId',            ctypes.c_uint8),        # Team id - see appendix (255 if no team currently selected)
        ('m_nationality',       ctypes.c_uint8),        # Nationality of the driver
        ('m_platform',          ctypes.c_uint8),        # Platform in Appendices1
        ('m_name',              ctypes.c_char * 48),    # Name of participant in UTF-8 format – null terminated Will be truncated with ... (U+2026) if too long
        ('m_carNumber',         ctypes.c_uint8),        # Car number of the player
        ('m_yourTelemetry',     ctypes.c_uint8),        # The player's UDP setting, 0 = restricted, 1 = public
        ('m_showOnlineNames',   ctypes.c_uint8),        # The player's show online names setting, 0 = off, 1 = on
        ('m_techLevel',         ctypes.c_uint16),       # F1 World tech level
        ('m_readyStatus',       ctypes.c_uint8),        # ReadyStatus in Appendices1
    ]

class PacketLobbyInfoData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header',        PacketHeader),      # Header Packet specific data
        ('m_numPlayers',    ctypes.c_uint8),    # Number of players in the lobby data
        ('m_lobbyPlayers',  LobbyInfoData * 22),
    ]

### Car Damage Packet -- 10 per second -- 953 bytes

class CarDamageData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_tyresWear',             ctypes.c_float * 4),    # Tyre wear (percentage)
        ('m_tyresDamage',           ctypes.c_uint8 * 4),    # Tyre damage (percentage)
        ('m_brakesDamage',          ctypes.c_uint8 * 4),    # Brakes damage (percentage)
        ('m_frontLeftWingDamage',   ctypes.c_uint8),        # Front left wing damage (percentage)
        ('m_frontRightWingDamage',  ctypes.c_uint8),        # Front right wing damage (percentage)
        ('m_rearWingDamage',        ctypes.c_uint8),        # Rear wing damage (percentage)
        ('m_floorDamage',           ctypes.c_uint8),        # Floor damage (percentage)
        ('m_diffuserDamage',        ctypes.c_uint8),        # Diffuser damage (percentage)
        ('m_sidepodDamage',         ctypes.c_uint8),        # Sidepod damage (percentage)
        ('m_drsFault',              ctypes.c_uint8),        # Indicator for DRS fault, Fault in Appendices1
        ('m_ersFault',              ctypes.c_uint8),        # Indicator for ERS fault, Fault in Appendices1

        ('m_gearBoxDamage',         ctypes.c_uint8),        # Gear box damage (percentage)
        ('m_engineDamage',          ctypes.c_uint8),        # Engine damage (percentage)
        ('m_engineMguhwear',        ctypes.c_uint8),        # Engine wear MGU-H (percentage)
        ('m_engineEswear',          ctypes.c_uint8),        # Engine wear ES (percentage)
        ('m_engineCewear',          ctypes.c_uint8),        # Engine wear CE (percentage)
        ('m_engineIcewear',         ctypes.c_uint8),        # Engine wear ICE (percentage)
        ('m_engineMgukwear',        ctypes.c_uint8),        # Engine wear MGU-K (percentage)
        ('m_engineTcwear',          ctypes.c_uint8),        # Engine wear TC (percentage)
        ('m_engineBlown',           ctypes.c_uint8),        # Engine blown, Fault in Appendices1
        ('m_engineSeized',          ctypes.c_uint8),        # Engine seized, Fault in Appendices1
    ]

class PacketCarDamageData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header',        PacketHeader), # Header
        ('m_carDamageData', CarDamageData * 22),
    ]

### Session History Packet -- 20 per second but cycling through cars -- 1460 bytes

class LapHistoryData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_lapTimeInMs',       ctypes.c_uint32),   # Lap time in milliseconds
        ('m_sector1TimeInMs',   ctypes.c_uint16),   # Sector 1 time in milliseconds
        ('m_sector1TimeMinutes',ctypes.c_uint8),    # Sector 1 whole minute part
        ('m_sector2TimeInMs',   ctypes.c_uint16),   # Sector 2 time in milliseconds
        ('m_sector2TimeMinutes',ctypes.c_uint8),    # Sector 2 whole minute part
        ('m_sector3TimeInMs',   ctypes.c_uint16),   # Sector 3 time in milliseconds
        ('m_sector3TimeMinutes',ctypes.c_uint8),    # Sector 3 whole minute part
        ('m_lapValidBitFlags',  ctypes.c_uint8),    # ValidBitFlag in Appendices1
    ]

class TyreStintHistoryData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_endLap',                ctypes.c_uint8), # Lap the tyre usage ends on (255 of current tyre)
        ('m_tyreActualCompound',    ctypes.c_uint8), # Actual tyres used by this driver
        ('m_tyreVisualCompound',    ctypes.c_uint8), # Visual tyres used by this driver
    ]

class PacketSessionHistoryData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header',                PacketHeader),          # Header
        ('m_carIdx',                ctypes.c_uint8),        # Index of the car this lap data relates to
        ('m_numLaps',               ctypes.c_uint8),        # Num laps in the data (including current partial lap)
        ('m_numTyreStints',         ctypes.c_uint8),        # Number of tyre stints in the data
        ('m_bestLapTimeLapNum',     ctypes.c_uint8),        # Lap the best lap time was achieved on
        ('m_bestSector1LapNum',     ctypes.c_uint8),        # Lap the best Sector 1 time was achieved on
        ('m_bestSector2LapNum',     ctypes.c_uint8),        # Lap the best Sector 2 time was achieved on
        ('m_bestSector3LapNum',     ctypes.c_uint8),        # Lap the best Sector 3 time was achieved on
        ('m_lapHistoryData',        LapHistoryData * 100),  # 100 laps of data max
        ('m_tyreStintsHistoryData', TyreStintHistoryData * 8),
    ]

### Tyre Set Packet -- 20 per second but cycling through cars -- 231 bytes

class TyreSetData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_actualTyreCompound',      ctypes.c_uint8),   # Actual tyre compound used
        ('m_visualTyreCompound',      ctypes.c_uint8),   # Visual tyre compound used
        ('m_wear',                    ctypes.c_uint8),   # Tyre wear (percentage)
        ('m_available',               ctypes.c_uint8),   # Whether this set is currently available
        ('m_recommendedSession',      ctypes.c_uint8),   # Recommended session for tyre set
        ('m_lifeSpan',                ctypes.c_uint8),   # Laps left in this tyre set
        ('m_usableLife',              ctypes.c_uint8),   # Max number of laps recommended for this compound
        ('m_lapDeltaTime',            ctypes.c_int16),   # Lap delta time in milliseconds compared to fitted set
        ('m_fitted',                  ctypes.c_uint8),   # Whether the set is fitted or not
    ]

class PacketTyreSetsData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header',        PacketHeader),      # Header
        ('m_carIdx',        ctypes.c_uint8),    # Index of the car this data relates to
        ('m_tyreSetData',   TyreSetData * 20),  # 13 (dry) + 7 (wet)
        ('m_fittedIdx',     ctypes.c_uint8),    # Index into array of fitted tyre
    ]

### Motion Ex Packet -- Rate as specified in menus -- 237 bytes

class PacketMotionExData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header',                    PacketHeader),       # Header
        # Extra player car ONLY data
        ('m_suspensionPosition',        ctypes.c_float * 4), # Note: All wheel arrays have the following order:
        ('m_suspensionVelocity',        ctypes.c_float * 4), # RL, RR, FL, FR
        ('m_suspensionAcceleration',    ctypes.c_float * 4), # RL, RR, FL, FR
        ('m_wheelSpeed',                ctypes.c_float * 4), # Speed of each wheel
        ('m_wheelSlipRatio',            ctypes.c_float * 4), # Slip ratio for each wheel
        ('m_wheelSlipAngle',            ctypes.c_float * 4), # Slip angles for each wheel
        ('m_wheelLatForce',             ctypes.c_float * 4), # Lateral forces for each wheel
        ('m_wheelLongForce',            ctypes.c_float * 4), # Longitudinal forces for each wheel
        ('m_heightOfCOGAboveGround',    ctypes.c_float),     # Height of centre of gravity above ground
        ('m_localVelocityX',            ctypes.c_float),     # Velocity in local space – metres/s
        ('m_localVelocityY',            ctypes.c_float),     # Velocity in local space
        ('m_localVelocityZ',            ctypes.c_float),     # Velocity in local space
        ('m_angularVelocityX',          ctypes.c_float),     # Angular velocity x-component – metres/s
        ('m_angularVelocityY',          ctypes.c_float),     # Angular velocity y-component
        ('m_angularVelocityZ',          ctypes.c_float),     # Angular velocity z-component
        ('m_angularAccelerationX',      ctypes.c_float),     # Angular acceleration x-component – metres/s
        ('m_angularAccelerationY',      ctypes.c_float),     # Angular acceleration y-component
        ('m_angularAccelerationZ',      ctypes.c_float),     # Angular acceleration z-component
        ('m_frontWheelsAngle',          ctypes.c_float),     # Current front wheels angle in radians
        ('m_wheelVertForce',            ctypes.c_float * 4), # Vertical forces for each wheel
        ('m_frontAeroHeight',           ctypes.c_float),     # Front plank edge height above road surface
        ('m_rearAeroHeight',            ctypes.c_float),     # Rear plank edge height above road surface
        ('m_frontRollAngle',            ctypes.c_float),     # Roll angle of the front suspension
        ('m_rearRollAngle',             ctypes.c_float),     # Roll angle of the rear suspension
        ('m_chassisYaw',                ctypes.c_float),     # Yaw angle of the chassis relative to the direction of motion - radians
    ]

### Time Trial Packet -- 1 per second, only in time trial -- 101 bytes


class TimeTrialDataSet(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_carIdx',                ctypes.c_uint8),    # Index of the car this data relates to
        ('m_teamId',                ctypes.c_uint8),    # Team id - see appendix
        ('m_lapTimeInMS',           ctypes.c_uint32),   # Lap time in milliseconds
        ('m_sector1TimeInMS',       ctypes.c_uint32),   # Sector 1 time in milliseconds
        ('m_sector2TimeInMS',       ctypes.c_uint32),   # Sector 2 time in milliseconds
        ('m_sector3TimeInMS',       ctypes.c_uint32),   # Sector 3 time in milliseconds
        ('m_tractionControl',       ctypes.c_uint8),    # 0 = off, 1 = medium, 2 = full
        ('m_gearboxAssist',         ctypes.c_uint8),    # 1 = manual, 2 = manual & suggested gear, 3 = auto
        ('m_antiLockBrakes',        ctypes.c_uint8),    # 0 (off) - 1 (on)
        ('m_equalCarPerformance',   ctypes.c_uint8),    # 0 = Realistic, 1 = Equal
        ('m_customSetup',           ctypes.c_uint8),    # 0 = No, 1 = Yes
        ('m_valid',                 ctypes.c_uint8)     # 0 = invalid, 1 = valid
    ]


class PacketTimeTrialData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header',                    PacketHeader),      # Header
        ('m_playerSessionBestDataSet',  TimeTrialDataSet),  # Player session best data set
        ('m_personalBestDataSet',       TimeTrialDataSet),  # Personal best data set
        ('m_rivalDataSet',              TimeTrialDataSet),  # Rival data set
    ]

###









