import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

from components.SetValueFrame import SetValueFrame
from components.SelectValueFrame import SelectValueFrame
from components.GraphFrame import GraphFrame




class PidSetupFrame(tb.Frame):
  def __init__(self, parentFrame):
    super().__init__(master=parentFrame)

    self.label = tb.Label(self, text="MOTOR A PID SETUP", font=('Monospace',16, 'bold') ,bootstyle="dark")

    self.frame1 = tb.Frame(self)
    self.frame2 = tb.Frame(self)

    # configure grid for frame1
    self.frame1.grid_columnconfigure((0,1,2,3), weight=1, uniform='a')
    self.frame1.grid_rowconfigure((0,1), weight=1, uniform='a')


    #create widgets to be added to frame1
    self.setKp = SetValueFrame(self.frame1, keyTextInit="KP_A: ", valTextInit="400.75")
    self.setKi = SetValueFrame(self.frame1, keyTextInit="KI_A: ", valTextInit="1500.00")
    self.setKd = SetValueFrame(self.frame1, keyTextInit="KD_A: ", valTextInit="20.50")
    self.setCf = SetValueFrame(self.frame1, keyTextInit="CF_A(Hz): ", valTextInit="1.5")

    self.setMaxVel = SetValueFrame(self.frame1, keyTextInit="MAX(rad/s): ", valTextInit="200.00")
    self.setTargetVel = SetValueFrame(self.frame1, keyTextInit="TARGET(rad/s): ", valTextInit="6.284")
    self.selectSignalType = SelectValueFrame(self.frame1, keyTextInit="TEST_SIGNAL: ", valTextInit="step")
    self.selectDuration = SelectValueFrame(self.frame1, keyTextInit="TEST_TIME(sec): ", valTextInit="20")


    #add framed widgets to frame1
    self.setKp.grid(row=0, column=0, sticky='nsew', padx=5, pady=(0,10))
    self.setKi.grid(row=0, column=1, sticky='nsew', padx=5, pady=(0,10))
    self.setKd.grid(row=0, column=2, sticky='nsew', padx=5, pady=(0,10))
    self.setCf.grid(row=0, column=3, sticky='nsew', padx=5, pady=(0,10))
  
    self.setMaxVel.grid(row=1, column=0, sticky='nsew', padx=5)
    self.setTargetVel.grid(row=1, column=1, sticky='nsew', padx=5)
    self.selectSignalType.grid(row=1, column=2, sticky='nsew', padx=5)
    self.selectDuration.grid(row=1, column=3, sticky='nsew', padx=5)


    #create widgets to be added to frame2
    self.graph = GraphFrame(self.frame2)

    #add framed widgets to frame2
    self.graph.pack(side="left", expand=True, fill="both", padx=5)


    #add frame1, frame2 and frame3 to MainFrame
    self.label.pack(side="top", fill="x", padx=(200,0), pady=(5,0))
    self.frame1.pack(side="top", expand=True, fill="x")
    self.frame2.pack(side="top", expand=True, fill="both", pady=(20, 0))
