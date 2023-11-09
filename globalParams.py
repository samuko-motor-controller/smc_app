import time

class g():
  dirConfigTextList = ['left-wheel', 'right-wheel']
  durationList = [5,10, 15, 20] # in sec

  app = None
  serClient = None
  port = "None"

  i2cAddress = None

  testPwmA = 0 
  testDurationA = durationList[1]
  initialThetaA = -90
  thetaA = 0.0

  pulsePerRevA = 1
  dirConfigA = 1
  dirConfigTextA = dirConfigTextList[0]

  motorAOnStartTime = time.time()
  motorAIsOn = False

  angPosA = 0.0
  angVelA = 0.0
