import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pyqtgraph as pg
import time
from datetime import datetime
import pickle
import math
import os
import re
import pandas as pd
import collections
import matplotlib
matplotlib.style.use('ggplot')
import time
import matplotlib.colors as mcolors
from matplotlib import colors
import sys
import csv
from PyQt4 import QtGui,QtCore
from datetime import date, timedelta as td

class Window(QtGui.QMainWindow):
	def __init__(self):
		super(Window,self).__init__() #return parent object
		self.setGeometry(100,100,500,300)
		self.setWindowTitle("LongWall")
		self.setWindowIcon(QtGui.QIcon('LW.png'))

		p = QtGui.QPalette()
		brush = QtGui.QBrush(QtCore.Qt.white,QtGui.QPixmap('LWBG.png'))
		p.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Window,brush)
		p.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Window,brush)
		p.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Window,brush)
		self.setPalette(p)


		openEditor = QtGui.QAction("&Editor", self)
		openEditor.setShortcut("Ctrl+E")
		openEditor.setStatusTip('Open Editor')
		openEditor.triggered.connect(self.editor)

		openFile = QtGui.QAction("&Open File", self)
		openFile.setShortcut("Ctrl+O")
		openFile.setStatusTip('Open File')
		openFile.triggered.connect(self.file_open)

		saveFile = QtGui.QAction("&Save File", self)
		saveFile.setShortcut("Ctrl+S")
		saveFile.setStatusTip('Save File')
		saveFile.triggered.connect(self.file_save)

		self.statusBar()

		mainMenu = self.menuBar()
		fileMenu = mainMenu.addMenu('&File')
		fileMenu.addAction(openFile)
		fileMenu.addAction(saveFile)

		editorMenu = mainMenu.addMenu('&Editor')
		editorMenu.addAction(openEditor)

		self.home()

	def color_picker(self):
		color=QtGui.QColorDialog.getColor()
		self.styleChoice.setStyleSheet("QWidget {background-color: %s}"%color.name())


	def file_save(self):
		name=QtGui.QFileDialog.getSaveFileName(self,'Save File')
		file = open(name,'w')
		text=self.textEdit.toPlainText()
		file.write(text)
		file.close()

	def editor(self):
		self.textEdit=QtGui.QTextEdit()
		self.setCentralWidget(self.textEdit)

	def font_choice(self):
		font,valid=QtGui.QFontDialog.getFont()
		if valid:
			self.styleChoice.setFont(font)

	def style_choice(self,text,tex):
		print text
		print tex
		# self.styleChoice.setText(text)
		# QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(text))

	def download(self):
		self.completed=0

		while self.completed<100:
			self.completed+=0.00005
			self.progress.setValue(self.completed)
			pass

	def enlarge_window(self,state):
		if state==QtCore.Qt.Checked:
			self.setGeometry(50,50,1000,600)
		else:
			self.setGeometry(50,50,500,300)

	def close_application(self):
		choice=QtGui.QMessageBox.question(self,'Extract!',
											"Get into the chopper?",
											QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)
		if choice==QtGui.QMessageBox.Yes:
			print("Extracting Naaaoooww!!")
			sys.exit()
		else:
			pass


	def home(self):
		btn=QtGui.QPushButton("Quit",self)
		btn.clicked.connect(self.close_application)
		btn.resize(btn.minimumSizeHint())
		btn.move(175,150)

		self.progress=QtGui.QProgressBar(self)
		self.progress.setGeometry(175,125,250,20)
		lists=[]
		try:
			infile = open("Dates.p", 'rb')
		except:
			pass
		while 1:
			try:
				# print "appending"
				lists.append(pickle.load(infile))
			except:
				break

		comboBox=QtGui.QComboBox(self)
		for i in lists:
			i=str(i)
			i=i[2:-2]
			i=i.split(".csv")
			comboBox.addItem(i[0])


		comboBox.setGeometry(50,250,80,25)
		# self.styleChoice.move(50,150)
		# comboBox.activated[str].connect(self.style_choice)

		spinBox=QtGui.QSpinBox(self)
		spinBox.setGeometry(130,250,100,25)
		# spinBox.move(200,250)
		spinBox.setPrefix("No. of Days: ")
		spinBox.setMinimum(1)
		spinBox.setMaximum(len(lists))
		# spinBox.valueChanged.connect(self.style_choice)
		# print comboBox.currentText()
		# self.style_choice(spinBox.value(),comboBox.currentText())
		spinBox1=QtGui.QSpinBox(self)
		spinBox1.setGeometry(230,250,100,25)
		spinBox1.setPrefix("Group in: ")
		spinBox1.setMinimum(5)
		spinBox1.setSingleStep(5)
		spinBox1.setMaximum(20)

		btn = QtGui.QPushButton("Plot", self)
		btn.clicked.connect(lambda: self.plot(comboBox.currentText(),spinBox.value(),spinBox1.value()))
		btn.resize(btn.minimumSizeHint())
		btn.setGeometry(340, 250,100,25)


		self.show()
	def plot(self,start,no_of_days,group):
		print "Plotting!!"
		start=str(start)
		lists = []
		infile = open("Data.p", 'rb')
		while 1:
			try:
				lists.append(dict(pickle.load(infile)))
			except:
				break
		infile.close()

		li = []
		for i in range(0, len(lists)):
			if (start in lists[i]['Day']):
				for j in range(0, no_of_days):
					li.append(lists[i + j])
				break

		p = {}
		for l in li:
			for i in l.keys()[0:-1]:
				try:
					for j in l[i]:
						p[i].append(j[0][0] / 9.81)
				except:
					p[i] = []
					for j in l[i]:
						p[i].append(j[0][0] / 9.81)
		max_length = 2
		for i in p.keys():
			if (len(p[i]) >= max_length):
				max_length = len(p[i])

		for i in p.iteritems():
			t = {}
			if len(i[1]) < max_length:
				p[i[0]] = i[1] + [0 for _ in range(max_length - len(i[1]))]
		df = pd.DataFrame(p.items(), columns=['Valve', 'Y'])
		l1 = []
		for i in range(1, max_length + 1):
			l1.append('Y' + str(i))
		df[l1] = pd.DataFrame([x for x in df.Y])
		df = df.drop('Y', axis=1)
		df = df.set_index('Valve')
		# df = df.transpose()

		nrows, ncols = df.shape[0], df.shape[1]

		m = df.as_matrix()
		row_labels = df.columns.values.tolist()
		col_labels = df.transpose().columns.values.tolist()
		# print col_labels
		# df=df.transpose()
		# cmap = colors.ListedColormap(['white','green', 'yellow', 'red', 'black'])
		# bounds = [0, m.min()+1,35,38,42, m.max()]
		cmap = colors.ListedColormap(['white','green', 'red', 'black'])
		
		bounds = [0, m.min()+1,37,42, m.max()]
		norm = colors.BoundaryNorm(bounds, cmap.N)

		fig = plt.figure(figsize=(8,20))
		a1 = plt.subplot(111)
		cax = a1.imshow(m, interpolation='nearest', origin='lower',
						cmap=cmap, norm=norm)
		# a1.set_xticks(range(ncols), row_labels)
		ncols=math.ceil(ncols)
		ncols=int(ncols)
		nc=range(1,ncols+1,5)
		nr=range(1,nrows,group)
		# ncols=ncols+1
		# a1.set_xticks(range(ncols), nc)
		# print nc , nr
		a1.set_xticks(nc)
		# plt.xticks(nc,[i*0.85 for i in nc])
		# print row_labels
		a1.set_xticklabels(row_labels)
		a1.set_yticks(range(nrows), col_labels)
		fig.colorbar(cax)
		# plt.tight_layout(pad=5, w_pad=0, h_pad=1.0)
		# plt.show()
		# print type(cax)
		# print
		s=start+str(no_of_days)
		fig.savefig(s+".jpg")
		lists = []
		infile = open("Data.p", 'rb')
		while 1:
			try:
				lists.append(dict(pickle.load(infile)))
			except :
				break
		infile.close()
		li = []
		for i in range(0,len(lists)):
			if(start in lists[i]['Day']):
				for j in range(0,no_of_days):
					li.append(lists[i+j])
				break
		main=[]
		f =  pickle.load( open( "dated.p", "rb" ) )
		for l in li:
			#ver=pd.read_excel("/home/prithvi/Downloads/"+l['Day'])
			t_average = []
			for i in l.keys()[0:-5]:
				d={}
				d['S'+str(i)+'Val'] = [[],[]]
				for j in l[i]:
					d['S'+str(i)+'Val'][0].append(j[1][1])
					d['S'+str(i)+'Val'][1].append(j[0][1])
				t_average.append(d)
			max_point = 1
			time = []
			m=[]
			for i in t_average:
				for key in i:
					if(len(i[key][0]) >max_point):
						max_point = len(i[key][0])
						valve = t_average.index(i)
						ke=key
			#print ke
			for j in t_average[valve][ke][0]:
				if j==0:
					 continue
				else:
					time.append(f.loc[j])
					m.append(j)
			c=[]
			for k in range(0,len(time)):
				if k==0:
					c.append(l['Day']+":"+"00:00:00"+'-'+str(time[k]).split(" ")[1])
				else:
					c.append(l['Day']+":"+str(time[k-1]).split(" ")[1] + "-" + str(time[k]).split(" ")[1])
			c.append(l['Day'] + ":" + str(time[len(time)-1]).split(" ")[1] + "-" + "23:59:59")
			c.append('Valve')
			df_data=[]
			for j in range(0,len(t_average)):
				s = []
				if (t_average[j].keys()[0] == ke):
					for o in t_average[j].values()[0][1]:
						if o==None:
							continue
						else:
							index = t_average[j].values()[0][1].index(o)
							ele = l[int(t_average[j].keys()[0].split("V")[0].split("S")[1])][index][0][0]
							s.append(ele)
							#s.append(ver[t_average[j].keys()[0]].loc[o])
					s.append(s[-1])
					s[:] = [x / 9.81 for x in s]
					s.append(j+1)
				else:
					avg = [[] for _ in range(len(c)-1)]
					a = t_average[j].values()[0][0]
					b = t_average[j].values()[0][1]
					for o in range(0,len(a)):
						try:
							#avg[[n for n,i in enumerate(m) if i>=a[o]][0]].append(ver[t_average[j].keys()[0]].loc[b[o]])
							avg[[n for n,i in enumerate(m) if i>=a[o]][0]].append(l[int(t_average[j].keys()[0].split("V")[0].split("S")[1])][o][0][0])
						except IndexError:
							avg[-1].append(l[int(t_average[j].keys()[0].split("V")[0].split("S")[1])][o][0][0]) 
							#avg[-1].append(ver[t_average[j].keys()[0]].loc[b[o]]) 
					if all(u==0 for u in [len(v) for v in avg]):
						continue
					else:
						pass
					ne_values = [p for p in range(0,len(avg)) if avg[p]]
					e_values = [p for p in range(0,len(avg)) if not avg[p]]
					for e in e_values:
						try:
							v = [ n for n,i in enumerate(ne_values) if i>e ][0]
							if v==0:
								avg[e].append(avg[ne_values[v]][0])
							else:
								av = (avg[ne_values[v]][0] + avg[ne_values[v-1]][-1])/2
								avg[e].append(av)
						except IndexError:
								avg[e].append(avg[ne_values[-1]][-1])
					s = [(sum(v)/float(len(v)))/9.81 for v in avg]
					s.append(j+1)
				df_data.append(s)
			r = pd.DataFrame(np.array(df_data),columns=c)
			df1 = r[c[0:len(c)-1]]
			# print group
			group=145
			i = int(r.shape[0]/group)
			j=0
			a=[]
			while(j<i):
				aDict={}
				for k in df1.columns.values.tolist():
					aDict[k]=df1[k][j*group:(j+1)*group].mean()
				a.append(aDict)
				j=j+1
			if(j*group<r.shape[0]):
				aDict={}
				for k in df1.columns.values.tolist():
					aDict[k]=df1[k][j*group:(j+1)*group].mean()
				a.append(aDict)
			if(li.index(l)==0):
				main = pd.DataFrame(a)
			else:
				main = pd.concat([main, pd.DataFrame(a)], axis=1)
		main.fillna(0, inplace=True)
		nrows, ncols = main.shape[0],main.shape[1]
		m= main.as_matrix()
		row_labels = main.columns.values.tolist()
		col_labels = main.transpose().columns.values.tolist()
		# cmap = colors.ListedColormap(['blue', 'green' ,'yellow','red','black' ])
		# bounds=[m.min(),20,25,30,35,m.max()]
		cmap = colors.ListedColormap(['green', 'red', 'black'])
		bounds = [0,37,42, m.max()]
		norm = colors.BoundaryNorm(bounds, cmap.N)
		fig = plt.figure(figsize=(2,5))
		a1 = fig.add_subplot(111)
		cax = a1.matshow(m, interpolation='nearest', origin='lower',
							cmap=cmap, norm=norm)

		ncols=math.ceil(ncols)
		ncols=int(ncols)
		nc=range(1,ncols+1,20)
		nr=range(1,nrows,5)
		# ncols=ncols+1
		# a1.set_xticks(range(ncols), nc)
		# print nc , nr
		a1.set_xticks(nc)
		# plt.xticks(nc,[i*0.85 for i in nc])
		a1.set_xticklabels([i*0.85 for i in nc])
		# a1.set_xticklabels([i for i in row_labels])
		# print row_labels
		# print ncols, nrows
		a1.set_yticks(nr)
		a1.set_yticklabels([i*group for i in nr])
		fig.colorbar(cax)
		# plt.tight_layout()
		plt.show()
		#fig.savefig(f + ".jpg")

	def file_open(self):
		f=QtGui.QFileDialog.getOpenFileName(self,'Open File')

		flag=1

		if f:
			try:
				ver=pd.read_csv(str(f))
			except:
				ver=pd.read_excel(str(f),sheetname=1)
		else:
			print "Chose Nothing!!"
			self.home()

		lists = []
		try:
			infile = open("Dates.p", 'rb')
		except:
			pass

		while 1:
			try:
				# print "appending"
				lists.append(pickle.load(infile))
			except:
				break
	   
		li = []
		day = os.path.basename(str(f))
		for i in lists:
			if i == [day]:
				flag=0
				print "is in file"
				break

		if flag:
			column_names = ver.columns.values.tolist()[1:]
			d = []
			d1_2=[]
			d1 = []
			d2 = []
			d3 = []
			tm = 100
			ti = 270
			t_average = []
			for k in column_names:
				# l = ver[['Logtime',k.encode("ascii","ignore"),'time']]
				l = ver[['Logtime', k.encode("ascii", "ignore")]]
				p2time = []
				p1time = []
				p3time = []
				i = int(8634 / tm)
				j = 0
				while (j < i):
					median = l[j * tm:(j + 1) * tm][k.encode("ascii", "ignore")].median()
					minm = l[j * tm:(j + 1) * tm][k.encode("ascii", "ignore")].min()
					th = median / 3
					if (median - minm) > th:
						m = l[j * tm:(j + 1) * tm][k.encode("ascii", "ignore")].idxmin()
						if len(p2time) == 0 or (m - p2time[len(p2time) - 1]) >= ti:
							pass
						else:
							j = j + 1
							continue
						p2 = minm
						if m <= 30 and m != 0:
							max_list = l[0:m][k.encode("ascii", "ignore")].tolist()
							a = max(max_list)
							maxi = 0
							for b in range(0, len(max_list)):
								if (max_list[b] == a):
									maxi = b
							p1 = l[k.encode("ascii", "ignore")].loc[maxi]
							if p1 > 50 and p1 > p2:
								pass
							else:
								j +=1
								continue
							p2time.append(l[j * tm:(j + 1) * tm][k.encode("ascii", "ignore")].idxmin())
							p2t=(l[j * tm:(j + 1) * tm][k.encode("ascii", "ignore")].idxmin())
							p1time.append(maxi)
							p1t=maxi
							p3 = l[k.encode("ascii", "ignore")].loc[m + 30]
							p3time.append(m + 30)
							p3t=m+30
							di = {'valve': k.encode("ascii", "ignore"), 'day': f, 'p1': [p1, l['Logtime'].loc[maxi]],
								  'p2': [p2, l['Logtime'].loc[m]], 'p3': [p3, l['Logtime'].loc[m + 30]]}
							di1 = {'valve': int(re.search(r'\d+', k).group()), 'p1': [p1, p1t]}
							di2 = {'valve': int(re.search(r'\d+', k).group()), 'p2': [p2, p2t]}
							di3 = {'valve': int(re.search(r'\d+', k).group()), 'p3': [p3, p3t]}
							di1_2 = {'valve': int(re.search(r'\d+', k).group()), 'p': [[p1, p1t], [p2, p2t]]}
							d1_2.append(di1_2)
							d.append(di)
							d1.append(di1)
							d2.append(di2)
							d3.append(di3)
						elif m >= 8604:
							max_list = l[m - 30:m][k.encode("ascii", "ignore")].tolist()
							a = max(max_list)
							maxi = 0
							for b in range(0, len(max_list)):
								if max_list[b] == a:
									maxi = b
							p1 = l[k.encode("ascii", "ignore")].loc[m - 30 + maxi]
							if p1 > 50 and p1 > p2:
								pass
							else:
								j+=1
								continue
							p2time.append(l[j * tm:(j + 1) * tm][k.encode("ascii", "ignore")].idxmin())
							p2t=(l[j * tm:(j + 1) * tm][k.encode("ascii", "ignore")].idxmin())
							p1time.append(m - 30 + maxi)
							p1t=(m - 30 + maxi)
							p3 = l[k.encode("ascii", "ignore")].loc[8633]
							p3time.append(8633)
							p3t=(8633)
							di = {'valve': k.encode("ascii", "ignore"), 'day': f,
								  'p1': [p1, l['Logtime'].loc[m - 30 + maxi]], 'p2': [p2, l['Logtime'].loc[m]],
								  'p3': [p3, l['Logtime'].loc[8633]]}
							di1 = {'valve': int(re.search(r'\d+', k).group()), 'p1': [p1, p1t]}
							di2 = {'valve': int(re.search(r'\d+', k).group()), 'p2': [p2, p2t]}
							di3 = {'valve': int(re.search(r'\d+', k).group()), 'p3': [p3, p3t]}
							di1_2 = {'valve': int(re.search(r'\d+', k).group()), 'p': [[p1, p1t], [p2, p2t]]}
							d1_2.append(di1_2)
							d.append(di)
							d1.append(di1)
							d2.append(di2)
							d3.append(di3)
						elif m != 0:
							max_list = l[m - 30:m][k.encode("ascii", "ignore")].tolist()
							a = max(max_list)
							maxi = 0
							for b in range(0, len(max_list)):
								if max_list[b] == a:
									maxi = b
							p1 = l[k.encode("ascii", "ignore")].loc[m - 30 + maxi]
							if p1 > 50 and p1 > p2:
								pass
							else:
								j += 1
								continue
							p2time.append(l[j * tm:(j + 1) * tm][k.encode("ascii", "ignore")].idxmin())
							p2t=(l[j * tm:(j + 1) * tm][k.encode("ascii", "ignore")].idxmin())
							p1time.append(m - 30 + maxi)
							p1t=(m - 30 + maxi)
							p3 = l[k.encode("ascii", "ignore")].loc[m + 30]
							p3time.append(m + 30)
							p3t=(m + 30)
							di = {'valve': k.encode("ascii", "ignore"), 'day': f,
								  'p1': [p1, l['Logtime'].loc[m - 30 + maxi]], 'p2': [p2, l['Logtime'].loc[m]],
								  'p3': [p3, l['Logtime'].loc[m + 30]]}
							di1 = {'valve': int(re.search(r'\d+', k).group()), 'p1': [p1, p1t]}
							di2 = {'valve': int(re.search(r'\d+', k).group()), 'p2': [p2, p2t]}
							di3 = {'valve': int(re.search(r'\d+', k).group()), 'p3': [p3, p3t]}
							di1_2={'valve': int(re.search(r'\d+', k).group()), 'p': [[p1, p1t],[p2,p2t]]}
							d1_2.append(di1_2)
							d.append(di)
							d1.append(di1)
							d2.append(di2)
							d3.append(di3)

					j += 1
			d1_2 = pd.DataFrame(d1_2) # Only those data are here for which there is NON ZERO pressure value
			p1_2valve = set(d1_2['valve'].values.tolist()) # making set so that multiple instance of a valve is removed
			p1_2valve = sorted(list(p1_2valve))


			col_list=[]
			for i in column_names:
				col_list.append(int(re.search(r'\d+', i).group()))

			valves = []
			p1_2dict = dict()
			for i in col_list:
				valves.append(i)
				p1_2dict[i] = []
			gc = [i for i in valves if i not in p1_2valve] # to find the Valve Nos. which didn't work

			for index, row in d1_2.iterrows():              # making dictionary of Valves with key as Valve Nos.
				p1_2dict[row['valve']].append(row['p'])


			p1_2dict = collections.OrderedDict(sorted(p1_2dict.items()))
			# day = os.path.basename(str(f))
			p1_2dict['Day'] = day
			# open the file for writing
			file_Name = "Data.p"
			fileObject = open(file_Name, 'ab')

			# this writes the object a to the
			# file named 'Data.p'
			pickle.dump(p1_2dict, fileObject)

			# here we close the fileObject
			fileObject.close()

			file_Name = "Dates.p"
			fileObject = open(file_Name, 'ab')

			# this writes the object a to the
			# file named 'Data.p'
			pickle.dump([day], fileObject)

			# here we close the fileObject
			fileObject.close()
			# we open the file for reading
			# Below is the procedure for writing in CSV format.. which will not help as it stores in string format
			# head = list(p1_2dict.keys())
			# wr = []
			# with open('D:\BTP\Data\dict.csv', 'ab') as csv_file:
			#     writer = csv.writer(csv_file, delimiter=',')
			#     for key, value in p1_2dict.items():
			#         wr.append(value)
			#     if flag == 2:
			#         writer.writerow(['Day']+head) # Use it first time so that header is created
			#     writer.writerow([f] + wr)
			# csv_file.close()
			#
			# with open('D:\BTP\Data/files.csv', 'ab') as csv_file:
			#     writer = csv.writer(csv_file, delimiter=',')
			#     writer.writerow([f])
			# csv_file.close()
			# d2 = pd.DataFrame(d2) # for minima
			# d3 = pd.DataFrame(d3) # for next setting pressure

			# d1.to_csv("D:\BTP\Data\check1.csv", header=False, index=f)
			# d2.to_csv("D:\BTP\Data\check2.csv", header=False, index=False)
			# d3.to_csv("D:\BTP\Data\check3.csv", header=False, index=False)
		#print lists
		print "written"+str(f)
		self.download()





def run():
	app=QtGui.QApplication(sys.argv)
	GUI=Window()
	sys.exit(app.exec_())

run()