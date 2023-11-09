import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *


class MotorDrawFrame(tb.Frame):
  def __init__(self, parentFrame):
    super().__init__(master=parentFrame)

    self.displayFrame = tb.Frame(self)
    self.canvasFrame = tb.Frame(self)

    self.textFrame1 = tb.Frame(self.displayFrame)
    self.textFrame2 = tb.Frame(self.displayFrame)
    

    #create widgets to be added to the textFame
    buttonStyle = tb.Style()
    buttonStyleName = 'danger.TButton'
    buttonStyle.configure(buttonStyleName, font=('Monospace',10, 'bold'))

    self.posText = tb.Label(self.textFrame1, text="POS(rad):", font=('Monospace',10, 'bold') ,bootstyle="danger")
    self.posVal = tb.Label(self.textFrame1, text="3.142", font=('Monospace',10), bootstyle="dark")

    self.velText = tb.Label(self.textFrame2, text="VEL(rad/s):", font=('Monospace',10, 'bold') ,bootstyle="primary")
    self.velVal = tb.Label(self.textFrame2, text="6.284", font=('Monospace',10), bootstyle="dark")

    self.button1 = tb.Button(self.displayFrame, text="RESET HAND", style=buttonStyleName)
    self.button2 = tb.Button(self.displayFrame, text="CTRL MOTOR", style=buttonStyleName)

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

    self.canvas.create_line((0, 0), (100, 100), width=1, fill='red')
    self.canvas.create_rectangle((100, 100), (200, 200), fill='blue')


    # add displayFrame and canvasFrame to GraphFrame
    self.displayFrame.pack(side='top', expand=True, fill='x', padx=10)
    self.canvasFrame.pack(side='top', expand=True, fill='both', pady=(10,0))



