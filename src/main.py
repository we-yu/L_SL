# coding: UTF-8
import sys
import tkinter as tk
# ---
import GUICtrl

windowTitle = 'WindowTitle'
windowWidth = '800'
windowHeight = '600'

gCtrl = GUICtrl.GUIController(windowTitle, windowWidth, windowHeight)
# ----------------------
# gCtrl.IconLoader()
# ----------------------
gCtrl.ShowWindow()


# class MainApplication(tk.Frame):
#     def __init__(self, parent, *args, **kwargs):
#         tk.Frame.__init__(self, parent, *args, **kwargs)
#         self.parent = parent
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     MainApplication(root).pack(side="top", fill="both", expand=True)
#     root.mainloop()
