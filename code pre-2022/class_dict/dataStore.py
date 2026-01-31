class MotionData():
    def __init__(self):
        self.m_suspensionPosition1=[]
        self.m_suspensionPosition2=[]
        self.m_suspensionPosition3=[]
        self.m_suspensionPosition4=[]
        self.m_suspensionVelocity1=[]
        self.m_suspensionVelocity2=[]
        self.m_suspensionVelocity3=[]
        self.m_suspensionVelocity4=[]
        self.m_suspensionAcceleration1=[]
        self.m_suspensionAcceleration2=[]
        self.m_suspensionAcceleration3=[]
        self.m_suspensionAcceleration4=[]
        self.m_wheelSpeed1=[]
        self.m_wheelSpeed2=[]
        self.m_wheelSpeed3=[]
        self.m_wheelSpeed4=[]
        self.m_wheelSlip1=[]
        self.m_wheelSlip2=[]
        self.m_wheelSlip3=[]
        self.m_wheelSlip4=[]
        self.m_localVelocityX=[]
        self.m_localVelocityY=[]
        self.m_localVelocityZ=[]
        self.m_angularVelocityX=[]
        self.m_angularVelocityY=[]
        self.m_angularVelocityZ=[]
        self.m_angularAccelerationX=[]
        self.m_angularAccelerationY=[]
        self.m_angularAccelerationZ=[]
        self.m_frontWheelsAngle=[]
        self.m_carMotionData=[]

    def update(self,data):
        self.m_suspensionPosition1.append(data["m_suspensionPosition"][0])
        self.m_suspensionPosition2.append(data["m_suspensionPosition"][1])
        self.m_suspensionPosition3.append(data["m_suspensionPosition"][2])
        self.m_suspensionPosition4.append(data["m_suspensionPosition"][3])
        self.m_suspensionVelocity1.append(data["m_suspensionVelocity"][0])
        self.m_suspensionVelocity2.append(data["m_suspensionVelocity"][1])
        self.m_suspensionVelocity3.append(data["m_suspensionVelocity"][2])
        self.m_suspensionVelocity4.append(data["m_suspensionVelocity"][3])
        self.m_suspensionAcceleration1.append(data["m_suspensionAcceleration"][0])
        self.m_suspensionAcceleration2.append(data["m_suspensionAcceleration"][1])
        self.m_suspensionAcceleration3.append(data["m_suspensionAcceleration"][2])
        self.m_suspensionAcceleration4.append(data["m_suspensionAcceleration"][3])
        self.m_wheelSpeed1.append(data["m_wheelSpeed"][0])
        self.m_wheelSpeed2.append(data["m_wheelSpeed"][1])
        self.m_wheelSpeed3.append(data["m_wheelSpeed"][2])
        self.m_wheelSpeed4.append(data["m_wheelSpeed"][3])
        self.m_wheelSlip1.append(data["m_wheelSlip"][0])
        self.m_wheelSlip2.append(data["m_wheelSlip"][1])
        self.m_wheelSlip3.append(data["m_wheelSlip"][2])
        self.m_wheelSlip4.append(data["m_wheelSlip"][3])
        self.m_localVelocityX.append(data["m_localVelocityX"])
        self.m_localVelocityY.append(data["m_localVelocityY"])
        self.m_localVelocityZ.append(data["m_localVelocityZ"])
        self.m_angularVelocityX.append(data["m_angularVelocityX"])
        self.m_angularVelocityY.append(data["m_angularVelocityY"])
        self.m_angularVelocityZ.append(data["m_angularVelocityZ"])
        self.m_angularAccelerationX.append(data["m_angularAccelerationX"])
        self.m_angularAccelerationY.append(data["m_angularAccelerationY"])
        self.m_angularAccelerationZ.append(data["m_angularAccelerationZ"])
        self.m_frontWheelsAngle.append(data["m_frontWheelsAngle"])
        self.m_carMotionData.append(data["m_carMotionData"])

class participantsData():
    def __init__(self):
        self.m_numActiveCars=[]
        self.m_participants=[]
    def update(self,data):
        self.m_numActiveCars.append(data["m_numActiveCars"])
        self.m_participants.append(data["m_participants"])