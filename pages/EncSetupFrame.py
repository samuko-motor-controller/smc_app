import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

from globalParams import g

from components.SetValueFrame import SetValueFrame
from components.SelectValueFrame import SelectValueFrame
from components.MotorDrawFrame import MotorDrawFrame





class EncSetupFrame(tb.Frame):
  def __init__(self, parentFrame):
    super().__init__(master=parentFrame)

    self.label = tb.Label(self, text="MOTOR A ENCODER SETUP", font=('Monospace',16, 'bold') ,bootstyle="dark")

    self.frame1 = tb.Frame(self)
    self.frame2 = tb.Frame(self)

    # configure grid for frame1
    self.frame1.grid_columnconfigure((0,1,2,3), weight=1, uniform='a')

    #create widgets to be added to frame1
    g.pulsePerRevA = g.serClient.get("pprA")
    self.setPulsePerRev = SetValueFrame(self.frame1, keyTextInit="PPR_A: ", valTextInit=g.pulsePerRevA,
                                        middleware_func=self.setPulsePerRevFunc)
    
    self.initDirConfigA()
    self.selectDirConfig = SelectValueFrame(self.frame1, keyTextInit="DIR_A: ", valTextInit=g.dirConfigTextA,
                                            initialComboValues=g.dirConfigTextList, middileware_func=self.selectDirConfigFunc)
    
    self.setTestPwm = SetValueFrame(self.frame1, keyTextInit="TEST_PWM: ", valTextInit=g.testPwmA,
                                    middleware_func=self.setTestPwmFunc)
    
    self.selectDuration = SelectValueFrame(self.frame1, keyTextInit="TEST_TIME(sec): ", valTextInit=g.testDurationA,
                                           initialComboValues=g.durationList, middileware_func=self.selectDurationFunc)

    #add framed widgets to frame1
    self.setPulsePerRev.grid(row=0, column=0, sticky='nsew', padx=5)
    self.selectDirConfig.grid(row=0, column=1, sticky='nsew', padx=5)
    self.setTestPwm.grid(row=0, column=2, sticky='nsew', padx=5)
    self.selectDuration.grid(row=0, column=3, sticky='nsew', padx=5)

    #create widgets to be added to frame2
    self.drawMotor = MotorDrawFrame(self.frame2)

    #add framed widgets to frame2
    self.drawMotor.pack(side="left", expand=True, fill="both", padx=5)


    #add frame1, frame2 and frame3 to MainFrame
    self.label.pack(side="top", fill="x", padx=(200,0), pady=(5,0))
    self.frame1.pack(side="top", expand=True, fill="x")
    self.frame2.pack(side="top", expand=True, fill="both", pady=(120, 0))




  def setTestPwmFunc(self, pwm_val_str):
    try:
      if pwm_val_str:
        val = int(pwm_val_str)
        if val > 255:
          g.testPwmA = 255
        elif val < -255:
          g.testPwmA = -255
        else:
          g.testPwmA = val
    except:
      pass

    return g.testPwmA
    


  def setPulsePerRevFunc(self, ppr_val_str):
    try:
      if ppr_val_str:
        val = float(ppr_val_str)
        isSuccessful = g.serClient.send("pprA", val)
        val = g.serClient.get("pprA")
        g.pprA = val
    except:
      pass

    return g.pprA

  

  def selectDurationFunc(self, duration_val_str):
    try:
      if duration_val_str:
        val = int(duration_val_str)
        g.testDurationA = val
    except:
      pass

    return g.testDurationA
  


  def initDirConfigA(self):
    try:
      g.dirConfigA = g.serClient.get("rdirA")
      if int(g.dirConfigA) == 1:
        g.dirConfigTextA = g.dirConfigTextList[0]
      elif int(g.dirConfigA) == -1:
        g.dirConfigTextA = g.dirConfigTextList[1]
      self.resetInitialTheta()
    except:
      pass



  def selectDirConfigFunc(self, dir_val_str):
    try:
      if dir_val_str:
        g.dirConfigTextA = dir_val_str

        if g.dirConfigTextA == g.dirConfigTextList[0]:
          isSuccessful = g.serClient.send("rdirA", 1.00)
          g.dirConfigA = g.serClient.get("rdirA")
          g.initialThetaA = -1*g.thetaA - 90
        elif g.dirConfigTextA == g.dirConfigTextList[1]:
          isSuccessful = g.serClient.send("rdirA", -1.00)
          g.dirConfigA = g.serClient.get("rdirA")
          g.initialThetaA = -1*g.thetaA + 90

    except:
      pass

    return g.dirConfigTextA



  def resetInitialTheta(self):
    if int(g.dirConfigA) == 1:
      g.initialThetaA = g.thetaA - 90
    elif int(g.dirConfigA) == -1:
      g.initialThetaA = g.thetaA + 90
