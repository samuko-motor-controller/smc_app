import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

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
    self.setPulsePerRev = SetValueFrame(self.frame1, keyTextInit="PPR_A: ", valTextInit="990")
    self.selectWheelConfig = SelectValueFrame(self.frame1, keyTextInit="DIR_A: ", valTextInit="left-wheel")
    self.setTestPwm = SetValueFrame(self.frame1, keyTextInit="TEST_PWM: ", valTextInit="100")
    self.selectDuration = SelectValueFrame(self.frame1, keyTextInit="TEST_TIME(sec): ", valTextInit="20")

    #add framed widgets to frame1
    self.setPulsePerRev.grid(row=0, column=0, sticky='nsew', padx=5)
    self.selectWheelConfig.grid(row=0, column=1, sticky='nsew', padx=5)
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

