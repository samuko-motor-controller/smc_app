import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

from math import sin, cos, radians, pi
import time

from globalParams import g




class MotorDrawFrame(tb.Frame):
  def __init__(self, parentFrame, motorNo):
    super().__init__(master=parentFrame)

    self.motorNo = motorNo

    self.displayFrame = tb.Frame(self)
    self.canvasFrame = tb.Frame(self)

    self.textFrame1 = tb.Frame(self.displayFrame)
    self.textFrame2 = tb.Frame(self.displayFrame)
    

    #create widgets to be added to the textFame
    buttonStyle = tb.Style()
    buttonStyleName = 'danger.TButton'
    buttonStyle.configure(buttonStyleName, font=('Monospace',10, 'bold'))

    g.motorAngPos[self.motorNo], g.motorAngVel[self.motorNo] = g.serClient.get(f'data{g.motorLabel[self.motorNo]}')

    self.posText = tb.Label(self.textFrame1, text="POS(rad):", font=('Monospace',10, 'bold') ,bootstyle="danger")
    self.posVal = tb.Label(self.textFrame1, text=g.motorAngPos[self.motorNo], font=('Monospace',10), bootstyle="dark")

    self.velText = tb.Label(self.textFrame2, text="VEL(rad/s):", font=('Monospace',10, 'bold') ,bootstyle="primary")
    self.velVal = tb.Label(self.textFrame2, text=g.motorAngVel[self.motorNo], font=('Monospace',10), bootstyle="dark")

    self.button1 = tb.Button(self.displayFrame, text="RESET HAND", style=buttonStyleName,
                             command=self.resetInitialTheta)
    self.button2 = tb.Button(self.displayFrame, text="START MOTOR", style=buttonStyleName,
                             command=self.sendPwmCtrl)

    #add created widgets to displayFrame
    self.posText.pack(side='left', fill='both')
    self.posVal.pack(side='left', expand=True, fill='both')

    self.velText.pack(side='left', fill='both')
    self.velVal.pack(side='left', expand=True, fill='both')

    self.textFrame1.pack(side='left', expand=True, fill='both')
    self.textFrame2.pack(side='left', expand=True, fill='both')

    self.button1.pack(side='left', fill='both', padx=(0,10))
    self.button2.pack(side='left', fill='both')

    #create widgets to be added to the canvasFame
    self.canvas = tb.Canvas(self.canvasFrame, width=300, height=500,autostyle=False ,bg="#FFFFFF", relief='solid')

    #add created widgets to canvasFame
    self.canvas.pack(side='left', expand=True, fill='both')

    # initialize canvas with motor representation shape
    x = 120
    self.r = 170 # circle radius
    self.m = (320, 180) #x, y primary "#4582EC" danger "#D9534F"
    self.circle = self.canvas.create_oval(152, 12, 488, 348, outline="#ADB5BD", width=5)
    self.line = self.canvas.create_line(self.m[0], self.m[1], 
                                  self.m[0]+self.r*cos(radians(-1*(g.motorTheta[self.motorNo]-g.motorInitialTheta[self.motorNo]))), 
                                  self.m[1]+self.r*sin(radians(-1*(g.motorTheta[self.motorNo]-g.motorInitialTheta[self.motorNo]))), 
                                  fill='#4582EC',width=10)
    self.mid_circle = self.canvas.create_oval(300, 160, 340, 200, fill="#D9534F", outline="#4582EC", width=7)


    # add displayFrame and canvasFrame to GraphFrame
    self.displayFrame.pack(side='top', expand=True, fill='x', padx=10)
    self.canvasFrame.pack(side='top', expand=True, fill='both', pady=(10,0))

    ############################################
    self.draw_motor_ang_pos()



  def sendPwmCtrl(self):
    if g.motorIsOn[self.motorNo]:
      isSuccess = g.serClient.send("pwm", 0, 0)
      if isSuccess:
        g.motorIsOn[self.motorNo] = False
        self.button2.configure(text="START MOTOR")
        # print('Motor off', isSuccess)
    else:
      if self.motorNo == 0:
        isSuccess = g.serClient.send("pwm", g.motorTestPwm[self.motorNo], 0)
      elif self.motorNo == 1:
        isSuccess = g.serClient.send("pwm", 0, g.motorTestPwm[self.motorNo])

      if isSuccess:
        g.motorIsOn[self.motorNo] = True
        g.motorStartTime[self.motorNo] = time.time()
        self.button2.configure(text="STOP MOTOR")
        # print('Motor On', isSuccess)




  def draw_motor_ang_pos(self):
    if g.motorIsOn[self.motorNo] and g.motorTestDuration[self.motorNo] < time.time()-g.motorStartTime[self.motorNo]:
        isSuccess = g.serClient.send("pwm", 0, 0)
        if isSuccess:
          g.motorIsOn[self.motorNo] = False
          self.button2.configure(text="START MOTOR")
          # print('Motor off', isSuccess)

    self.canvas.delete(self.line)
    self.canvas.delete(self.mid_circle)

    try:
      g.motorAngPos[self.motorNo], g.motorAngVel[self.motorNo] = g.serClient.get(f'data{g.motorLabel[self.motorNo]}')
    except:
      pass

    g.motorTheta[self.motorNo] = round(self.absAngDeg(g.motorAngPos[self.motorNo]),2)

    if int(g.motorDirConfig[self.motorNo]) == -1:
      self.line = self.canvas.create_line(self.m[0], self.m[1], 
                                    self.m[0]+self.r*cos(radians(g.motorTheta[self.motorNo]-g.motorInitialTheta[self.motorNo])), 
                                    self.m[1]+self.r*sin(radians(g.motorTheta[self.motorNo]-g.motorInitialTheta[self.motorNo])), 
                                    fill='#4582EC',width=10)
    elif int(g.motorDirConfig[self.motorNo]) == 1:
      self.line = self.canvas.create_line(self.m[0], self.m[1], 
                                    self.m[0]+self.r*cos(radians(-1*(g.motorTheta[self.motorNo]-g.motorInitialTheta[self.motorNo]))), 
                                    self.m[1]+self.r*sin(radians(-1*(g.motorTheta[self.motorNo]-g.motorInitialTheta[self.motorNo]))),   
                                    fill='#4582EC',width=10)
    self.mid_circle = self.canvas.create_oval(300, 160, 340, 200, fill="#D9534F", outline="#4582EC", width=7)

    self.posVal.configure(text=f"{g.motorAngPos[self.motorNo]}")
    self.velVal.configure(text=f"{g.motorAngVel[self.motorNo]}")

    self.canvas.after(1, self.draw_motor_ang_pos)


  def resetInitialTheta(self):
    if int(g.motorDirConfig[self.motorNo]) == 1:
      g.motorInitialTheta[self.motorNo] = g.motorTheta[self.motorNo] - 90
    elif int(g.motorDirConfig[self.motorNo]) == -1:
      g.motorInitialTheta[self.motorNo] = g.motorTheta[self.motorNo] + 90

  def absAngDeg(self, incAngRad):
    incAngDeg = incAngRad * 180.0 / pi
    return incAngDeg % 360.0






















# from math import sin, cos, radians, pi
# import time
# from global_var_and_func import g, setPulseDurationA, SetDataCardFrame, ChooseDataCardFrame
# import customtkinter




# def setPwmValA(text):
#   try:
#     if text:
#       val = int(text)
#       if val > 255:
#         g.ctrlPwmA = 255
#       elif val < -255:
#         g.ctrlPwmA = -255
#       else:
#         g.ctrlPwmA = val
#   except:
#     pass

#   return g.ctrlPwmA
  


# def setEncAppr(text):
#   try:
#     if text:
#       val = float(text)
#       isSuccessful = g.serClient.send("pprA", val)
#       val = g.serClient.get("pprA")
#       g.pprA = val
#   except:
#     pass

#   return g.pprA


# def sendPwmCtrlA():
#   if g.motorAIsOn:
#     isSuccess = g.serClient.send("pwm", 0, 0)
#     if isSuccess:
#       g.motorAIsOn = False
#       # print('Motor off', isSuccess)
#   else:
#     isSuccess = g.serClient.send("pwm", g.ctrlPwmA, 0)
#     if isSuccess:
#       g.motorAIsOn = True
#       g.motorAOnStartTime = time.time()
#       # print('Motor On', isSuccess)



# def resetInitialThetaA():
#   if int(g.dirA) == 1:
#     g.initialThetaA = g.thetaA - 90
#   elif int(g.dirA) == -1:
#     g.initialThetaA = g.thetaA + 90



# def initDirA():
#   try:
#     g.dirA = g.serClient.get("rdirA")
#     if int(g.dirA) == 1:
#       g.initConfigA = g.motorConfig[0]
#     elif int(g.dirA) == -1:
#       g.initConfigA = g.motorConfig[1]
#     resetInitialThetaA()
#   except:
#     pass

# def setDirA(text):
#   try:
#     if text == g.motorConfig[0]:
#       isSuccessful = g.serClient.send("rdirA", 1.00)
#       g.dirA = g.serClient.get("rdirA")
#     elif text == g.motorConfig[1]:
#       isSuccessful = g.serClient.send("rdirA", -1.00)
#       g.dirA = g.serClient.get("rdirA")
    
#     g.initConfigA = text
#     resetInitialThetaA()
#   except:
#     pass

#   return g.initConfigA





# class MotorAPosCanvas(customtkinter.CTkFrame):
#   def __init__(self, parentFrame):
#     super().__init__(parentFrame)
    
#     self.myCanvas = customtkinter.CTkCanvas(master=self, width=400, height=360, bg='white')
#     self.r = 170 # circle radius
#     self.m = (200, 180) #x, y
#     self.circle = self.myCanvas.create_oval(32, 12, 368, 348, outline="grey", width=5)
#     self.line = self.myCanvas.create_line(self.m[0], self.m[1], 
#                                   self.m[0]+self.r*cos(radians(-1*(g.thetaA-g.initialThetaA))), 
#                                   self.m[1]+self.r*sin(radians(-1*(g.thetaA-g.initialThetaA))), 
#                                   fill='#434242',width=15)
#     self.mid_circle = self.myCanvas.create_oval(180, 160, 220, 200, fill="grey", outline="#434242")

#     self.myCanvas.grid(row=0, rowspan=5, column=0, columnspan=2, padx=(5,5), pady=10)

#     # add display label
#     self.angPosDisplayLabel = customtkinter.CTkLabel(self, text="rawPosA (rad): ", font=customtkinter.CTkFont(size=13, weight="bold"), width=250)
#     self.angPosDisplayLabel.grid(row=0, column=2, padx=(5,5), pady=5, sticky="w")

#     self.angPosDisplayLabelVal = customtkinter.CTkLabel(self, text="0.0", font=customtkinter.CTkFont(size=12, weight="bold"), width=250)
#     self.angPosDisplayLabelVal.grid(row=1, column=2, padx=(5,5), pady=5, sticky="nw")

#     self.angVelDisplayLabel = customtkinter.CTkLabel(self, text="rawVelA (rad/s): ", font=customtkinter.CTkFont(size=13, weight="bold"), width=250)
#     self.angVelDisplayLabel.grid(row=2, column=2, padx=(5,5), pady=5, sticky="w")

#     self.angVelDisplayLabelVal = customtkinter.CTkLabel(self, text="0.0", font=customtkinter.CTkFont(size=12, weight="bold"), width=250)
#     self.angVelDisplayLabelVal.grid(row=3, column=2, padx=(5,5), pady=5, sticky="nw")

#     initDirA()
#     self.chooseMotorConfigFrame = ChooseDataCardFrame(self, "CONFIG AS", g.initConfigA,
#                                                       input_values=g.motorConfig,
#                                                       set_func=setDirA)
#     self.chooseMotorConfigFrame.grid(row=4, column=2, padx=5 , pady=10, ipadx=5, ipady=5)

#     self.myCanvas.after(1, self.draw_motor_ang_pos)

#   def draw_motor_ang_pos(self):
#     if g.motorAIsOn and g.motorAOnDuration < time.time()-g.motorAOnStartTime:
#         isSuccess = g.serClient.send("pwm", 0, 0)
#         if isSuccess:
#           g.motorAIsOn = False
#           # print('Motor off', isSuccess)
#     self.myCanvas.delete(self.line)
#     self.myCanvas.delete(self.mid_circle)

#     try:
#       g.angPosA, g.angVelA = g.serClient.get("dataA")
#     except:
#       pass

#     g.thetaA = round(self.absAngDeg(g.angPosA),2)

#     if int(g.dirA) == -1:
#       self.line = self.myCanvas.create_line(self.m[0], self.m[1], 
#                                     self.m[0]+self.r*cos(radians(g.thetaA-g.initialThetaA)), 
#                                     self.m[1]+self.r*sin(radians(g.thetaA-g.initialThetaA)),  
#                                     fill='#434242',width=10)
#     elif int(g.dirA) == 1:
#       self.line = self.myCanvas.create_line(self.m[0], self.m[1], 
#                                     self.m[0]+self.r*cos(radians(-1*(g.thetaA-g.initialThetaA))), 
#                                     self.m[1]+self.r*sin(radians(-1*(g.thetaA-g.initialThetaA))),  
#                                     fill='#434242',width=10)
#     self.mid_circle = self.myCanvas.create_oval(180, 160, 220, 200, fill="grey", outline="#434242")

#     self.angPosDisplayLabelVal.configure(text=f"{g.angPosA}")
#     self.angVelDisplayLabelVal.configure(text=f"{g.angVelA}")

#     self.myCanvas.after(1, self.draw_motor_ang_pos)

#   def absAngDeg(self, incAngRad):
#     incAngDeg = incAngRad * 180.0 / pi
#     return incAngDeg % 360.0




# class MotorAEncSetupFrame(customtkinter.CTkFrame):
#   def __init__(self, parent):
#     super().__init__(parent)

#     self.grid_columnconfigure((0,1,2), weight=0)
#     self.grid_rowconfigure((0,1,2,3,4,5,6), weight=0)

#     # add heading
#     self.heading = customtkinter.CTkLabel(self, text="MOTOR A ENCODER SETUP", font=customtkinter.CTkFont(size=24, weight="bold", underline=False))
#     self.heading.grid(row=0, column=0, columnspan=3, padx=10, pady=(5,25))

#     # add set card frame
#     g.pprA = g.serClient.get("pprA")
#     self.setPwmCardFrame = SetDataCardFrame(self, "PPR", g.pprA, placeHolderText="enter PPR", set_func=setEncAppr)
#     self.setPwmCardFrame.grid(row=1, column=0, padx=(20,10), pady=10)

#     self.setPwmCardFrame = SetDataCardFrame(self, "PWM", g.ctrlPwmA, placeHolderText="enter PWM",set_func=setPwmValA)
#     self.setPwmCardFrame.grid(row=1, column=1, padx=10, pady=10)

#     self.setDurationCardFrame = SetDataCardFrame(self, "DURATION(sec)", g.motorAOnDuration, placeHolderText="enter DURATION", set_func=setPulseDurationA)
#     self.setDurationCardFrame.grid(row=1, column=2, padx=10, pady=10)


#     # add buttons
#     self.resetHandButton = customtkinter.CTkButton(self, text="RESET HAND", 
#                                                    fg_color='#9BABB8', text_color='black', hover_color='#EEEEEE',
#                                                    command=resetInitialThetaA)
#     self.resetHandButton.grid(row=2, column=0, columnspan=2, padx=20 , pady=(80, 30), ipadx=5, ipady=5)

#     self.sendPulsedCmdButton = customtkinter.CTkButton(self, text="SEND PULSED COMMAND", 
#                                                        fg_color='#256D85', text_color='white',
#                                                        command=sendPwmCtrlA)
#     self.sendPulsedCmdButton.grid(row=2, column=2, padx=20, pady=(80, 30), ipadx=5, ipady=5)

#     # add canvas
#     self.motorAPosCanvas = MotorAPosCanvas(self)
#     self.motorAPosCanvas.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

