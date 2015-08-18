import csv,glob,os
from Tkinter import *
import tkMessageBox
from xlrd import *
from xlwt import *
#import Tkinter
#http://blog.csdn.net/onlyanyz/article/details/45348279
#dark green-17; yellow-5; red-2; pink-29

class Application(Frame):

    def __init__(self,master):
        Frame.__init__(self,master)
        self.pack()
        self.createWidgets()
        self.warning='Finished \n'

    def createWidgets(self):
        self.label1=Label(self,text='Please input the directory under which all the xls files exist')
        self.label1.pack()
        self.label2=Label(self,text='Remember to put either ONLY rear xls or front xls in this folder')
        self.label2.pack()

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


        self.label3=Label(self,text='If re-generate comparison xls')
        self.label3.pack()
        self.label4=Label(self,text='Please close previously generated ones')
        self.label4.pack()

        self.button1=Button(self,text='Get Rear comparison.xls',command=self.getRear)
        self.button1.pack(side=LEFT)
        self.button2=Button(self,text='Get Front comparison.xls',command=self.getFront)
        self.button2.pack(side=RIGHT)

    def getRear(self):

        directory=self.entry.get()
        if not directory or not os.path.isdir(directory):
            tkMessageBox.showinfo('Warning','Please input valid directory')
        else:
            self.warning='Finished \n'
            allFiles=glob.glob(os.path.join(directory,'*.xls'))

            if len(allFiles)<2:
                tkMessageBox.showinfo('Warning','There are not enough spreadsheets for comparison in '+directory)
            else:
                book=Workbook(encoding='utf-8')
                sheet=book.add_sheet('Rear')
                style=XFStyle()
                style.font.name='Calibri'
                sheet.write(0,0,'Rear Camera IQ Results Comparison',style)

                header_style=XFStyle()
                header_style.font.name='Calibri'
                header_style.font.colour_index=1
                header_style.font.bold=True
                header_style.alignment.horz=Alignment.HORZ_CENTER
                header_style.alignment.vert=Alignment.VERT_CENTER
                header_style.borders.left=Borders.THIN
                header_style.borders.right=Borders.THIN
                header_style.borders.top=Borders.THIN
                header_style.borders.bottom=Borders.THIN
                header_style.pattern.pattern=Pattern.SOLID_PATTERN
                header_style.pattern.pattern_fore_colour=23

                item_style=XFStyle()
                item_style.font.name='Calibri'
                item_style.alignment.horz=Alignment.HORZ_CENTER
                item_style.alignment.vert=Alignment.VERT_CENTER
                item_style.borders.left=Borders.THIN
                item_style.borders.right=Borders.THIN
                item_style.borders.top=Borders.THIN
                item_style.borders.bottom=Borders.THIN

                bold_item_style=XFStyle()
                bold_item_style.font.name='Calibri'
                bold_item_style.font.bold=True
                bold_item_style.alignment.horz=Alignment.HORZ_CENTER
                bold_item_style.alignment.vert=Alignment.VERT_CENTER
                bold_item_style.borders.left=Borders.THIN
                bold_item_style.borders.right=Borders.THIN
                bold_item_style.borders.top=Borders.THIN
                bold_item_style.borders.bottom=Borders.THIN
                
                sheet.col(0).width=256*20
                sheet.write_merge(3,4,0,0,'Item',header_style)
                sheet.col(1).width=256*20
                sheet.write_merge(3,4,1,1,'Sub-Items',header_style)
                sheet.col(2).width=256*20
                sheet.write_merge(3,4,2,2,'Test Conditions',header_style)

                for i in range(len(allFiles)):
                    sheet.col(3+i*2).width=256*20
                    sheet.write(2,3+i*2,os.path.basename(allFiles[i]),style)
                    sheet.write_merge(3,4,3+i*2,3+i*2,'Measured Values',header_style)
                    sheet.col(4+i*2).width=256*20
                    sheet.write_merge(3,4,4+i*2,4+i*2,'Weighted Score',header_style)


                sheet.write_merge(5,13,0,0,'Color',bold_item_style)
                sheet.write_merge(5,7,1,1,'Accuracy',item_style)
                sheet.write_merge(8,10,1,1,'Saturation',item_style)
                sheet.write_merge(11,13,1,1,'White Balance',item_style)
                for i in range(3):
                    sheet.write(5+i*3,2,'2800K',item_style)
                    sheet.write(6+i*3,2,'4100K',item_style)
                    sheet.write(7+i*3,2,'6500K',item_style)
                
                sheet.write_merge(14,22,0,0,'SNR',bold_item_style)
                sheet.write_merge(14,16,1,1,'Luma (Y)',item_style)
                sheet.write_merge(17,19,1,1,'Chroma (Cb)',item_style)
                sheet.write_merge(20,22,1,1,'Chroma (Cr)',item_style)
                for i in range(3):
                    sheet.write(14+i*3,2,'> 500 Lux',item_style)
                    sheet.write(15+i*3,2,'100 Lux',item_style)
                    sheet.write(16+i*3,2,'20 Lux',item_style)
                
                sheet.write_merge(23,30,0,0,'Uniformity',bold_item_style)
                sheet.write_merge(23,26,1,1,'Shading (Luma)',item_style)
                sheet.write_merge(27,30,1,1,'Color',item_style)
                for i in range(2):
                    sheet.write(23+i*4,2,'2800K A',item_style)
                    sheet.write(24+i*4,2,'2800K f12',item_style)
                    sheet.write(25+i*4,2,'4100K',item_style)
                    sheet.write(26+i*4,2,'6500K',item_style)
                
                sheet.write_merge(31,40,0,0,'Resolution',bold_item_style)
                sheet.write_merge(31,35,1,1,'SFR',item_style)
                sheet.write_merge(36,40,1,1,'Sharpness',item_style)
                for i in range(2):
                    sheet.write(31+i*5,2,'10 cm',item_style)
                    sheet.write(32+i*5,2,'60 cm',item_style)
                    sheet.write(33+i*5,2,'60cm, 20Lux',item_style)
                    sheet.write(34+i*5,2,'120 cm',item_style)
                    sheet.write(35+i*5,2,'400 cm',item_style)
                
                sheet.write_merge(41,52,0,0,'Illumination (flash)',bold_item_style)
                sheet.write_merge(41,44,1,1,'Accuracy',item_style)
                sheet.write_merge(45,48,1,1,'Saturation',item_style)
                sheet.write_merge(49,52,1,1,'White Balance',item_style)
                for i in range(3):
                    sheet.write(41+i*4,2,'2800K 10Lux',item_style)
                    sheet.write(42+i*4,2,'4100K 10Lux',item_style)
                    sheet.write(43+i*4,2,'6500K 10Lux',item_style)
                    sheet.write(44+i*4,2,'0Lux',item_style)



                limit_col=3+2*len(allFiles)
                sheet.write_merge(3,3,limit_col,limit_col+1,'Green Limits',header_style)
                sheet.write_merge(3,3,limit_col+2,limit_col+3,'Yellow Limits',header_style)
                sheet.write(4,limit_col,'Lower',header_style)
                sheet.write(4,limit_col+1,'Upper',header_style)
                sheet.write(4,limit_col+2,'Lower',header_style)
                sheet.write(4,limit_col+3,'Upper',header_style)
                for i in range(5,6):
                    sheet.write(i,limit_col,0,item_style)
                    sheet.write(i,limit_col+1,18,item_style)
                    sheet.write(i,limit_col+2,18,item_style)
                    sheet.write(i,limit_col+3,24,item_style)
                for i in range(6,8):
                    sheet.write(i,limit_col,0,item_style)
                    sheet.write(i,limit_col+1,12,item_style)
                    sheet.write(i,limit_col+2,12,item_style)
                    sheet.write(i,limit_col+3,18,item_style)
                for i in range(8,9):
                    sheet.write(i,limit_col,115,item_style)
                    sheet.write(i,limit_col+1,135,item_style)
                    sheet.write(i,limit_col+2,100,item_style)
                    sheet.write(i,limit_col+3,145,item_style)
                for i in range(9,11):
                    sheet.write(i,limit_col,115,item_style)
                    sheet.write(i,limit_col+1,135,item_style)
                    sheet.write(i,limit_col+2,110,item_style)
                    sheet.write(i,limit_col+3,145,item_style)
                for i in range(11,12):
                    sheet.write(i,limit_col,0,item_style)
                    sheet.write(i,limit_col+1,6,item_style)
                    sheet.write(i,limit_col+2,6,item_style)
                    sheet.write(i,limit_col+3,10,item_style)
                for i in range(12,14):
                    sheet.write(i,limit_col,0,item_style)
                    sheet.write(i,limit_col+1,4,item_style)
                    sheet.write(i,limit_col+2,4,item_style)
                    sheet.write(i,limit_col+3,6,item_style)
                for i in range(14,16):
                    sheet.write(i,limit_col,35,item_style)
                    sheet.write(i,limit_col+1,70,item_style)
                    sheet.write(i,limit_col+2,30,item_style)
                    sheet.write(i,limit_col+3,35,item_style)
                for i in range(16,17):
                    sheet.write(i,limit_col,25,item_style)
                    sheet.write(i,limit_col+1,70,item_style)
                    sheet.write(i,limit_col+2,20,item_style)
                    sheet.write(i,limit_col+3,25,item_style)
                for i in range(17,18):
                    sheet.write(i,limit_col,45,item_style)
                    sheet.write(i,limit_col+1,70,item_style)
                    sheet.write(i,limit_col+2,40,item_style)
                    sheet.write(i,limit_col+3,45,item_style)
                for i in range(18,19):
                    sheet.write(i,limit_col,40,item_style)
                    sheet.write(i,limit_col+1,70,item_style)
                    sheet.write(i,limit_col+2,35,item_style)
                    sheet.write(i,limit_col+3,40,item_style)
                for i in range(19,20):
                    sheet.write(i,limit_col,35,item_style)
                    sheet.write(i,limit_col+1,70,item_style)
                    sheet.write(i,limit_col+2,30,item_style)
                    sheet.write(i,limit_col+3,35,item_style)
                for i in range(20,21):
                    sheet.write(i,limit_col,45,item_style)
                    sheet.write(i,limit_col+1,70,item_style)
                    sheet.write(i,limit_col+2,40,item_style)
                    sheet.write(i,limit_col+3,45,item_style)
                for i in range(21,22):
                    sheet.write(i,limit_col,40,item_style)
                    sheet.write(i,limit_col+1,70,item_style)
                    sheet.write(i,limit_col+2,35,item_style)
                    sheet.write(i,limit_col+3,40,item_style)
                for i in range(22,23):
                    sheet.write(i,limit_col,35,item_style)
                    sheet.write(i,limit_col+1,70,item_style)
                    sheet.write(i,limit_col+2,30,item_style)
                    sheet.write(i,limit_col+3,35,item_style)
                for i in range(23,27):
                    sheet.write(i,limit_col,'70.0%',item_style)
                    sheet.write(i,limit_col+1,'90.0%',item_style)
                    sheet.write(i,limit_col+2,'60%',item_style)
                    sheet.write(i,limit_col+3,'100%',item_style)
                for i in range(27,31):
                    sheet.write(i,limit_col,0,item_style)
                    sheet.write(i,limit_col+1,6,item_style)
                    sheet.write(i,limit_col+2,6,item_style)
                    sheet.write(i,limit_col+3,10,item_style)
                for i in range(31,33):
                    sheet.write(i,limit_col,0.4,item_style)
                    sheet.write(i,limit_col+1,1,item_style)
                    sheet.write(i,limit_col+2,0.3,item_style)
                    sheet.write(i,limit_col+3,0.4,item_style)
                for i in range(33,34):
                    sheet.write(i,limit_col,0.1,item_style)
                    sheet.write(i,limit_col+1,1,item_style)
                    sheet.write(i,limit_col+2,0.3,item_style)
                    sheet.write(i,limit_col+3,0.1,item_style)
                for i in range(34,36):
                    sheet.write(i,limit_col,0.4,item_style)
                    sheet.write(i,limit_col+1,1,item_style)
                    sheet.write(i,limit_col+2,0.3,item_style)
                    sheet.write(i,limit_col+3,0.4,item_style)
                for i in range(36,41):
                    sheet.write(i,limit_col,'-10%',item_style)
                    sheet.write(i,limit_col+1,'20%',item_style)
                    sheet.write(i,limit_col+2,'',item_style)
                    sheet.write(i,limit_col+3,'',item_style)
                for i in range(41,42):
                    sheet.write(i,limit_col,0,item_style)
                    sheet.write(i,limit_col+1,18,item_style)
                    sheet.write(i,limit_col+2,18,item_style)
                    sheet.write(i,limit_col+3,24,item_style)
                for i in range(42,45):
                    sheet.write(i,limit_col,0,item_style)
                    sheet.write(i,limit_col+1,12,item_style)
                    sheet.write(i,limit_col+2,12,item_style)
                    sheet.write(i,limit_col+3,18,item_style)
                for i in range(45,46):
                    sheet.write(i,limit_col,115,item_style)
                    sheet.write(i,limit_col+1,135,item_style)
                    sheet.write(i,limit_col+2,100,item_style)
                    sheet.write(i,limit_col+3,145,item_style)
                for i in range(46,49):
                    sheet.write(i,limit_col,115,item_style)
                    sheet.write(i,limit_col+1,135,item_style)
                    sheet.write(i,limit_col+2,110,item_style)
                    sheet.write(i,limit_col+3,145,item_style)
                for i in range(49,50):
                    sheet.write(i,limit_col,0,item_style)
                    sheet.write(i,limit_col+1,6,item_style)
                    sheet.write(i,limit_col+2,6,item_style)
                    sheet.write(i,limit_col+3,10,item_style)
                for i in range(50,53):
                    sheet.write(i,limit_col,0,item_style)
                    sheet.write(i,limit_col+1,4,item_style)
                    sheet.write(i,limit_col+2,4,item_style)
                    sheet.write(i,limit_col+3,6,item_style)
                
                

       
                for i in range(len(allFiles)):
                    report=open_workbook(allFiles[i],formatting_info=True)
                    summary=report.sheet_by_index(0)

                    color_row=None;SNR_row=None;uniformity_row=None;resolution_row=None;illumination_row=None;score_col=None
                    j=0
                    while j<summary.nrows:
                        if 'Measured Value' in str(summary.cell_value(j,3)):
                            break
                        j+=1

                    while j<summary.nrows:
                        if 'Color' in str(summary.cell_value(j,0)):
                            color_row=j
                        if 'SNR' in str(summary.cell_value(j,0)):
                            SNR_row=j
                        if 'Uniformity' in str(summary.cell_value(j,0)):
                            #uniformity did not merge all the cells
                            uniformity_row=j-1
                        if 'Resolution' in str(summary.cell_value(j,0)):
                            resolution_row=j
                        if 'Illumination' in str(summary.cell_value(j,0)):
                            illumination_row=j
                        if 'Weighted Score' in str(summary.cell_value(j,13)):
                            score_col=13
                        j+=1
                    print color_row,SNR_row,uniformity_row,resolution_row,illumination_row,score_col

                    

                    if not color_row and not SNR_row and not uniformity_row and not resolution_row and not illumination_row:
                        self.warning+='Cannot find any Measured Value to compare in '+str(allFiles[i])+'\n'
                    else:
                        if color_row:
                            if '2800K' in str(summary.cell_value(color_row,2)) and '6500K' in str(summary.cell_value(color_row+8,2)):
                                for k in range(1):
                                    cell_val=summary.cell_value(color_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,0,18,18,24)
                                    if isinstance(cell_val,float):
                                        sheet.write(5+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(5+k,3+i*2,cell_val,cell_style)
                                for k in range(1,3):
                                    cell_val=summary.cell_value(color_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,0,12,12,18)
                                    if isinstance(cell_val,float):
                                        sheet.write(5+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(5+k,3+i*2,cell_val,cell_style)
                                for k in range(3,4):
                                    cell_val=summary.cell_value(color_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,115,135,100,145)
                                    if isinstance(cell_val,float):
                                        sheet.write(5+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(5+k,3+i*2,cell_val,cell_style)
                                for k in range(4,6):
                                    cell_val=summary.cell_value(color_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,115,135,110,145)
                                    if isinstance(cell_val,float):
                                        sheet.write(5+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(5+k,3+i*2,cell_val,cell_style)
                                for k in range(6,7):
                                    cell_val=summary.cell_value(color_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,0,6,6,10)
                                    if isinstance(cell_val,float):
                                        sheet.write(5+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(5+k,3+i*2,cell_val,cell_style)
                                for k in range(7,9):
                                    cell_val=summary.cell_value(color_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,0,4,4,6)
                                    if isinstance(cell_val,float):
                                        sheet.write(5+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(5+k,3+i*2,cell_val,cell_style)
                            else:
                                sheet.write_merge(5,13,3+i*2,3+i*2,'No Corresponding Data',item_style)
                        else:
                            sheet.write_merge(5,13,3+i*2,3+i*2,'No Data',item_style)
                        if SNR_row:
                            if '500 Lux' in str(summary.cell_value(SNR_row,2)) and '20 Lux' in str(summary.cell_value(SNR_row+8,2)):
                                for k in range(2):
                                    cell_val=summary.cell_value(SNR_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,35,70,30,35)
                                    if isinstance(cell_val,float):
                                        sheet.write(14+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(14+k,3+i*2,cell_val,cell_style)
                                for k in range(2,3):
                                    cell_val=summary.cell_value(SNR_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,25,70,20,25)
                                    if isinstance(cell_val,float):
                                        sheet.write(14+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(14+k,3+i*2,cell_val,cell_style)
                                for k in range(3,4):
                                    cell_val=summary.cell_value(SNR_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,45,70,40,45)
                                    if isinstance(cell_val,float):
                                        sheet.write(14+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(14+k,3+i*2,cell_val,cell_style)
                                for k in range(4,5):
                                    cell_val=summary.cell_value(SNR_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,40,70,35,40)
                                    if isinstance(cell_val,float):
                                        sheet.write(14+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(14+k,3+i*2,cell_val,cell_style)
                                for k in range(5,6):
                                    cell_val=summary.cell_value(SNR_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,35,70,30,35)
                                    if isinstance(cell_val,float):
                                        sheet.write(14+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(14+k,3+i*2,cell_val,cell_style)
                                for k in range(6,7):
                                    cell_val=summary.cell_value(SNR_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,45,70,40,45)
                                    if isinstance(cell_val,float):
                                        sheet.write(14+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(14+k,3+i*2,cell_val,cell_style)
                                for k in range(7,8):
                                    cell_val=summary.cell_value(SNR_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,40,70,35,40)
                                    if isinstance(cell_val,float):
                                        sheet.write(14+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(14+k,3+i*2,cell_val,cell_style)
                                for k in range(8,9):
                                    cell_val=summary.cell_value(SNR_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,35,70,30,35)
                                    if isinstance(cell_val,float):
                                        sheet.write(14+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(14+k,3+i*2,cell_val,cell_style)
                            else:
                                sheet.write_merge(14,22,3+i*2,3+i*2,'No Corresponding Data',item_style)
                        else:
                            sheet.write_merge(14,22,3+i*2,3+i*2,'No Data',item_style)
                        if uniformity_row:
                            if '2800K A' in str(summary.cell_value(uniformity_row,2)) and '6500K' in str(summary.cell_value(uniformity_row+7,2)):
                                for k in range(4):
                                    cell_val=summary.cell_value(uniformity_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,0.7,0.9,0.6,1)
                                    if isinstance(cell_val,float):
                                        sheet.write(23+k,3+i*2,'{:.2%}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(23+k,3+i*2,cell_val,cell_style)
                                for k in range(4,8):
                                    cell_val=summary.cell_value(uniformity_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,0,6,6,10)
                                    if isinstance(cell_val,float):
                                        sheet.write(23+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(23+k,3+i*2,cell_val,cell_style)
                            else:
                                sheet.write_merge(23,30,3+i*2,3+i*2,'No Corresponding Data',item_style)
                        else:
                            sheet.write_merge(23,30,3+i*2,3+i*2,'No Data',item_style)
                        if resolution_row:
                            if '10 cm' in str(summary.cell_value(resolution_row,2)) and '400 cm' in str(summary.cell_value(resolution_row+9,2)):
                                for k in range(2):
                                    cell_val=summary.cell_value(resolution_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,0.4,2,None,None)
                                    if isinstance(cell_val,float):
                                        sheet.write(31+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(31+k,3+i*2,cell_val,cell_style)
                                for k in range(2,3):
                                    cell_val=summary.cell_value(resolution_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,0.1,2,None,None)
                                    if isinstance(cell_val,float):
                                        sheet.write(31+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(31+k,3+i*2,cell_val,cell_style)
                                for k in range(3,5):
                                    cell_val=summary.cell_value(resolution_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,0.4,2,None,None)
                                    if isinstance(cell_val,float):
                                        sheet.write(31+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(31+k,3+i*2,cell_val,cell_style)
                                for k in range(5,10):
                                    cell_val=summary.cell_value(resolution_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,-0.1,0.2,None,None)
                                    if isinstance(cell_val,float):
                                        sheet.write(31+k,3+i*2,'{:.2%}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(31+k,3+i*2,cell_val,cell_style)
                            else:
                                sheet.write_merge(31,40,3+i*2,3+i*2,'No Corresponding Data',item_style)
                        else:
                            sheet.write_merge(31,40,3+i*2,3+i*2,'No Data',item_style)
                        if illumination_row:
                            if '2800K' in str(summary.cell_value(illumination_row,2)) and '0Lux' in str(summary.cell_value(illumination_row+8,2)):
                                for k in range(1):
                                    cell_val=summary.cell_value(illumination_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,0,18,18,24)
                                    if isinstance(cell_val,float):
                                        sheet.write(41+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(41+k,3+i*2,cell_val,cell_style)
                                for k in range(1,4):
                                    cell_val=summary.cell_value(illumination_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,0,12,12,18)
                                    if isinstance(cell_val,float):
                                        sheet.write(41+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(41+k,3+i*2,cell_val,cell_style)
                                for k in range(4,5):
                                    cell_val=summary.cell_value(illumination_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,115,135,100,145)
                                    if isinstance(cell_val,float):
                                        sheet.write(41+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(41+k,3+i*2,cell_val,cell_style)
                                for k in range(5,8):
                                    cell_val=summary.cell_value(illumination_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,115,135,110,145)
                                    if isinstance(cell_val,float):
                                        sheet.write(41+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(41+k,3+i*2,cell_val,cell_style)
                                for k in range(8,9):
                                    cell_val=summary.cell_value(illumination_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,0,6,6,10)
                                    if isinstance(cell_val,float):
                                        sheet.write(41+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(41+k,3+i*2,cell_val,cell_style)
                                for k in range(9,12):
                                    cell_val=summary.cell_value(illumination_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,0,4,4,6)
                                    if isinstance(cell_val,float):
                                        sheet.write(41+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(41+k,3+i*2,cell_val,cell_style)
                            else:
                                sheet.write_merge(41,52,3+i*2,3+i*2,'No Corresponding Data',item_style)
                        else:
                            sheet.write_merge(41,52,3+i*2,3+i*2,'No Data',item_style)
                        if score_col:
                            if color_row:
                                cell_val=summary.cell_value(color_row,score_col)
                                if isinstance(cell_val,float):
                                    sheet.write_merge(5,13,4+i*2,4+i*2,'{0:.2f}'.format(cell_val),item_style)
                                else:
                                    sheet.write_merge(5,13,4+i*2,4+i*2,cell_val,item_style)
                            else:
                                sheet.write_merge(5,13,4+i*2,4+i*2,'No Corresponding Data',item_style)
                            if SNR_row:
                                cell_val=summary.cell_value(SNR_row,score_col)
                                if isinstance(cell_val,float):
                                    sheet.write_merge(14,22,4+i*2,4+i*2,'{0:.2f}'.format(cell_val),item_style)
                                else:
                                    sheet.write_merge(14,22,4+i*2,4+i*2,cell_val,item_style)
                            else:
                                sheet.write_merge(14,22,4+i*2,4+i*2,'No Corresponding Data',item_style)
                            if uniformity_row:
                                cell_val=summary.cell_value(uniformity_row,score_col)
                                if isinstance(cell_val,float):
                                    sheet.write_merge(23,30,4+i*2,4+i*2,'{0:.2f}'.format(cell_val),item_style)
                                else:
                                    sheet.write_merge(23,30,4+i*2,4+i*2,cell_val,item_style)
                            else:
                                sheet.write_merge(23,30,4+i*2,4+i*2,'No Corresponding Data',item_style)
                            if resolution_row:
                                cell_val=summary.cell_value(resolution_row,score_col)
                                if isinstance(cell_val,float):
                                    sheet.write_merge(31,40,4+i*2,4+i*2,'{0:.2f}'.format(cell_val),item_style)
                                else:
                                    sheet.write_merge(31,40,4+i*2,4+i*2,cell_val,item_style)
                            else:
                                sheet.write_merge(31,40,4+i*2,4+i*2,'No Corresponding Data',item_style)
                            if illumination_row:
                                cell_val=summary.cell_value(illumination_row,score_col)
                                if isinstance(cell_val,float):
                                    sheet.write_merge(41,52,4+i*2,4+i*2,'{0:.2f}'.format(cell_val),item_style)
                                else:
                                    sheet.write_merge(41,52,4+i*2,4+i*2,cell_val,item_style)
                            else:
                                sheet.write_merge(41,52,4+i*2,4+i*2,'No Corresponding Data',item_style)

                book.save('rear_comparison.xls')
                tkMessageBox.showinfo('Notice',self.warning)



    def getFront(self):

        directory=self.entry.get()
        if not directory or not os.path.isdir(directory):
            tkMessageBox.showinfo('Warning','Please input valid directory')
        else:
            self.warning='Finished \n'
            allFiles=glob.glob(os.path.join(directory,'*.xls'))

            if len(allFiles)<2:
                tkMessageBox.showinfo('Warning','There are not enough spreadsheets for comparison in '+directory)
            else:
                book=Workbook(encoding='utf-8')
                sheet=book.add_sheet('Front')
                style=XFStyle()
                style.font.name='Calibri'
                sheet.write(0,0,'Front Camera IQ Results Comparison',style)

                header_style=XFStyle()
                header_style.font.name='Calibri'
                header_style.font.colour_index=1
                header_style.font.bold=True
                header_style.alignment.horz=Alignment.HORZ_CENTER
                header_style.alignment.vert=Alignment.VERT_CENTER
                header_style.borders.left=Borders.THIN
                header_style.borders.right=Borders.THIN
                header_style.borders.top=Borders.THIN
                header_style.borders.bottom=Borders.THIN
                header_style.pattern.pattern=Pattern.SOLID_PATTERN
                header_style.pattern.pattern_fore_colour=23

                item_style=XFStyle()
                item_style.font.name='Calibri'
                item_style.alignment.horz=Alignment.HORZ_CENTER
                item_style.alignment.vert=Alignment.VERT_CENTER
                item_style.borders.left=Borders.THIN
                item_style.borders.right=Borders.THIN
                item_style.borders.top=Borders.THIN
                item_style.borders.bottom=Borders.THIN

                bold_item_style=XFStyle()
                bold_item_style.font.name='Calibri'
                bold_item_style.font.bold=True
                bold_item_style.alignment.horz=Alignment.HORZ_CENTER
                bold_item_style.alignment.vert=Alignment.VERT_CENTER
                bold_item_style.borders.left=Borders.THIN
                bold_item_style.borders.right=Borders.THIN
                bold_item_style.borders.top=Borders.THIN
                bold_item_style.borders.bottom=Borders.THIN
                
                sheet.col(0).width=256*20
                sheet.write_merge(3,4,0,0,'Item',header_style)
                sheet.col(1).width=256*20
                sheet.write_merge(3,4,1,1,'Sub-Items',header_style)
                sheet.col(2).width=256*20
                sheet.write_merge(3,4,2,2,'Test Conditions',header_style)

                for i in range(len(allFiles)):
                    sheet.col(3+i*2).width=256*20
                    sheet.write(2,3+i*2,os.path.basename(allFiles[i]),style)
                    sheet.write_merge(3,4,3+i*2,3+i*2,'Measured Values',header_style)
                    sheet.col(4+i*2).width=256*20
                    sheet.write_merge(3,4,4+i*2,4+i*2,'Weighted Score',header_style)


                sheet.write_merge(5,13,0,0,'Color',bold_item_style)
                sheet.write_merge(5,7,1,1,'Accuracy',item_style)
                sheet.write_merge(8,10,1,1,'Saturation',item_style)
                sheet.write_merge(11,13,1,1,'White Balance',item_style)
                for i in range(3):
                    sheet.write(5+i*3,2,'2800K',item_style)
                    sheet.write(6+i*3,2,'4100K',item_style)
                    sheet.write(7+i*3,2,'6500K',item_style)
                
                sheet.write_merge(14,22,0,0,'SNR',bold_item_style)
                sheet.write_merge(14,16,1,1,'Luma (Y)',item_style)
                sheet.write_merge(17,19,1,1,'Chroma (Cb)',item_style)
                sheet.write_merge(20,22,1,1,'Chroma (Cr)',item_style)
                for i in range(3):
                    sheet.write(14+i*3,2,'> 500 Lux',item_style)
                    sheet.write(15+i*3,2,'100 Lux',item_style)
                    sheet.write(16+i*3,2,'20 Lux',item_style)
                
                sheet.write_merge(23,30,0,0,'Uniformity',bold_item_style)
                sheet.write_merge(23,26,1,1,'Shading (Luma)',item_style)
                sheet.write_merge(27,30,1,1,'Color',item_style)
                for i in range(2):
                    sheet.write(23+i*4,2,'2800K A',item_style)
                    sheet.write(24+i*4,2,'2800K f12',item_style)
                    sheet.write(25+i*4,2,'4100K',item_style)
                    sheet.write(26+i*4,2,'6500K',item_style)
                
                sheet.write_merge(31,40,0,0,'Resolution',bold_item_style)
                sheet.write_merge(31,35,1,1,'SFR',item_style)
                sheet.write_merge(36,40,1,1,'Sharpness',item_style)
                for i in range(2):
                    sheet.write(31+i*5,2,'10 cm',item_style)
                    sheet.write(32+i*5,2,'60 cm',item_style)
                    sheet.write(33+i*5,2,'60cm, 20Lux',item_style)
                    sheet.write(34+i*5,2,'120 cm',item_style)
                    sheet.write(35+i*5,2,'400 cm',item_style)
                
                sheet.write_merge(41,52,0,0,'Illumination (flash)',bold_item_style)
                sheet.write_merge(41,44,1,1,'Accuracy',item_style)
                sheet.write_merge(45,48,1,1,'Saturation',item_style)
                sheet.write_merge(49,52,1,1,'White Balance',item_style)
                for i in range(3):
                    sheet.write(41+i*4,2,'2800K 10Lux',item_style)
                    sheet.write(42+i*4,2,'4100K 10Lux',item_style)
                    sheet.write(43+i*4,2,'6500K 10Lux',item_style)
                    sheet.write(44+i*4,2,'0Lux',item_style)



                limit_col=3+2*len(allFiles)
                sheet.write_merge(3,3,limit_col,limit_col+1,'Green Limits',header_style)
                sheet.write_merge(3,3,limit_col+2,limit_col+3,'Yellow Limits',header_style)
                sheet.write(4,limit_col,'Lower',header_style)
                sheet.write(4,limit_col+1,'Upper',header_style)
                sheet.write(4,limit_col+2,'Lower',header_style)
                sheet.write(4,limit_col+3,'Upper',header_style)
                for i in range(5,6):
                    sheet.write(i,limit_col,0,item_style)
                    sheet.write(i,limit_col+1,18,item_style)
                    sheet.write(i,limit_col+2,18,item_style)
                    sheet.write(i,limit_col+3,24,item_style)
                for i in range(6,8):
                    sheet.write(i,limit_col,0,item_style)
                    sheet.write(i,limit_col+1,12,item_style)
                    sheet.write(i,limit_col+2,12,item_style)
                    sheet.write(i,limit_col+3,18,item_style)
                for i in range(8,9):
                    sheet.write(i,limit_col,115,item_style)
                    sheet.write(i,limit_col+1,135,item_style)
                    sheet.write(i,limit_col+2,100,item_style)
                    sheet.write(i,limit_col+3,145,item_style)
                for i in range(9,11):
                    sheet.write(i,limit_col,115,item_style)
                    sheet.write(i,limit_col+1,135,item_style)
                    sheet.write(i,limit_col+2,110,item_style)
                    sheet.write(i,limit_col+3,145,item_style)
                for i in range(11,12):
                    sheet.write(i,limit_col,0,item_style)
                    sheet.write(i,limit_col+1,6,item_style)
                    sheet.write(i,limit_col+2,6,item_style)
                    sheet.write(i,limit_col+3,10,item_style)
                for i in range(12,14):
                    sheet.write(i,limit_col,0,item_style)
                    sheet.write(i,limit_col+1,4,item_style)
                    sheet.write(i,limit_col+2,4,item_style)
                    sheet.write(i,limit_col+3,6,item_style)
                for i in range(14,16):
                    sheet.write(i,limit_col,35,item_style)
                    sheet.write(i,limit_col+1,70,item_style)
                    sheet.write(i,limit_col+2,30,item_style)
                    sheet.write(i,limit_col+3,35,item_style)
                for i in range(16,17):
                    sheet.write(i,limit_col,25,item_style)
                    sheet.write(i,limit_col+1,70,item_style)
                    sheet.write(i,limit_col+2,20,item_style)
                    sheet.write(i,limit_col+3,25,item_style)
                for i in range(17,18):
                    sheet.write(i,limit_col,45,item_style)
                    sheet.write(i,limit_col+1,70,item_style)
                    sheet.write(i,limit_col+2,40,item_style)
                    sheet.write(i,limit_col+3,45,item_style)
                for i in range(18,19):
                    sheet.write(i,limit_col,40,item_style)
                    sheet.write(i,limit_col+1,70,item_style)
                    sheet.write(i,limit_col+2,35,item_style)
                    sheet.write(i,limit_col+3,40,item_style)
                for i in range(19,20):
                    sheet.write(i,limit_col,35,item_style)
                    sheet.write(i,limit_col+1,70,item_style)
                    sheet.write(i,limit_col+2,30,item_style)
                    sheet.write(i,limit_col+3,35,item_style)
                for i in range(20,21):
                    sheet.write(i,limit_col,45,item_style)
                    sheet.write(i,limit_col+1,70,item_style)
                    sheet.write(i,limit_col+2,40,item_style)
                    sheet.write(i,limit_col+3,45,item_style)
                for i in range(21,22):
                    sheet.write(i,limit_col,40,item_style)
                    sheet.write(i,limit_col+1,70,item_style)
                    sheet.write(i,limit_col+2,35,item_style)
                    sheet.write(i,limit_col+3,40,item_style)
                for i in range(22,23):
                    sheet.write(i,limit_col,35,item_style)
                    sheet.write(i,limit_col+1,70,item_style)
                    sheet.write(i,limit_col+2,30,item_style)
                    sheet.write(i,limit_col+3,35,item_style)
                for i in range(23,27):
                    sheet.write(i,limit_col,'70.0%',item_style)
                    sheet.write(i,limit_col+1,'90.0%',item_style)
                    sheet.write(i,limit_col+2,'60%',item_style)
                    sheet.write(i,limit_col+3,'100%',item_style)
                for i in range(27,31):
                    sheet.write(i,limit_col,0,item_style)
                    sheet.write(i,limit_col+1,6,item_style)
                    sheet.write(i,limit_col+2,6,item_style)
                    sheet.write(i,limit_col+3,10,item_style)
                for i in range(31,33):
                    sheet.write(i,limit_col,0.4,item_style)
                    sheet.write(i,limit_col+1,1,item_style)
                    sheet.write(i,limit_col+2,0.3,item_style)
                    sheet.write(i,limit_col+3,0.4,item_style)
                for i in range(33,34):
                    sheet.write(i,limit_col,0.1,item_style)
                    sheet.write(i,limit_col+1,1,item_style)
                    sheet.write(i,limit_col+2,0.3,item_style)
                    sheet.write(i,limit_col+3,0.1,item_style)
                for i in range(34,36):
                    sheet.write(i,limit_col,0.4,item_style)
                    sheet.write(i,limit_col+1,1,item_style)
                    sheet.write(i,limit_col+2,0.3,item_style)
                    sheet.write(i,limit_col+3,0.4,item_style)
                for i in range(36,41):
                    sheet.write(i,limit_col,'-10%',item_style)
                    sheet.write(i,limit_col+1,'20%',item_style)
                    sheet.write(i,limit_col+2,'',item_style)
                    sheet.write(i,limit_col+3,'',item_style)
                for i in range(41,42):
                    sheet.write(i,limit_col,0,item_style)
                    sheet.write(i,limit_col+1,18,item_style)
                    sheet.write(i,limit_col+2,18,item_style)
                    sheet.write(i,limit_col+3,24,item_style)
                for i in range(42,45):
                    sheet.write(i,limit_col,0,item_style)
                    sheet.write(i,limit_col+1,12,item_style)
                    sheet.write(i,limit_col+2,12,item_style)
                    sheet.write(i,limit_col+3,18,item_style)
                for i in range(45,46):
                    sheet.write(i,limit_col,115,item_style)
                    sheet.write(i,limit_col+1,135,item_style)
                    sheet.write(i,limit_col+2,100,item_style)
                    sheet.write(i,limit_col+3,145,item_style)
                for i in range(46,49):
                    sheet.write(i,limit_col,115,item_style)
                    sheet.write(i,limit_col+1,135,item_style)
                    sheet.write(i,limit_col+2,110,item_style)
                    sheet.write(i,limit_col+3,145,item_style)
                for i in range(49,50):
                    sheet.write(i,limit_col,0,item_style)
                    sheet.write(i,limit_col+1,6,item_style)
                    sheet.write(i,limit_col+2,6,item_style)
                    sheet.write(i,limit_col+3,10,item_style)
                for i in range(50,53):
                    sheet.write(i,limit_col,0,item_style)
                    sheet.write(i,limit_col+1,4,item_style)
                    sheet.write(i,limit_col+2,4,item_style)
                    sheet.write(i,limit_col+3,6,item_style)
                
                

       
                for i in range(len(allFiles)):
                    report=open_workbook(allFiles[i],formatting_info=True)
                    summary=report.sheet_by_index(0)

                    color_row=None;SNR_row=None;uniformity_row=None;resolution_row=None;illumination_row=None;score_col=None
                    j=0
                    while j<summary.nrows:
                        if 'Measured Value' in str(summary.cell_value(j,3)):
                            break
                        j+=1

                    while j<summary.nrows:
                        if 'Color' in str(summary.cell_value(j,0)):
                            color_row=j
                        if 'SNR' in str(summary.cell_value(j,0)):
                            SNR_row=j
                        if 'Uniformity' in str(summary.cell_value(j,0)):
                            #uniformity did not merge all the cells
                            uniformity_row=j-1
                        if 'Resolution' in str(summary.cell_value(j,0)):
                            resolution_row=j
                        if 'Illumination' in str(summary.cell_value(j,0)):
                            illumination_row=j
                        if 'Weighted Score' in str(summary.cell_value(j,13)):
                            score_col=13
                        j+=1
                    print color_row,SNR_row,uniformity_row,resolution_row,illumination_row,score_col

                    

                    if not color_row and not SNR_row and not uniformity_row and not resolution_row and not illumination_row:
                        self.warning+='Cannot find any Measured Value to compare in '+str(allFiles[i])+'\n'
                    else:
                        if color_row:
                            if '2800K' in str(summary.cell_value(color_row,2)) and '6500K' in str(summary.cell_value(color_row+8,2)):
                                for k in range(1):
                                    cell_val=summary.cell_value(color_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,0,18,18,24)
                                    if isinstance(cell_val,float):
                                        sheet.write(5+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(5+k,3+i*2,cell_val,cell_style)
                                for k in range(1,3):
                                    cell_val=summary.cell_value(color_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,0,12,12,18)
                                    if isinstance(cell_val,float):
                                        sheet.write(5+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(5+k,3+i*2,cell_val,cell_style)
                                for k in range(3,4):
                                    cell_val=summary.cell_value(color_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,115,135,100,145)
                                    if isinstance(cell_val,float):
                                        sheet.write(5+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(5+k,3+i*2,cell_val,cell_style)
                                for k in range(4,6):
                                    cell_val=summary.cell_value(color_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,115,135,110,145)
                                    if isinstance(cell_val,float):
                                        sheet.write(5+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(5+k,3+i*2,cell_val,cell_style)
                                for k in range(6,7):
                                    cell_val=summary.cell_value(color_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,0,6,6,10)
                                    if isinstance(cell_val,float):
                                        sheet.write(5+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(5+k,3+i*2,cell_val,cell_style)
                                for k in range(7,9):
                                    cell_val=summary.cell_value(color_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,0,4,4,6)
                                    if isinstance(cell_val,float):
                                        sheet.write(5+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(5+k,3+i*2,cell_val,cell_style)
                            else:
                                sheet.write_merge(5,13,3+i*2,3+i*2,'No Corresponding Data',item_style)
                        else:
                            sheet.write_merge(5,13,3+i*2,3+i*2,'No Data',item_style)
                        if SNR_row:
                            if '500 Lux' in str(summary.cell_value(SNR_row,2)) and '20 Lux' in str(summary.cell_value(SNR_row+8,2)):
                                for k in range(2):
                                    cell_val=summary.cell_value(SNR_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,35,70,30,35)
                                    if isinstance(cell_val,float):
                                        sheet.write(14+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(14+k,3+i*2,cell_val,cell_style)
                                for k in range(2,3):
                                    cell_val=summary.cell_value(SNR_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,25,70,20,25)
                                    if isinstance(cell_val,float):
                                        sheet.write(14+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(14+k,3+i*2,cell_val,cell_style)
                                for k in range(3,4):
                                    cell_val=summary.cell_value(SNR_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,45,70,40,45)
                                    if isinstance(cell_val,float):
                                        sheet.write(14+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(14+k,3+i*2,cell_val,cell_style)
                                for k in range(4,5):
                                    cell_val=summary.cell_value(SNR_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,40,70,35,40)
                                    if isinstance(cell_val,float):
                                        sheet.write(14+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(14+k,3+i*2,cell_val,cell_style)
                                for k in range(5,6):
                                    cell_val=summary.cell_value(SNR_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,35,70,30,35)
                                    if isinstance(cell_val,float):
                                        sheet.write(14+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(14+k,3+i*2,cell_val,cell_style)
                                for k in range(6,7):
                                    cell_val=summary.cell_value(SNR_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,45,70,40,45)
                                    if isinstance(cell_val,float):
                                        sheet.write(14+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(14+k,3+i*2,cell_val,cell_style)
                                for k in range(7,8):
                                    cell_val=summary.cell_value(SNR_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,40,70,35,40)
                                    if isinstance(cell_val,float):
                                        sheet.write(14+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(14+k,3+i*2,cell_val,cell_style)
                                for k in range(8,9):
                                    cell_val=summary.cell_value(SNR_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,35,70,30,35)
                                    if isinstance(cell_val,float):
                                        sheet.write(14+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(14+k,3+i*2,cell_val,cell_style)
                            else:
                                sheet.write_merge(14,22,3+i*2,3+i*2,'No Corresponding Data',item_style)
                        else:
                            sheet.write_merge(14,22,3+i*2,3+i*2,'No Data',item_style)
                        if uniformity_row:
                            if '2800K A' in str(summary.cell_value(uniformity_row,2)) and '6500K' in str(summary.cell_value(uniformity_row+7,2)):
                                for k in range(4):
                                    cell_val=summary.cell_value(uniformity_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,0.7,0.9,0.6,1)
                                    if isinstance(cell_val,float):
                                        sheet.write(23+k,3+i*2,'{:.2%}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(23+k,3+i*2,cell_val,cell_style)
                                for k in range(4,8):
                                    cell_val=summary.cell_value(uniformity_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,0,6,6,10)
                                    if isinstance(cell_val,float):
                                        sheet.write(23+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(23+k,3+i*2,cell_val,cell_style)
                            else:
                                sheet.write_merge(23,30,3+i*2,3+i*2,'No Corresponding Data',item_style)
                        else:
                            sheet.write_merge(23,30,3+i*2,3+i*2,'No Data',item_style)
                        if resolution_row:
                            if '10 cm' in str(summary.cell_value(resolution_row,2)) and '400 cm' in str(summary.cell_value(resolution_row+9,2)):
                                for k in range(2):
                                    cell_val=summary.cell_value(resolution_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,0.4,2,None,None)
                                    if isinstance(cell_val,float):
                                        sheet.write(31+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(31+k,3+i*2,cell_val,cell_style)
                                for k in range(2,3):
                                    cell_val=summary.cell_value(resolution_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,0.1,2,None,None)
                                    if isinstance(cell_val,float):
                                        sheet.write(31+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(31+k,3+i*2,cell_val,cell_style)
                                for k in range(3,5):
                                    cell_val=summary.cell_value(resolution_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,0.4,2,None,None)
                                    if isinstance(cell_val,float):
                                        sheet.write(31+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(31+k,3+i*2,cell_val,cell_style)
                                for k in range(5,10):
                                    cell_val=summary.cell_value(resolution_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,-0.1,0.2,None,None)
                                    if isinstance(cell_val,float):
                                        sheet.write(31+k,3+i*2,'{:.2%}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(31+k,3+i*2,cell_val,cell_style)
                            else:
                                sheet.write_merge(31,40,3+i*2,3+i*2,'No Corresponding Data',item_style)
                        else:
                            sheet.write_merge(31,40,3+i*2,3+i*2,'No Data',item_style)
                        if illumination_row:
                            if '2800K' in str(summary.cell_value(illumination_row,2)) and '0Lux' in str(summary.cell_value(illumination_row+8,2)):
                                for k in range(1):
                                    cell_val=summary.cell_value(illumination_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,0,18,18,24)
                                    if isinstance(cell_val,float):
                                        sheet.write(41+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(41+k,3+i*2,cell_val,cell_style)
                                for k in range(1,4):
                                    cell_val=summary.cell_value(illumination_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,0,12,12,18)
                                    if isinstance(cell_val,float):
                                        sheet.write(41+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(41+k,3+i*2,cell_val,cell_style)
                                for k in range(4,5):
                                    cell_val=summary.cell_value(illumination_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,115,135,100,145)
                                    if isinstance(cell_val,float):
                                        sheet.write(41+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(41+k,3+i*2,cell_val,cell_style)
                                for k in range(5,8):
                                    cell_val=summary.cell_value(illumination_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,115,135,110,145)
                                    if isinstance(cell_val,float):
                                        sheet.write(41+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(41+k,3+i*2,cell_val,cell_style)
                                for k in range(8,9):
                                    cell_val=summary.cell_value(illumination_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,0,6,6,10)
                                    if isinstance(cell_val,float):
                                        sheet.write(41+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(41+k,3+i*2,cell_val,cell_style)
                                for k in range(9,12):
                                    cell_val=summary.cell_value(illumination_row+k,3)
                                    cell_style=self.getCellStyle(cell_val,0,4,4,6)
                                    if isinstance(cell_val,float):
                                        sheet.write(41+k,3+i*2,'{0:.2f}'.format(cell_val),cell_style)
                                    else:
                                        sheet.write(41+k,3+i*2,cell_val,cell_style)
                            else:
                                sheet.write_merge(41,52,3+i*2,3+i*2,'No Corresponding Data',item_style)
                        else:
                            sheet.write_merge(41,52,3+i*2,3+i*2,'No Data',item_style)
                        if score_col:
                            if color_row:
                                cell_val=summary.cell_value(color_row,score_col)
                                if isinstance(cell_val,float):
                                    sheet.write_merge(5,13,4+i*2,4+i*2,'{0:.2f}'.format(cell_val),item_style)
                                else:
                                    sheet.write_merge(5,13,4+i*2,4+i*2,cell_val,item_style)
                            else:
                                sheet.write_merge(5,13,4+i*2,4+i*2,'No Corresponding Data',item_style)
                            if SNR_row:
                                cell_val=summary.cell_value(SNR_row,score_col)
                                if isinstance(cell_val,float):
                                    sheet.write_merge(14,22,4+i*2,4+i*2,'{0:.2f}'.format(cell_val),item_style)
                                else:
                                    sheet.write_merge(14,22,4+i*2,4+i*2,cell_val,item_style)
                            else:
                                sheet.write_merge(14,22,4+i*2,4+i*2,'No Corresponding Data',item_style)
                            if uniformity_row:
                                cell_val=summary.cell_value(uniformity_row,score_col)
                                if isinstance(cell_val,float):
                                    sheet.write_merge(23,30,4+i*2,4+i*2,'{0:.2f}'.format(cell_val),item_style)
                                else:
                                    sheet.write_merge(23,30,4+i*2,4+i*2,cell_val,item_style)
                            else:
                                sheet.write_merge(23,30,4+i*2,4+i*2,'No Corresponding Data',item_style)
                            if resolution_row:
                                cell_val=summary.cell_value(resolution_row,score_col)
                                if isinstance(cell_val,float):
                                    sheet.write_merge(31,40,4+i*2,4+i*2,'{0:.2f}'.format(cell_val),item_style)
                                else:
                                    sheet.write_merge(31,40,4+i*2,4+i*2,cell_val,item_style)
                            else:
                                sheet.write_merge(31,40,4+i*2,4+i*2,'No Corresponding Data',item_style)
                            if illumination_row:
                                cell_val=summary.cell_value(illumination_row,score_col)
                                if isinstance(cell_val,float):
                                    sheet.write_merge(41,52,4+i*2,4+i*2,'{0:.2f}'.format(cell_val),item_style)
                                else:
                                    sheet.write_merge(41,52,4+i*2,4+i*2,cell_val,item_style)
                            else:
                                sheet.write_merge(41,52,4+i*2,4+i*2,'No Corresponding Data',item_style)

                book.save('front_comparison.xls')
                tkMessageBox.showinfo('Notice',self.warning)




    def getCellStyle(self,value,greenLow,greenUpp,yellowLow,yellowUpp):

        cell_style=XFStyle()
        cell_style.font.name='Calibri'
        cell_style.alignment.horz=Alignment.HORZ_CENTER
        cell_style.alignment.vert=Alignment.VERT_CENTER
        cell_style.borders.left=Borders.THIN
        cell_style.borders.right=Borders.THIN
        cell_style.borders.top=Borders.THIN
        cell_style.borders.bottom=Borders.THIN
        cell_style.pattern.pattern=Pattern.SOLID_PATTERN

        if isinstance(value,float) and value>=greenLow and value<=greenUpp:
            cell_style.pattern.pattern_fore_colour=17
        elif not yellowLow and not yellowUpp:
            cell_style.pattern.pattern_fore_colour=29
        elif isinstance(value,float) and value>=yellowLow and value<=yellowUpp:
            cell_style.pattern.pattern_fore_colour=5
        else:
            cell_style.pattern.pattern_fore_colour=2

        return cell_style



window=Tk()
window.title('Comparison Generator GUI by Xiaopei Zhang')
window.geometry('600x200')
app=Application(window)
window.mainloop()
print app.warning


