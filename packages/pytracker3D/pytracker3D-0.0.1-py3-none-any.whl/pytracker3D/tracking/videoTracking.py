import cv2
import numpy as np
import pandas as pd
import os
from PyQt5.QtWidgets import QMessageBox

class VideoTracking():
    
    def __init__(self,MainWindow):
        self.MainWindow=MainWindow
        self.path, self.basename=os.path.split(os.path.abspath(self.MainWindow.video))
        self.filename=os.path.splitext(self.basename)[0]
 
    def blockRegion(self,img):
        if self.MainWindow.blockRegion1_cb.isChecked()==True:              
            cv2.rectangle(img, (self.blockOriginx_region1,self.blockOriginy_region1),(self.blocktopx_region1,self.blocktopy_region1), 100,-1)
        if self.MainWindow.blockRegion2_cb.isChecked()==True:
            cv2.rectangle(img, (self.blockOriginx_region2,self.blockOriginy_region2),(self.blocktopx_region2,self.blocktopy_region2), 100,-1)
        return img

    def preview(self):
        cap = cv2.VideoCapture(self.MainWindow.video)
        self.MainWindow.track_TE.append("Playing preview. Click video window and press 'q' or click 'Stop' button to cancel")
        
        while(True):
            (grabbed, frame) = cap.read()
            
            if not grabbed:
                break                 
            currentframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width = currentframe.shape[:2]
            cv2.namedWindow("Preview", cv2.WINDOW_NORMAL) 
            cv2.imshow("Preview",currentframe)  
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break  
        cap.release()
        cv2.destroyAllWindows()  

    def selectVideoBounds(self):
        cap = cv2.VideoCapture(self.MainWindow.video)
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        def onChange(trackbarValue):
            cap.set(cv2.CAP_PROP_POS_FRAMES,trackbarValue)
            err,img = cap.read()
            cv2.imshow("mywindow", img)
            pass

        cv2.namedWindow('mywindow')
        cv2.createTrackbar( 'start', 'mywindow', 0, length, onChange )
        cv2.createTrackbar( 'end'  , 'mywindow', 100, length, onChange )

        onChange(0)
        cv2.waitKey()
        
        self.start = cv2.getTrackbarPos('start','mywindow')
        self.end   = cv2.getTrackbarPos('end','mywindow')
        self.MainWindow.start_l.setText(str(self.start))
        self.MainWindow.end_l.setText(str(self.end))
         
        cap.release()
        cv2.destroyAllWindows()    

    def trackVideo(self):
        self.blocktopx_region1 = int(self.MainWindow.le_topx_region1.text())
        self.blocktopy_region1 = int(self.MainWindow.le_topy_region1.text())
        self.blockOriginx_region1 = int(self.MainWindow.le_originx_region1.text())
        self.blockOriginy_region1 = int(self.MainWindow.le_originy_region1.text())
        self.blocktopx_region2 = int(self.MainWindow.le_topx_region2.text())
        self.blocktopy_region2 = int(self.MainWindow.le_topy_region2.text())
        self.blockOriginx_region2 = int(self.MainWindow.le_originx_region2.text())
        self.blockOriginy_region2 = int(self.MainWindow.le_originy_region2.text())
        self.cap = cv2.VideoCapture(self.MainWindow.video)
        self.firstFrame = None
        self.fgbg = cv2.createBackgroundSubtractorMOG2()

        count = 0
        xcoord=[]
        ycoord=[]
        frame=[]
        cx=0
        cy=0

        while(True):
            if count==0:
                self.MainWindow.track_TE.setText("Tracking. Click video window and press 'q' or click 'Stop' button to cancel")
            
            if self.MainWindow.trkTrack_B.isChecked()== False:
                self.MainWindow.trkTrack_B.setText('Track')
                break
            else:
                self.MainWindow.trkTrack_B.setText('Stop')
                
            (self.grabbed, self.frame) = self.cap.read()

            if not self.grabbed:
                self.MainWindow.trkTrack_B.setChecked(False)
                self.MainWindow.trkTrack_B.setText('Track')
                self.MainWindow.track_TE.append("Tracking complete!")
                self.MainWindow.track_TE.append("Raw pixel coordinate points saved to:")    
                self.MainWindow.track_TE.append("%s\\%s.csv" %(self.MainWindow.path,self.filename))                

                break
            
            rows,cols,ch = self.frame.shape
        
            ret=self.backgroundsubtraction()
            if ret:
                pass
            else:
                self.errMessage="Please specify a background image of identical pixel dimensions to video."
                self.errorTitle="Image matrix size error." 
                self.errorMsg()
                self.MainWindow.trkTrack_B.setText('Track')
                break
            
            self.filters()

            try:
                self.cntareathreshold=int(self.MainWindow.contourLineEdit.text())
            except AttributeError:
                cntareathreshold=100
            
            (_, cnts, _) = cv2.findContours(self.currentframe.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

            cntarea=[0]
            xcntcoord=[0]
            ycntcoord=[0]
            
            for c in cnts:
                if cv2.contourArea(c) < self.cntareathreshold:
                    continue
                
                cntarea.append(cv2.contourArea(c))
                (x, y, w, h) = cv2.boundingRect(c)
        
                M = cv2.moments(c)
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                
                xcntcoord.append(cx)
                ycntcoord.append(cy)
                self.MainWindow.track_TE.append("coutour area: %d" % float(cv2.contourArea(c)))
            
            self.start=int(self.MainWindow.start_l.text())
            self.end=int(self.MainWindow.end_l.text())            
            if count > self.end or count < self.start:
                self.MainWindow.track_TE.append("Animal not within frame limits.")  
            else:
                biggestcontour=cntarea.index(max(cntarea))
                xcoord.append(xcntcoord[biggestcontour])
                ycoord.append(ycntcoord[biggestcontour])
                frame.append(count)
                self.fishcoords=np.array((frame,xcoord,ycoord),dtype=float) 

            for i in range(len(xcoord)):
                if xcoord[i]==0:
                    pass
                else:
                    cv2.circle(self.frame, (xcoord[i], ycoord[i]),6, (0, 0, 255),thickness=-1)
                    if i == len(xcoord)-1:
                        self.MainWindow.track_TE.append("Detection on frame: %d" % count)
                        
            cv2.namedWindow("Background removed", cv2.WINDOW_NORMAL) 
            cv2.imshow("Background removed",self.currentframe)   

            if self.MainWindow.blockRegion1_cb.isChecked()==True:
                cv2.rectangle(self.frame,(self.blockOriginx_region1,self.blockOriginy_region1),(self.blocktopx_region1,self.blocktopy_region1), 100,-1)
            if self.MainWindow.blockRegion2_cb.isChecked()==True:
                cv2.rectangle(self.frame,(self.blockOriginx_region2,self.blockOriginy_region2),(self.blocktopx_region2,self.blocktopy_region2), 100,-1)
                
            cv2.namedWindow("Tracking", cv2.WINDOW_NORMAL)
            cv2.imshow("Tracking",self.frame)  

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.MainWindow.trkTrack_B.setChecked(False)
                self.MainWindow.trkTrack_B.setText('Track')
                break
            count = count +1
            
        self.cap.release()
        cv2.destroyAllWindows()
   
        try:
            os.mkdir(self.MainWindow.path+'\\'+'2DTracks')
        except WindowsError:
            pass
        try:
            self.fishcoords=np.transpose(self.fishcoords)
            self.fishcoords=pd.DataFrame(self.fishcoords)
            self.fishcoords.to_csv("%s\\2DTracks\\pixels_%s.csv" %(self.MainWindow.path,self.filename))
        except AttributeError:
            pass

    def backgroundsubtraction(self):
            if self.MainWindow.rb_MOG.isChecked() == True:
                self.currentframe = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                self.currentframe=self.blockRegion(self.currentframe)
                self.currentframe = self.fgbg.apply(self.currentframe)
                ret=True

            if self.MainWindow.rb_absolute.isChecked()==True:
                self.currentframe = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                self.blockRegion(self.currentframe)

                if self.firstFrame is None:
                    self.firstFrame = self.currentframe
                    
                if self.MainWindow.specify_background_cb.isChecked()==True:
                    try:
                        try:
                            self.firstFrame=self.MainWindow.background_img
                            self.firstFrame = cv2.cvtColor(self.firstFrame, cv2.COLOR_BGR2GRAY)
                            if self.MainWindow.specify_background_cb.isChecked()==True:
                                self.firstFrame=self.blockRegion(self.firstFrame)
                        except:
                            self.errMessage="Background image and video not of same dimensions."
                            self.errorTitle="Please specify the correct background image ..."
                            self.errorMsg()                                
                    except AttributeError:
                        self.errMessage="No background image specified."
                        self.errorTitle="Please specify a background iamge ..."
                        self.errorMsg()       
                        
                if self.firstFrame.shape[0] != self.currentframe.shape[0]:
                    ret=False
                    pass
                else:
                    self.frameDelta = cv2.absdiff(self.firstFrame, self.currentframe)
                    self.currentframe = cv2.threshold(self.frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
                    ret=True
                return ret
                     
    def filters(self):
            self.medianFiltersize=int(self.MainWindow.medianSlider.value())
            if self.medianFiltersize % 2 == 0:
                    self.medianFiltersize=self.medianFiltersize +1
            
            if self.MainWindow.medianFilterCheckbox.isChecked() == True:
                self.currentframe = cv2.medianBlur(self.currentframe,self.medianFiltersize)
            
            kernelsize=int(self.MainWindow.kernelSlider.value())
            if kernelsize % 2 == 0:
                    kernelsize=kernelsize +1
            kernel = np.ones((kernelsize,kernelsize),np.uint8)
            
            if self.MainWindow.erodeCheckbox.isChecked() == True:
                self.currentframe = cv2.erode(self.currentframe,kernel,iterations=1)
                
            if self.MainWindow.dilateCheckbox.isChecked() == True:
                self.currentframe = cv2.dilate(self.currentframe,kernel,iterations=1)
                
            if self.MainWindow.gaussCheckBox.isChecked() == True:
                self.gauss=int(self.MainWindow.gaussSlider.value())
                if self.gauss % 2 == 0:
                    self.gauss=self.gauss +1
                self.currentframe = cv2.GaussianBlur(self.currentframe, (self.gauss,self.gauss), 0)

    def errorMsg(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(self.errMessage)
        msg.setWindowTitle(self.errorTitle)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()       