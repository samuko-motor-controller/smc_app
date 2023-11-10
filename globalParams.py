import time

class g():
  dirConfigTextList = ['left-wheel', 'right-wheel']
  durationList = [5,10, 15, 20] # in sec

  app = None
  serClient = None
  port = "None"

  i2cAddress = None

  #### motorA is index 0 and motorB is index 1 ##########
  motorLabel = ['A', 'B']

  motorTestPwm = [0, 0] 
  motorTestDuration = [durationList[1], durationList[1]]
  
  motorInitialTheta = [-90, -90]
  motorTheta = [0.0, 0.0]

  motorPPR = [1, 1]
  motorDirConfig = [1, 1]
  motorDirConfigText = [dirConfigTextList[0], dirConfigTextList[1]]

  motorStartTime = [time.time(), time.time()]
  motorIsOn = [False, False]

  motorAngPos = [0.0, 0.0]
  motorAngVel = [0.0, 0.0]
  #######################################################
