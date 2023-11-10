import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

from globalParams import g

from components.SetValueFrame import SetValueFrame
from components.SelectValueFrame import SelectValueFrame
from components.GraphFrame import GraphFrame




class PidSetupFrame(tb.Frame):
  def __init__(self, parentFrame, motorNo):
    super().__init__(master=parentFrame)

    self.motorNo = motorNo

    self.label = tb.Label(self, text=f"MOTOR {g.motorLabel[self.motorNo]} PID SETUP", font=('Monospace',16, 'bold') ,bootstyle="dark")

    self.frame1 = tb.Frame(self)
    self.frame2 = tb.Frame(self)

    # configure grid for frame1
    self.frame1.grid_columnconfigure((0,1,2,3), weight=1, uniform='a')
    self.frame1.grid_rowconfigure((0,1), weight=1, uniform='a')


    #create widgets to be added to frame1
    g.motorKp[self.motorNo] = g.serClient.get(f"kp{g.motorLabel[self.motorNo]}")
    self.setKp = SetValueFrame(self.frame1, keyTextInit=f"KP_{g.motorLabel[self.motorNo]}: ", valTextInit=g.motorKp[self.motorNo],
                               middleware_func=self.setKpFunc)

    g.motorKi[self.motorNo] = g.serClient.get(f"ki{g.motorLabel[self.motorNo]}")
    self.setKi = SetValueFrame(self.frame1, keyTextInit=f"KI_{g.motorLabel[self.motorNo]}: ", valTextInit=g.motorKi[self.motorNo],
                               middleware_func=self.setKiFunc)

    g.motorKd[self.motorNo] = g.serClient.get(f"kd{g.motorLabel[self.motorNo]}")
    self.setKd = SetValueFrame(self.frame1, keyTextInit=f"KD_{g.motorLabel[self.motorNo]}: ", valTextInit=g.motorKd[self.motorNo],
                               middleware_func=self.setKdFunc)

    g.motorCf[self.motorNo] = g.serClient.get(f"f0{g.motorLabel[self.motorNo]}")
    self.setCf = SetValueFrame(self.frame1, keyTextInit=f"CF_{g.motorLabel[self.motorNo]}(Hz): ", valTextInit=g.motorCf[self.motorNo],
                               middleware_func=self.setCfFunc)
    


    self.setMaxVel = SetValueFrame(self.frame1, keyTextInit="MAX(rad/s): ", valTextInit=g.motorMaxVel[self.motorNo],
                                    middleware_func=self.setMaxVelFunc)
    
    self.setTargetVel = SetValueFrame(self.frame1, keyTextInit="TARGET(rad/s): ", valTextInit=g.motorTargetVel[self.motorNo],
                                    middleware_func=self.setTargetVelFunc)
    
    self.selectSignal = SelectValueFrame(self.frame1, keyTextInit="TEST_SIGNAL: ", valTextInit=g.motorTestSignal[self.motorNo],
                                           initialComboValues=g.signalList, middileware_func=self.selectSignalFunc)
    
    self.selectDuration = SelectValueFrame(self.frame1, keyTextInit="TEST_TIME(sec): ", valTextInit=g.motorTestDuration[self.motorNo],
                                           initialComboValues=g.durationList, middileware_func=self.selectDurationFunc)


    #add framed widgets to frame1
    self.setKp.grid(row=0, column=0, sticky='nsew', padx=5, pady=(0,10))
    self.setKi.grid(row=0, column=1, sticky='nsew', padx=5, pady=(0,10))
    self.setKd.grid(row=0, column=2, sticky='nsew', padx=5, pady=(0,10))
    self.setCf.grid(row=0, column=3, sticky='nsew', padx=5, pady=(0,10))
  
    self.setMaxVel.grid(row=1, column=0, sticky='nsew', padx=5)
    self.setTargetVel.grid(row=1, column=1, sticky='nsew', padx=5)
    self.selectSignal.grid(row=1, column=2, sticky='nsew', padx=5)
    self.selectDuration.grid(row=1, column=3, sticky='nsew', padx=5)


    #create widgets to be added to frame2
    self.graph = GraphFrame(self.frame2)

    #add framed widgets to frame2
    self.graph.pack(side="left", expand=True, fill="both", padx=5)


    #add frame1, frame2 and frame3 to MainFrame
    self.label.pack(side="top", fill="x", padx=(200,0), pady=(5,0))
    self.frame1.pack(side="top", expand=True, fill="x")
    self.frame2.pack(side="top", expand=True, fill="both", pady=(20, 0))

 

  def setKpFunc(self, kp_val_str):
    try:
      if kp_val_str:
        isSuccessful = g.serClient.send(f"kp{g.motorLabel[self.motorNo]}", float(kp_val_str))
        val = g.serClient.get(f"kp{g.motorLabel[self.motorNo]}")
        g.motorKp[self.motorNo] = val
    except:
      pass

    return g.motorKp[self.motorNo]
  

  def setKiFunc(self, ki_val_str):
    try:
      if ki_val_str:
        isSuccessful = g.serClient.send(f"ki{g.motorLabel[self.motorNo]}", float(ki_val_str))
        val = g.serClient.get(f"ki{g.motorLabel[self.motorNo]}")
        g.motorKi[self.motorNo] = val
    except:
      pass

    return g.motorKi[self.motorNo]
  

  def setKdFunc(self, kd_val_str):
    try:
      if kd_val_str:
        isSuccessful = g.serClient.send(f"kd{g.motorLabel[self.motorNo]}", float(kd_val_str))
        val = g.serClient.get(f"kd{g.motorLabel[self.motorNo]}")
        g.motorKd[self.motorNo] = val
    except:
      pass

    return g.motorKd[self.motorNo]
  

  def setCfFunc(self, cf_val_str):
    try:
      if cf_val_str:
        isSuccessful = g.serClient.send(f"f0{g.motorLabel[self.motorNo]}", float(cf_val_str))
        val = g.serClient.get(f"f0{g.motorLabel[self.motorNo]}")
        g.motorCf[self.motorNo] = val
    except:
      pass

    return g.motorCf[self.motorNo]
  

  def setMaxVelFunc(self, vel_val_str):
    try:
      if vel_val_str:
        g.motorMaxVel[self.motorNo] = float(vel_val_str)
    except:
      pass

    return g.motorMaxVel[self.motorNo]
  

  def setTargetVelFunc(self, vel_val_str):
    try:
      if vel_val_str:
        g.motorTargetVel[self.motorNo] = float(vel_val_str)
    except:
      pass

    return g.motorTargetVel[self.motorNo]
  

  def selectSignalFunc(self, signal_val_str):
    try:
      if signal_val_str:
        g.motorTestSignal[self.motorNo] = signal_val_str
    except:
      pass

    return g.motorTestSignal[self.motorNo]
  

  def selectDurationFunc(self, duration_val_str):
    try:
      if duration_val_str:
        val = int(duration_val_str)
        g.motorTestDuration[self.motorNo] = val
    except:
      pass

    return g.motorTestDuration[self.motorNo]























# import time
# from global_var_and_func import g, SetDataCardFrame, ChooseDataCardFrame, signalTypes, selectSignal
# import customtkinter



# def setKpA(text):
#   try:
#     if text:
#       isSuccessful = g.serClient.send("kpA", float(text))
#       val = g.serClient.get("kpA")
#       g.kpA = val
#   except:
#     pass

#   return g.kpA


# def setKiA(text):
#   try:
#     if text:
#       isSuccessful = g.serClient.send("kiA", float(text))
#       val = g.serClient.get("kiA")
#       g.kiA = val
#   except:
#     pass

#   return g.kiA


# def setKdA(text):
#   try:
#     if text:
#       isSuccessful = g.serClient.send("kdA", float(text))
#       val = g.serClient.get("kdA")
#       g.kdA = val
#   except:
#     pass

#   return g.kdA


# def setCtrlVelA(text):
#   try:
#     if text:
#       val = float(text)
#       g.ctrlVelA = val
#   except:
#     pass

#   return g.ctrlVelA

















# class MotorAGraphCanvas(customtkinter.CTkFrame):
#   def __init__(self, parentFrame):
#     super().__init__(parentFrame)

#     # graph parameters
#     self.w = 720
#     self.h = 400
#     self.xStartOffsetPnt = 40
#     self.xStopOffsetPnt = 20
#     self.yStopOffsetPnt = 20
#     self.xAxisLen = self.w - self.xStartOffsetPnt - self.xStopOffsetPnt
#     self.yAxisLen = self.h - (2*self.yStopOffsetPnt)
#     self.initStartPnt = (self.xStartOffsetPnt, self.h/2) # x,y


#     self.clearPlot = False
#     self.doPlot = False
#     self.doPlotTime = time.time()
#     self.doPlotDuration = g.motorAOnDuration

#     self.currTime = 0.0
#     self.prevTime = 0.0
#     self.t = time.time()

#     self.currValA = 0.0
#     self.currValB = 0.0
#     self.prevValA = 0.0
#     self.prevValB = 0.0

#     self.plotGraphBuffer = []
#     self.plotLineBufferA = []
#     self.plotLineBufferB = []

#     self.maxXVal = self.doPlotDuration

#     self.maxYVal = 2*g.maxVelA

#     self.xScale = self.xAxisLen/self.maxXVal
#     self.yScale = self.yAxisLen/self.maxYVal

#     self.signalType = 'step'


#     # add display label
#     self.text = f"targetVelA (rad/s) = {0.0}"
#     self.tagVelLabel = customtkinter.CTkLabel(self, text=self.text, text_color="blue", font=customtkinter.CTkFont(size=12, weight="bold"))
#     self.tagVelLabel.grid(row=0, column=0, padx=(5,5), pady=5, sticky="w")

#     self.text = f"filtVelA (rad/s) = {0.0}"
#     self.filtVelLabel = customtkinter.CTkLabel(self, text=self.text, text_color="red", font=customtkinter.CTkFont(size=12, weight="bold"))
#     self.filtVelLabel.grid(row=0, column=1, padx=(5,5), pady=5, sticky="w")

#     # add plot command button
#     self.plotButton = customtkinter.CTkButton(self, text="START PLOT", command=self.tryPlot)
#     self.plotButton.grid(row=0, column=2, padx=(20,5) , pady=5, ipadx=5, ipady=5)

#     # add graghical canvas
#     self.myCanvas = customtkinter.CTkCanvas(master=self, width=self.w, height=self.h, bg='white')

#     self.drawGraphicalLine(self.maxYVal)

#     self.myCanvas.grid(row=1, column=0, columnspan=3, padx=(0,0), pady=5)

#     self.myCanvas.after(1, self.plot_graph)



#   def drawGraphicalLine(self, maxYVal):
#     self.deleteGraphParams(self.plotGraphBuffer)

#     xAxisline = self.myCanvas.create_line(self.xStartOffsetPnt, self.h/2,
#                                           self.xStartOffsetPnt+self.xAxisLen+self.xStopOffsetPnt, self.h/2,
#                                           fill="black",width=2)
#     self.plotGraphBuffer.append(xAxisline)
#     text = self.myCanvas.create_text(self.xStartOffsetPnt+self.xAxisLen+(self.xStopOffsetPnt/2), (self.h/2)+15,
#                                     text="(sec)", fill="green", font=('Helvetica 7 bold'), angle=90.0)
#     self.plotGraphBuffer.append(text)
    
#     yAxisline = self.myCanvas.create_line(self.xStartOffsetPnt, 0,
#                                           self.xStartOffsetPnt, self.h,
#                                           fill="black",width=2)
#     self.plotGraphBuffer.append(yAxisline)
#     text = self.myCanvas.create_text(self.xStartOffsetPnt-15, self.yStopOffsetPnt/2,
#                                     text="(rad/s)", fill="green", font=('Helvetica 7 bold'))
#     self.plotGraphBuffer.append(text)
    
#     text = self.myCanvas.create_text(self.xStartOffsetPnt-15, self.h/2,
#                                     text="0.0", fill="black", font=('Helvetica 7 bold'))
#     self.plotGraphBuffer.append(text)

#     for i in range(1,6):
#       yTickVal = i/5*maxYVal*-1
#       xAxisline = self.myCanvas.create_line(self.xStartOffsetPnt, (self.h/2)-((self.yScale/2)*yTickVal),
#                                                  self.xStartOffsetPnt+self.xAxisLen+self.xStopOffsetPnt, (self.h/2)+(i/5*(self.yScale/2)*self.maxYVal),
#                                                  fill="grey",width=0.1, dash=(1,3))
#       self.plotGraphBuffer.append(xAxisline)
#       text = self.myCanvas.create_text(self.xStartOffsetPnt-15, (self.h/2)-((self.yScale/2)*yTickVal),
#                                 text=str(round(yTickVal/2, 2)), fill="black", font=('Helvetica 7 bold'))
#       self.plotGraphBuffer.append(text)

#     for i in range(1,6):
#       yTickVal = i/5*maxYVal
#       xAxisline = self.myCanvas.create_line(self.xStartOffsetPnt, (self.h/2)-((self.yScale/2)*yTickVal),
#                                                  self.xStartOffsetPnt+self.xAxisLen+self.xStopOffsetPnt, (self.h/2)-(i/5*(self.yScale/2)*self.maxYVal),
#                                                  fill="grey",width=0.1, dash=(1,3))
#       self.plotGraphBuffer.append(xAxisline)
#       text = self.myCanvas.create_text(self.xStartOffsetPnt-15, (self.h/2)-((self.yScale/2)*yTickVal),
#                                 text=str(round(yTickVal/2, 2)), fill="black", font=('Helvetica 7 bold'))
#       self.plotGraphBuffer.append(text)
    
#     for i in range(1,21):
#       xTickVal = i/20*self.maxXVal
#       yAxisline = self.myCanvas.create_line(self.xStartOffsetPnt+(self.xScale*xTickVal), 0,
#                                                self.xStartOffsetPnt+(self.xScale*xTickVal), self.h,
#                                                fill="grey",width=0.1, dash=(1,3))
#       self.plotGraphBuffer.append(yAxisline)
#       text = self.myCanvas.create_text(self.xStartOffsetPnt+(self.xScale*xTickVal), (self.h/2)+15,
#                                 text=str(round(xTickVal, 2)), fill="black", font=('Helvetica 7 bold'), angle=90.0)
#       self.plotGraphBuffer.append(text)
      


#   def setMaxVel(self, text):
#     try:
#       if self.clearPlot == True or self.doPlot == False:
#         if text:
#           val = float(text)
#           g.maxVelA = abs(val)
#           self.maxYVal = 2 * g.maxVelA
#           self.yScale = self.yAxisLen/self.maxYVal
#           self.drawGraphicalLine(self.maxYVal)
#     except:
#       pass

#     return g.maxVelA
  

#   def getSignalType(self):
#     return self.signalType
  

#   def setSignalType(self, text):
#     if self.clearPlot == True or self.doPlot == False:
#       self.signalType = text
#     return self.signalType
  

#   def tryPlot(self):
#     if self.clearPlot:
#         self.deletePlot(self.plotLineBufferA, self.plotLineBufferB)
#         self.plotButton.configure(text='START PLOT')
#         self.clearPlot = False
#         time.sleep(0.1)

#     elif self.doPlot:
#         self.doPlot = False 
#         # print('stop plot')
#     else:
#         self.doPlot = True 
#         self.doPlotTime = time.time()
#         # print('start plot')
    

#   def deleteGraphParams(self, graphParams):
#       for param in graphParams:
#           self.myCanvas.delete(param)
#           # root.update_idletasks()
#       self.plotGraphBuffer = []

#   def deletePlot(self, linesA, linesB):
#       for lineA in linesA:
#           self.myCanvas.delete(lineA)
#           # root.update_idletasks()
#       for lineB in linesB:
#           self.myCanvas.delete(lineB)
#           # root.update_idletasks()
#       self.plotLineBufferA = []
#       self.plotLineBufferB = []


#   def plot_graph(self):
      
#       if self.doPlot and self.doPlotDuration < time.time()-self.doPlotTime:
#           if g.motorAIsOn:
#             isSuccess = g.serClient.send("tag", 0, 0)
#             isSuccessful = g.serClient.send("mode", 0)
#             if isSuccess:
#               g.motorAIsOn = False
#               # print('Motor off', isSuccess)
#           self.doPlot = False 
#           self.clearPlot = True
#           self.plotButton.configure(text='CLEAR PLOT')
#           self.currValA = 0.0
#           self.prevValA = 0.0
#           self.currValB = 0.0
#           self.prevValB = 0.0
#           self.currTime = 0.0
#           self.prevTime = 0.0
#           self.t = time.time()
#           # print('stop plot')
#           self.myCanvas.after(1, self.plot_graph)

#       elif self.doPlot:
#           targetVel =selectSignal(type=self.signalType,targetMax=g.ctrlVelA, duration=self.doPlotDuration, deltaT=time.time()-self.doPlotTime)
          
#           if not g.motorAIsOn:
#             isSuccessful = g.serClient.send("mode", 1)
#             isSuccess = g.serClient.send("tag", targetVel, 0)
#             if isSuccess:
#               g.motorAIsOn = True
#               # print('Motor on', isSuccess)
#           isSuccess = g.serClient.send("tag", targetVel, 0)

#           try:
#             g.targetA, g.filtAngVelA = g.serClient.get("pVelA")
#           except:
#             pass

#           self.currValA = g.targetA
#           self.currValB = g.filtAngVelA
#           self.currTime = time.time()-self.t

#           lineA = self.myCanvas.create_line(self.xStartOffsetPnt+(self.prevTime*self.xScale),-self.yScale*self.prevValA+self.h/2,
#                                            self.xStartOffsetPnt+(self.currTime*self.xScale), -self.yScale*self.currValA+self.h/2,
#                                            fill="blue", width=1.25)
#           lineB = self.myCanvas.create_line(self.xStartOffsetPnt+(self.prevTime*self.xScale),-self.yScale*self.prevValB+self.h/2,
#                                            self.xStartOffsetPnt+(self.currTime*self.xScale), -self.yScale*self.currValB+self.h/2,
#                                            fill="red", width=1.25)
          
#           self.text = f"targetVelA (rad/s) = {g.targetA}"
#           self.tagVelLabel.configure(text=self.text)

#           self.text = f"filtVelA (rad/s) = {g.filtAngVelA}"
#           self.filtVelLabel.configure(text=self.text)

#           self.plotButton.configure(text='STOP PLOT')

#           self.plotLineBufferA.append(lineA)
#           self.plotLineBufferB.append(lineB)
#           # root.update_idletasks()

#           self.prevValA = self.currValA
#           self.prevValB = self.currValB

#           self.prevTime = self.currTime
          
#           self.myCanvas.after(1, self.plot_graph)

#       else:
#           if g.motorAIsOn:
#             isSuccess = g.serClient.send("tag", 0, 0)
#             isSuccessful = g.serClient.send("mode", 0)
#             if isSuccess:
#               self.clearPlot = True
#               self.plotButton.configure(text='CLEAR PLOT')
#               g.motorAIsOn = False
#               # print('Motor off', isSuccess)
#           self.currValA = 0.0
#           self.prevValA = 0.0
#           self.currValB = 0.0
#           self.prevValB = 0.0
#           self.currTime = 0.0
#           self.prevTime = 0.0
#           self.t = time.time()
#           self.myCanvas.after(1, self.plot_graph)













# class MotorAPidSetupFrame(customtkinter.CTkFrame):
#   def __init__(self, parent):
#     super().__init__(parent)

#     self.grid_columnconfigure((0,1,2), weight=0)
#     self.grid_rowconfigure((0,1,2,3,4,5,6), weight=0)

#     self.motorAGraphCanvas = MotorAGraphCanvas(self)

#     # add heading
#     self.heading = customtkinter.CTkLabel(self, text="MOTOR A PID CONTROL SETUP", font=customtkinter.CTkFont(size=24, weight="bold", underline=False))
#     self.heading.grid(row=0, column=0, columnspan=3, padx=10, pady=(5,25))

#     # add set card frame
#     g.kpA = g.serClient.get("kpA")
#     self.setKpCardFrame = SetDataCardFrame(self, "KP", g.kpA,
#                                            placeHolderText="enter KP",
#                                            set_func=setKpA)
#     self.setKpCardFrame.grid(row=1, column=0, padx=(20,10), pady=10)

#     g.kiA = g.serClient.get("kiA")
#     self.setKiCardFrame = SetDataCardFrame(self, "KI", g.kiA,
#                                            placeHolderText="enter KI",
#                                            set_func=setKiA)
#     self.setKiCardFrame.grid(row=1, column=1, padx=10, pady=10)

#     g.kdA = g.serClient.get("kdA")
#     self.setKdCardFrame = SetDataCardFrame(self, "KD", g.kdA,
#                                            placeHolderText="enter KD",
#                                            set_func=setKdA)
#     self.setKdCardFrame.grid(row=1, column=2, padx=10, pady=10)


#     self.motorAGraphCanvas.setSignalType(signalTypes[0])
#     self.chooseFiltOrderFrame = ChooseDataCardFrame(self, "SIGNAL_TYPE", self.motorAGraphCanvas.getSignalType(),
#                                                     input_values=signalTypes,
#                                                     set_func=self.motorAGraphCanvas.setSignalType)
#     self.chooseFiltOrderFrame.grid(row=2, column=0, padx=10, pady=10)

#     self.setMaxVelFrame = SetDataCardFrame(self, "MAX_VEL(rad/s)", g.maxVelA,
#                                                    placeHolderText="enter Max Vel",
#                                                    set_func=self.motorAGraphCanvas.setMaxVel)
#     self.setMaxVelFrame.grid(row=2, column=1, padx=10, pady=10)

#     self.setMaxVelFrame = SetDataCardFrame(self, "TARGET_VEL(rad/s)", g.ctrlVelA,
#                                                    placeHolderText="enter target vel",
#                                                    set_func=setCtrlVelA)
#     self.setMaxVelFrame.grid(row=2, column=2, padx=10, pady=10)


#     # add canvas
#     # self.motorAGraphCanvas = MotorAGraphCanvas(self)
#     self.motorAGraphCanvas.grid(row=3, column=0, columnspan=3, padx=5, pady=5)
    