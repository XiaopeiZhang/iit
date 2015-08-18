import csv,glob,os
from Tkinter import *
import tkMessageBox
#import Tkinter

class Application(Frame):

    def __init__(self,master):
        Frame.__init__(self,master)
        self.pack()
        self.createWidgets()
        self.warning='Finished \n'

    def createWidgets(self):
        self.label1=Label(self,text='Please input the directory under which all the folders with cvs files exist')
        self.label1.pack()
        self.label2=Label(self,text='e.g., if color_0_off_d65_20_60cm folder is in the folder called Result')
        self.label2.pack()
        self.label3=Label(self,text='Input path below:      C:\...\...\Result')
        self.label3.pack()

        self.entry=Entry(self,width=50)
        self.entry.pack()
        self.menu=Menu(self,tearoff=0)
        self.menu.add_command(label='Cut',command=lambda: self.event_generate('<Control-x>'))
        self.menu.add_separator()
        self.menu.add_command(label='Copy',command=lambda: self.event_generate('<Control-c>'))
        self.menu.add_separator()
        self.menu.add_command(label='Paste',command=lambda: self.event_generate('<Control-v>'))
        def popup(event):
            self.menu.post(event.x_root,event.y_root)
        self.entry.bind("<Button-3>",popup)


        self.label4=Label(self,text='Please check the boxes below to choose the dataset you need')
        self.label4.pack()

        self.CheckVar1=IntVar()
        self.c1=Checkbutton(self,text='Raw Data Color and Raw Data Noise & SNR',variable=self.CheckVar1,onvalue=1,offvalue=0)
        self.CheckVar2=IntVar()
        self.c2=Checkbutton(self,text='Raw Data Color Flash',variable=self.CheckVar2,onvalue=1,offvalue=0)
        self.CheckVar3=IntVar()
        self.c3=Checkbutton(self,text='Raw Data Uniformity',variable=self.CheckVar3,onvalue=1,offvalue=0)
        self.CheckVar4=IntVar()
        self.c4=Checkbutton(self,text='Raw Data Resolution',variable=self.CheckVar4,onvalue=1,offvalue=0)
        self.c1.pack()
        self.c2.pack()
        self.c3.pack()
        self.c4.pack()

        self.label5=Label(self,text='If re-generate report_helper_rear.csv or report_helper_front.csv')
        self.label5.pack()
        self.label6=Label(self,text='Please close previously generated ones')
        self.label6.pack()

        self.button1=Button(self,text='Get Rear csv dataset',command=self.getRear)
        self.button1.pack(side=LEFT)
        self.button2=Button(self,text='Get Front csv dataset',command=self.getFront)
        self.button2.pack(side=RIGHT)

    def getRear(self):
        print 'rear'
        directory=self.entry.get()
        if not directory or not os.path.isdir(directory):
            tkMessageBox.showinfo('Warning','Please input valid directory')
        elif self.CheckVar1.get()==0 and self.CheckVar2.get()==0 and self.CheckVar3.get()==0 and self.CheckVar4.get()==0:
            tkMessageBox.showinfo('Warning','Please choose at least one test result you need')
        else:
            self.warning='Finished \n'
            rearOutput=[]
            rearOutput.append(['REAR'])
            rearOutput.append([])
            rearOutput.append([])
            rearOutput.append([])

            if self.CheckVar1.get()==1:
                rearOutput.append(['Raw Data Color'])
                rearOutput.append(['2800K,>500lux','','4100K,20lux','','4100K,100lux','','4100K,>500lux','','6500K,20lux','','6500K,100lux','','6500K,>500lux'])
                rearOutput.append(['a*','b*','a*','b*','a*','b*','a*','b*','a*','b*','a*','b*','a*','b*'])
                rearOutput.append(['Copy Starts Here**********************'])
                rearOutput.append([])
                raw_data=[[] for i in range(24)]
                rs1=self.getBestColor(directory+'\color_0_off_halogen_700_60cm')
                if rs1:
                    for i in range(24):
                        raw_data[i]+=rs1[i]
                rs2=self.getBestColor(directory+'\color_0_off_f11_20_60cm')
                if rs2:
                    for i in range(24):
                        raw_data[i]+=rs2[i]
                rs3=self.getBestColor(directory+'\color_0_off_f11_100_60cm')
                if rs3:
                    for i in range(24):
                        raw_data[i]+=rs3[i]
                rs4=self.getBestColor(directory+'\color_0_off_f11_700_60cm')
                if rs4:
                    for i in range(24):
                        raw_data[i]+=rs4[i]
                rs5=self.getBestColor(directory+'\color_0_off_d65_20_60cm')
                if rs5:
                    for i in range(24):
                        raw_data[i]+=rs5[i]
                rs6=self.getBestColor(directory+'\color_0_off_d65_100_60cm')
                if rs6:
                    for i in range(24):
                        raw_data[i]+=rs6[i]
                rs7=self.getBestColor(directory+'\color_0_off_d65_700_60cm')
                if rs7:
                    for i in range(24):
                        raw_data[i]+=rs7[i]
                rearOutput+=raw_data
                rearOutput.append([])
                rearOutput.append(['Copy Ends Here**********************'])
                rearOutput.append([])
                rearOutput.append([])
                rearOutput.append([])


                

                
            if self.CheckVar2.get()==1:
                rearOutput.append(['Raw Data Color Flash'])
                rearOutput.append(['2800K,10>lux','','4100K,10lux','','6500K,20lux','','0lux',''])
                rearOutput.append(['a*','b*','a*','b*','a*','b*','a*','b*'])
                rearOutput.append(['Copy Starts Here**********************'])
                rearOutput.append([])
                flash_data=[[] for i in range(24)]
                rs11=self.getBestColor(directory+'\color_0_on_f12_10_60cm')
                if rs11:
                    for i in range(24):
                        flash_data[i]+=rs11[i]
                rs12=self.getBestColor(directory+'\color_0_on_f11_10_60cm')
                if rs12:
                    for i in range(24):
                        flash_data[i]+=rs12[i]
                rs13=self.getBestColor(directory+'\color_0_on_d65_10_60cm')
                if rs13:
                    for i in range(24):
                        flash_data[i]+=rs13[i]
                rs14=self.getBestColor(directory+'\color_0_on_f12_0_60cm')
                if rs14:
                    for i in range(24):
                        flash_data[i]+=rs14[i]
                rearOutput+=flash_data
                rearOutput.append([])
                rearOutput.append(['Copy Ends Here**********************'])
                rearOutput.append([])
                rearOutput.append([])
                rearOutput.append([])

            if self.CheckVar1.get()==1:

                rearOutput.append(['Raw Data Noise & SNR'])
                rearOutput.append(['The order below: d65_20lux, d65_100lux and d65_700lux'])
                rearOutput.append(['Red','','','Green','','','Blue','','','Y','','','Cb','','','Cr'])
                rearOutput.append(['Ave','Stdev','SNR','Ave','Stdev','SNR','Ave','Stdev','SNR','Ave','Stdev','SNR','Ave','Stdev','SNR','Ave','Stdev','SNR'])
                rearOutput.append(['Copy Starts Here**********************'])
                rearOutput.append([])
                rs8=self.getSNR(directory+'\color_0_off_d65_20_60cm')
                if rs8:
                    rearOutput+=rs8
                rearOutput.append([])
                rearOutput.append([])
                rearOutput.append(['Red','','','Green','','','Blue','','','Y','','','Cb','','','Cr'])
                rearOutput.append(['Ave','Stdev','SNR','Ave','Stdev','SNR','Ave','Stdev','SNR','Ave','Stdev','SNR','Ave','Stdev','SNR','Ave','Stdev','SNR'])
                rs9=self.getSNR(directory+'\color_0_off_d65_100_60cm')
                if rs9:
                    rearOutput+=rs9
                rearOutput.append([])
                rearOutput.append([])
                rearOutput.append(['Red','','','Green','','','Blue','','','Y','','','Cb','','','Cr'])
                rearOutput.append(['Ave','Stdev','SNR','Ave','Stdev','SNR','Ave','Stdev','SNR','Ave','Stdev','SNR','Ave','Stdev','SNR','Ave','Stdev','SNR'])
                rs10=self.getSNR(directory+'\color_0_off_d65_700_60cm')
                if rs10:
                    rearOutput+=rs10
                rearOutput.append([])
                rearOutput.append(['Copy Ends Here**********************'])
                rearOutput.append([])
                rearOutput.append([])
                rearOutput.append([])


                
            if self.CheckVar3.get()==1:
                rearOutput.append(['Raw Data Uniformity'])
                rearOutput.append(['The order below: f12, f11, d65, and halogen'])
                rearOutput.append(['Copy Starts Below the First Luma**********************'])
                rearOutput.append([])
                rs15=self.getBestUniformity(directory+'\uniformity_0_off_f12_700_120cm')
                if rs15:
                    rearOutput+=rs15
                rearOutput.append([])
                rs16=self.getBestUniformity(directory+'\uniformity_0_off_f11_700_120cm')
                if rs16:
                    rearOutput+=rs16
                rearOutput.append([])
                rs17=self.getBestUniformity(directory+'\uniformity_0_off_d65_700_120cm')
                if rs17:
                    rearOutput+=rs17
                rearOutput.append([])
                rs18=self.getBestUniformity(directory+'\uniformity_0_off_halogen_700_120cm')
                if rs18:
                    rearOutput+=rs18
                rearOutput.append([])
                rearOutput.append(['Copy Ends Here**********************'])
                rearOutput.append([])
                rearOutput.append([])
                rearOutput.append([])

                
            if self.CheckVar4.get()==1:
                rearOutput.append(['Raw Data Resolution'])
                rearOutput.append(['The order below: 700lux_10cm, 700lux_60cm, 20lux_60cm, 700lux_120cm, and 700lux_400cm'])
                rearOutput.append(['Copy Starts Here**********************'])
                rearOutput.append([])
                rs19=self.getBestSFR(directory+'\sfr_0_off_d65_700_10cm')
                if rs19:
                    rearOutput+=rs19
                rearOutput.append([])
                rearOutput.append([])
                rs20=self.getBestSFR(directory+'\sfr_0_off_d65_700_60cm')
                if rs20:
                    rearOutput+=rs20
                rearOutput.append([])
                rs21=self.getBestSFR(directory+'\sfr_0_off_d65_20_60cm')
                if rs21:
                    rearOutput+=rs21
                rearOutput.append([])
                rs22=self.getBestSFR(directory+'\sfr_0_off_d65_700_120cm')
                if rs22:
                    rearOutput+=rs22
                rearOutput.append([])
                rs23=self.getBestSFR(directory+'\sfr_0_off_d65_700_400cm')
                if rs23:
                    rearOutput+=rs23
                rearOutput.append([])
                rearOutput.append(['Copy Ends Here**********************'])
                rearOutput.append([])
                rearOutput.append([])
                rearOutput.append([])

            with open('report_helper_rear.csv','wb') as f:
                csvWriter=csv.writer(f)
                csvWriter.writerows(rearOutput)

            tkMessageBox.showinfo('Notice',self.warning)

    def getFront(self):
        print 'front'
        directory=self.entry.get()
        if not directory or not os.path.isdir(directory):
            tkMessageBox.showinfo('Warning','Please input valid directory')
        elif self.CheckVar1.get()==0 and self.CheckVar2.get()==0 and self.CheckVar3.get()==0 and self.CheckVar4.get()==0:
            tkMessageBox.showinfo('Warning','Please choose at least one test result you need')
        else:
            self.warning='Finished \n'
            frontOutput=[]
            frontOutput.append(['FRONT'])
            frontOutput.append([])
            frontOutput.append([])
            frontOutput.append([])

            if self.CheckVar1.get()==1:
                frontOutput.append(['Raw Data Color'])
                frontOutput.append(['2800K,>500lux','','4100K,20lux','','4100K,100lux','','4100K,>500lux','','6500K,20lux','','6500K,100lux','','6500K,>500lux'])
                frontOutput.append(['a*','b*','a*','b*','a*','b*','a*','b*','a*','b*','a*','b*','a*','b*'])
                frontOutput.append(['Copy Starts Here**********************'])
                frontOutput.append([])
                raw_data=[[] for i in range(24)]
                rs1=self.getBestColor(directory+'\color_1_off_halogen_700_60cm')
                if rs1:
                    for i in range(24):
                        raw_data[i]+=rs1[i]
                rs2=self.getBestColor(directory+'\color_1_off_f11_20_60cm')
                if rs2:
                    for i in range(24):
                        raw_data[i]+=rs2[i]
                rs3=self.getBestColor(directory+'\color_1_off_f11_100_60cm')
                if rs3:
                    for i in range(24):
                        raw_data[i]+=rs3[i]
                rs4=self.getBestColor(directory+'\color_1_off_f11_700_60cm')
                if rs4:
                    for i in range(24):
                        raw_data[i]+=rs4[i]
                rs5=self.getBestColor(directory+'\color_1_off_d65_20_60cm')
                if rs5:
                    for i in range(24):
                        raw_data[i]+=rs5[i]
                rs6=self.getBestColor(directory+'\color_1_off_d65_100_60cm')
                if rs6:
                    for i in range(24):
                        raw_data[i]+=rs6[i]
                rs7=self.getBestColor(directory+'\color_1_off_d65_700_60cm')
                if rs7:
                    for i in range(24):
                        raw_data[i]+=rs7[i]
                frontOutput+=raw_data
                frontOutput.append([])
                frontOutput.append(['Copy Ends Here**********************'])
                frontOutput.append([])
                frontOutput.append([])
                frontOutput.append([])



                
            if self.CheckVar2.get()==1:
                frontOutput.append(['Raw Data Color Flash'])
                frontOutput.append(['2800K,10>lux','','4100K,10lux','','6500K,20lux','','0lux',''])
                frontOutput.append(['a*','b*','a*','b*','a*','b*','a*','b*'])
                frontOutput.append(['Copy Starts Here**********************'])
                frontOutput.append([])
                flash_data=[[] for i in range(24)]
                rs11=self.getBestColor(directory+'\color_1_on_f12_10_60cm')
                if rs11:
                    for i in range(24):
                        flash_data[i]+=rs11[i]
                rs12=self.getBestColor(directory+'\color_1_on_f11_10_60cm')
                if rs12:
                    for i in range(24):
                        flash_data[i]+=rs12[i]
                rs13=self.getBestColor(directory+'\color_1_on_d65_10_60cm')
                if rs13:
                    for i in range(24):
                        flash_data[i]+=rs13[i]
                rs14=self.getBestColor(directory+'\color_1_on_f12_0_60cm')
                if rs14:
                    for i in range(24):
                        flash_data[i]+=rs14[i]
                frontOutput+=flash_data
                frontOutput.append([])
                frontOutput.append(['Copy Ends Here**********************'])
                frontOutput.append([])
                frontOutput.append([])
                frontOutput.append([])


            if self.CheckVar1.get()==1:
                frontOutput.append(['Raw Data Noise & SNR'])
                frontOutput.append(['The order below: d65_20lux, d65_100lux and d65_700lux'])
                frontOutput.append(['Red','','','Green','','','Blue','','','Y','','','Cb','','','Cr'])
                frontOutput.append(['Ave','Stdev','SNR','Ave','Stdev','SNR','Ave','Stdev','SNR','Ave','Stdev','SNR','Ave','Stdev','SNR','Ave','Stdev','SNR'])
                frontOutput.append(['Copy Starts Here**********************'])
                frontOutput.append([])
                rs8=self.getSNR(directory+'\color_1_off_d65_20_60cm')
                if rs8:
                    frontOutput+=rs8
                frontOutput.append([])
                frontOutput.append([])
                frontOutput.append(['Red','','','Green','','','Blue','','','Y','','','Cb','','','Cr'])
                frontOutput.append(['Ave','Stdev','SNR','Ave','Stdev','SNR','Ave','Stdev','SNR','Ave','Stdev','SNR','Ave','Stdev','SNR','Ave','Stdev','SNR'])
                rs9=self.getSNR(directory+'\color_1_off_d65_100_60cm')
                if rs9:
                    frontOutput+=rs9
                frontOutput.append([])
                frontOutput.append([])
                frontOutput.append(['Red','','','Green','','','Blue','','','Y','','','Cb','','','Cr'])
                frontOutput.append(['Ave','Stdev','SNR','Ave','Stdev','SNR','Ave','Stdev','SNR','Ave','Stdev','SNR','Ave','Stdev','SNR','Ave','Stdev','SNR'])
                rs10=self.getSNR(directory+'\color_1_off_d65_700_60cm')
                if rs10:
                    frontOutput+=rs10
                frontOutput.append([])
                frontOutput.append(['Copy Ends Here**********************'])
                frontOutput.append([])
                frontOutput.append([])
                frontOutput.append([])


                
            if self.CheckVar3.get()==1:
                frontOutput.append(['Raw Data Uniformity'])
                frontOutput.append(['The order below: f12, f11, d65, and halogen'])
                frontOutput.append(['Copy Starts Below the First Luma**********************'])
                frontOutput.append([])
                rs15=self.getBestUniformity(directory+'\uniformity_1_off_f12_700_120cm')
                if rs15:
                    frontOutput+=rs15
                frontOutput.append([])
                rs16=self.getBestUniformity(directory+'\uniformity_1_off_f11_700_120cm')
                if rs16:
                    frontOutput+=rs16
                frontOutput.append([])
                rs17=self.getBestUniformity(directory+'\uniformity_1_off_d65_700_120cm')
                if rs17:
                    frontOutput+=rs17
                frontOutput.append([])
                rs18=self.getBestUniformity(directory+'\uniformity_1_off_halogen_700_120cm')
                if rs18:
                    frontOutput+=rs18
                frontOutput.append([])
                frontOutput.append(['Copy Ends Here**********************'])
                frontOutput.append([])
                frontOutput.append([])
                frontOutput.append([])

                
            if self.CheckVar4.get()==1:
                frontOutput.append(['Raw Data Resolution'])
                frontOutput.append(['The order below: 700lux_10cm, 700lux_60cm, 20lux_60cm, 700lux_120cm, and 700lux_400cm'])
                frontOutput.append(['Copy Starts Here**********************'])
                frontOutput.append([])
                rs19=self.getBestSFR(directory+'\sfr_1_off_d65_700_10cm')
                if rs19:
                    frontOutput+=rs19
                frontOutput.append([])
                frontOutput.append([])
                rs20=self.getBestSFR(directory+'\sfr_1_off_d65_700_60cm')
                if rs20:
                    frontOutput+=rs20
                frontOutput.append([])
                rs21=self.getBestSFR(directory+'\sfr_1_off_d65_20_60cm')
                if rs21:
                    frontOutput+=rs21
                frontOutput.append([])
                rs22=self.getBestSFR(directory+'\sfr_1_off_d65_700_120cm')
                if rs22:
                    frontOutput+=rs22
                frontOutput.append([])
                rs23=self.getBestSFR(directory+'\sfr_1_off_d65_700_400cm')
                if rs23:
                    frontOutput+=rs23
                frontOutput.append([])
                frontOutput.append(['Copy Ends Here**********************'])
                frontOutput.append([])
                frontOutput.append([])
                frontOutput.append([])

            with open('report_helper_front.csv','wb') as f:
                csvWriter=csv.writer(f)
                csvWriter.writerows(frontOutput)

            tkMessageBox.showinfo('Notice',self.warning)

    def getBestColor(self,directory):
        output=[['',''] for i in range(24)]
        if os.path.isdir(directory):
            errorResults=[]
            allFiles=glob.glob(os.path.join(directory,'*.csv'))
            for file in allFiles:
                errors=[]
                with open(file,'rb') as f:
                    csvReader=csv.reader(f)
                    for row in csvReader:
                        if row and 'Average Color Error Results' in row:
                            pos=row.index('Average Color Error Results')+1
                            for i in range(3):
                                cur=csvReader.next()
                                if cur and cur[pos]:
                                    errors.append(float(cur[pos]))
                            break
                f.close()
                if errors:
                    errorResults.append(errors)
            if errorResults:
                print errorResults
                errs=[]
                for x in errorResults:
                    errs.append(abs(x[0])+abs(x[1])+abs(x[2]-125))
                best=errs.index(min(errs))
                print(best)

                with open(allFiles[best],'rb') as f:
                    csvReader=csv.reader(f)
                    for row in csvReader:
                        if row and 'Measured Values' in row:
                            cur=csvReader.next()
                            pos=cur.index('a*')
                            for i in range(24):
                                cur=csvReader.next()
                                if cur and cur[pos] and cur[pos+1]:
                                    output[i][0],output[i][1]=cur[pos],cur[pos+1]
                            break
                f.close()
            else:
                self.warning+='Cannot get Error Results from '+directory+' \n'
        else:
            self.warning+='Cannot find path '+directory+' \n'
        return output

    def getSNR(self,directory):
        output=[[] for i in range(24)]
        if os.path.isdir(directory):
            errorResults=[]
            allFiles=glob.glob(os.path.join(directory,'*.csv'))
            for file in allFiles:
                errors=[]
                with open(file,'rb') as f:
                    csvReader=csv.reader(f)
                    for row in csvReader:
                        if row and 'Average Color Error Results' in row:
                            pos=row.index('Average Color Error Results')+1
                            for i in range(3):
                                cur=csvReader.next()
                                if cur and cur[pos]:
                                    errors.append(float(cur[pos]))
                            break
                f.close()
                if errors:
                    errorResults.append(errors)
            if errorResults:
                print errorResults
                errs=[]
                for x in errorResults:
                    errs.append(abs(x[0])+abs(x[1])+abs(x[2]-125))
                best=errs.index(min(errs))
                print(best)

                with open(allFiles[best],'rb') as f:
                    csvReader=csv.reader(f)
                    for row in csvReader:
                        if row and 'SNR Values' in row:
                            cur=csvReader.next()
                            start=cur.index('Red Ave.')
                            for i in range(24):
                                cur=csvReader.next()
                                if cur and cur[start]:
                                    output[i]+=cur[start:]
                            break
                f.close()
            else:
                self.warning+='Cannot get Error Results from '+directory+' \n'
        else:
            self.warning+='Cannot find path '+directory+' \n'
        return output

    def getBestSFR(self,directory):
        output=None
        if '400cm' in directory:
            output=[[] for i in range(2)]
        else:
            output=[[] for i in range(10)]
        
        if os.path.isdir(directory):
            centrals=[]
            allFiles=glob.glob(os.path.join(directory,'*.csv'))
            for file in allFiles:
                with open(file,'rb') as f:
                    csvReader=csv.reader(f)
                    for row in csvReader:
                        if row and 'MTF / Freq' in row:
                            pos=row.index('MTF / Freq')
                            cur=csvReader.next()
                            if cur and cur[pos]:
                                centrals.append(float(cur[pos]))
                            break
                f.close()
            if centrals:
                print centrals
                errs=[]
                for x in centrals:
                    errs.append(abs(x-1))
                best=errs.index(min(errs))
                print(best)

                with open(allFiles[best],'rb') as f:
                    csvReader=csv.reader(f)
                    for row in csvReader:
                        if row and 'Sharpness %' in row and '0' in row:
                            start=row.index('Sharpness %')+1
                            if row and row[start]:
                                output[0]+=row[start:]
                            if '10cm' in directory:                                    
                                cur=csvReader.next()
                                if cur and cur[start]:
                                    output[1]+=cur[start:]
                                else:
                                    output[1]=['csv files are not processed by IAT SFRPlus Old SFR Chart']
                                    break
                                cur=csvReader.next()
                                if cur and cur[start]:
                                    output[3]+=cur[start:]
                                else:
                                    output[1]=['csv files are not processed by IAT SFRPlus Old SFR Chart']
                                    break
                                cur=csvReader.next()
                                if cur and cur[start]:
                                    output[5]+=cur[start:]
                                else:
                                    output[1]=['csv files are not processed by IAT SFRPlus Old SFR Chart']
                                    break
                                cur=csvReader.next()
                                if cur and cur[start]:
                                    output[9]+=cur[start:]
                                else:
                                    output[1]=['csv files are not processed by IAT SFRPlus Old SFR Chart']
                                    break
                                cur=csvReader.next()
                                if cur and cur[start]:
                                    output[7]+=cur[start:]
                                else:
                                    output[1]=['csv files are not processed by IAT SFRPlus Old SFR Chart']
                                    break
                            elif '60cm' in directory or '120cm' in directory:
                                i=1
                                while i<10:
                                    cur=csvReader.next()
                                    if cur and cur[start]:
                                        output[i]+=cur[start:]
                                    else:
                                        break
                                    i+=1
                                    print i
                                if i<10:
                                    output[1]=['csv files are not processed by IAT SFRPlus 60% from center']
                            else:
                                cur=csvReader.next()
                                if cur and cur[start]:
                                    output[1]+=cur[start:]
                            break
                f.close()
                
            else:
                self.warning+='Cannot get Central MTF from '+directory+' \n'
        else:
            self.warning+='Cannot find path '+directory+' \n'
        return output

    def getBestUniformity(self,directory):
        output=[[] for i in range(53)]
        if os.path.isdir(directory):
            shadings=[]
            allFiles=glob.glob(os.path.join(directory,'*.csv'))
            for file in allFiles:
                with open(file,'rb') as f:
                    csvReader=csv.reader(f)
                    for row in csvReader:
                        if row and 'Shading %' in row:
                            pos=row.index('Shading %')+1
                            if row[pos]:
                                shadings.append(float(row[pos]))
                            break
                f.close()
            if shadings:
                print shadings
                errs=[]
                for x in shadings:
                    errs.append(abs(x-80))
                best=errs.index(min(errs))
                print(best)
                
                with open(allFiles[best],'rb') as f:
                    csvReader=csv.reader(f)
                    for row in csvReader:
                        if row and 'File Path' in row:
                            cur=csvReader.next()
                            start=cur.index('0')
                            output[0]+=['Luma']
                            for i in range(1,26):
                                if cur and cur[start]:
                                    output[i]+=cur[start:]
                                cur=csvReader.next()
                            output[27]+=['Delta C*ab']
                            for i in range(28,53):
                                cur=csvReader.next()
                                if cur and cur[start]:
                                    output[i]+=cur[start:]
                            break
                f.close()
                
            else:
                self.warning+='Cannot get Shadings from '+directory+' \n'
        else:
            self.warning+='Cannot find path '+directory+' \n'
        return output

window=Tk()
window.title('Report Helper GUI by Xiaopei Zhang')
window.geometry('600x350')
app=Application(window)
window.mainloop()
print app.warning


