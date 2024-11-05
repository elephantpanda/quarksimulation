'''WX TEMPLATE'''

import wx
import random
import math

class Quark:
    pos = []
    vel = []
    RGBW = [0,0.5,0]

#up     [1,1,-1,-1] +2/3
#down   [1,1,-1, 1] -1/3
#e      [1,1,1,-1]
#v      [1,1,1,1]


class MyForm(wx.Frame):

    quarks=[]
 

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "QUARKS")
        self.SetInitialSize((1600,1080))
        self.SetPosition((0,0))
        self.SetFocus()

       
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.timer = wx.Timer(self, 101)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBack)
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)
        self.Setup()
        self.timer.Start(1)    # 1 second  # 40 about realtime

    def Setup(self):
        w=800
        s=0
        for i in range(0,24):
            q=Quark()
            q.pos = [random.randrange(-w,w),random.randrange(-w,w)]
            q.vel = [random.uniform(-s,s),random.uniform(-s,s)]
            n=i%6
            p=1
            #if i%6>=3: p=-1
            
            if n==0:
                q.RGB = [p,-p,-p,-p]     
            elif n==1:
                q.RGB = [-p,p,-p,-p]
            elif n==2:
                q.RGB = [-p,-p,p,-p]
            #elif n==3:
            #    q.RGB = [-p,-p,-p,p]
            elif n==3:
                q.RGB = [-p,p,p,p]     
            elif n==4:
                q.RGB = [p,-p,p,p]
            elif n==5:
                q.RGB = [p,p,-p,p]
            '''
            if n==0:
                q.RGB = [p,-p,-p,-p]     
            elif n==1:
                q.RGB = [-p,p,p,p]
            '''
            self.quarks.append(q)


    clear=False

    def onKeyPress(self,event):
        keycode = event.GetUnicodeKey()
        print(keycode)
        if keycode==32:
            self.clear=True
            self.quarks = []
            self.Setup()
        pass

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        dc.SetBackground(wx.Brush("green"))
        self.DrawAll(dc)

   

    def DrawAll(self,dc):
        dc.SetBrush(wx.BLACK_BRUSH)
        if self.clear:
            dc.DrawRectangle(0,0,2000,1000)
            self.clear = False
        mx = 800
        my = 400
        s = 0.05
        dc.SetPen(wx.TRANSPARENT_PEN)
        for i in range(0,len(self.quarks)):
            q1=self.quarks[i]
            if q1.RGB[0]==q1.RGB[1] and q1.RGB[1]==q1.RGB[2]:
                 dc.SetBrush(wx.WHITE_BRUSH)   
            elif q1.RGB[0]<0 or q1.RGB[1]<0 or q1.RGB[2]<0:
                dc.SetBrush(wx.Brush(wx.Colour(255+q1.RGB[0]*255, 255+q1.RGB[1]*255, 255+q1.RGB[2]*255)))
            else:
                dc.SetBrush(wx.Brush(wx.Colour(q1.RGB[0]*255, q1.RGB[1]*255, q1.RGB[2]*255)))
            dc.DrawCircle(mx+s*q1.pos[0], my+s*q1.pos[1],3)

    def OnEraseBack(self,event):
        pass

    def OnClose(self, event):
        print("Exiting..")
        self.timer.Stop()
        self.Destroy()


    def OnTimer(self, event):
        s2=0.1
        L=len(self.quarks)
        for i in range(0,L):
            for j in range(0,L):
                q1 = self.quarks[i]
                q2 = self.quarks[j]
                R1 = q1.RGB[0]
                G1 = q1.RGB[1]
                B1 = q1.RGB[2]
                W1 = q1.RGB[3]
                R2 = q2.RGB[0]
                G2 = q2.RGB[1]
                B2 = q2.RGB[2]
                W2 = q2.RGB[3]
                #force?
                F = -(2*R1*R2+2*G1*G2+2*B1*B2 - R1*G2-R2*G1 - G1*B2-B1*G2 - B1*R2-B2*R1 )
                #electromagnetic
                Q2 = (R1+G1+B1-3*W1)*(R2+G2+B2-3*W2)
                if i!=j:
                    dx = q1.pos[0]-q2.pos[0]
                    dy = q1.pos[1]-q2.pos[1]
                    r = math.pow(math.sqrt(dx*dx+dy*dy),1)
                    dir = [dx/r,dy/r]
                    
                    q1.vel[0]-=dir[0]*F*math.tanh(r) - dir[0]/(r)*Q2*10
                    q1.vel[1]-=dir[1]*F*math.tanh(r) - dir[1]/(r)*Q2*10

        for i in range(0,L):
            q1 = self.quarks[i]
            q1.pos[0]+=q1.vel[0]*s2
            q1.pos[1]+=q1.vel[1]*s2
        self.Refresh()
        


# Run the program
if __name__ == "__main__":
    global frame
    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()