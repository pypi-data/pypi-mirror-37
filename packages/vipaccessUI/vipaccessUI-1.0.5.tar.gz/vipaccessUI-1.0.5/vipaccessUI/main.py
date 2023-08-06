
#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Tkinter import Tk, Canvas, Frame, BOTH
import subprocess 
import Tkinter
import time
import vipaccess2.cli
import cStringIO
import sys


class VipAccessUI(Frame):
    copied=False
    pulled=False
    last_pull=time.time()
          
    def __init__(self,master=None):
        Frame.__init__(self, master)

        self.initUI()
        

    def clear_copy_ui(self):
        self.lbl.config(background="black")
        self.lbl.update()


    def set_copy_ui(self):
        self.lbl.config(background="darkgrey")
        self.lbl.update()


    def copy_text_to_clipboard(self,event):
        self.set_copy_ui()
        self.master.after(500, self.clear_copy_ui)
        field_value =self.get_token()
        self.master.clipboard_clear()  
        self.master.clipboard_append(field_value)  


    def get_token(self):
        stream = cStringIO.StringIO()
        sys.stdout = stream
        vipaccess2.cli.main()
        access_key= stream.getvalue()
        sys.stdout = sys.__stdout__
        return access_key.rstrip()

    def get_master_token(self):
        token=vipaccess2.cli.show_master_token()
        return token.rstrip()


    def task(self):
        time_in_period=(int(time.time() )% 30 )
        now = 30 - time_in_period
        width=250
        if time_in_period == 0:
            diff=time.time()-self.last_pull
            if diff>5:
                self.pulled=False
        
        percent_done=float(now)/30
        half_width=int(width/2)
        percent_in_pixels=float(percent_done*half_width)
        x1=half_width-percent_in_pixels
        x2=half_width+percent_in_pixels
        self.canvas.coords(self.percentage,x1, 0, x2   , 10)

        if False== self.pulled:
            self.lbl['text']=self.get_token()
            self.pulled=True
            self.last_pull=time.time()
        
        seconds_left_text="{} Seconds left".format(now)
        if self.seconds['text']!=seconds_left_text:
            self.seconds['text']=seconds_left_text
            
        self.master.after(100, self.task)  # reschedule event in 2 seconds


        
    def initUI(self):
        #app = tkinter.Frame(master=window,bg='black')
        self.pack_propagate(0) 
        self.master.title("VIP - Access Token")
        self.pack(fill=BOTH, expand=1)
        self.configure(background='black')
        master_token=self.get_master_token()
        self.cred_lbl = Tkinter.Label(self, text="Credential ID:",font=("MONO", 14),fg="WHITE",background="black", height=1)
        self.cred_lbl.pack()
        
        self.master_token = Tkinter.Label(self, text=master_token,font=("MONO", 24),fg="LIGHTBLUE",background="black", height=1)
        self.master_token.pack()
        

        self.canvas = Canvas(self,width=250,height=10,bg='black',bd=0, highlightthickness=0, relief='ridge')
        self.percentage=self.canvas.create_rectangle(0, 0, 0   , 10, outline="black", fill="orange")
        self.canvas.pack()

        self.lbl = Tkinter.Label(self, text="",font=("MONO", 24),fg="WHITE",background="black", height=1)
        self.lbl.pack()
        self.lbl.bind("<Button-1>", self.copy_text_to_clipboard)  

        self.seconds = Tkinter.Label(self, text="",fg="WHITE",background="black",font=("MONO", 14))
        self.seconds.pack()

        self.master.after(200, self.task)
        # TODO get correct key bind. its not <Q>
        #self.master.bind("<Q>", lambda e: self.master.destroy())




def main():
  
    window = Tkinter.Tk()
    window.resizable(0, 0) #Don't allow resizing in the x or y direction
    window.geometry("250x160")
    VipAccessUI()
    window.mainloop()





if __name__ == '__main__':
    main()  