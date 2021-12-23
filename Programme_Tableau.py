import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def aberrant_numbers(x):
	dixon_value = 0.63
	x.sort()
	Q1 = abs(x[0] - x[1]) / (x[-1] - x[0])
	Q2 = abs(x[-1] - x[-2]) / (x[-1] - x[0])
	if Q1 > Q2 and Q1 > dixon_value:
		del x[0]
	elif Q2 > Q1 and Q2 > dixon_value:
		del x[-1]	
	return x	

def configure_labels(label, cut='', fill=''):
	label = label.dropna()
	n_label = []
	for n, l in enumerate(label):
		l1 = l.replace(cut, fill)
		n_label.append(l1)
	return n_label	

def create_ID(column):	
	ID = [x for x in range(0, len(column))]
	return ID

def separate_values(values, step):
	values = list(values)
	subvalues = [values[x:x+step] for x in range(0, len(values), step)]
	return subvalues

def find_mean_and_standard_deviation(sublists):
	mean = []
	STD = []
	for list_ in sublists:
		new_list = aberrant_numbers(list_)
		m = sum(new_list) / float(len(new_list))
		mean.append(m)
		
		array_list = np.array(new_list)
		s = np.std(array_list, axis=0)
		STD.append(s)

	return mean, STD	

def find_R_mean_and_R_STD(mean, STD):
	indicator = mean[0]
	rel_mean = []
	rel_STD = []
	for n, i in enumerate(mean):
		rel_m = i / indicator
		rel_mean.append(rel_m)
	
		rel_s = STD[n] / i * rel_mean[n] 
		rel_STD.append(rel_s)

	return rel_mean, rel_STD	

def print_table(labels, rel_mean, rel_STD, title='', xlabel='', ylabel=''):
	plt.bar(labels, rel_mean, width=0.4)
	plt.errorbar(labels, rel_mean, yerr=rel_STD, color='k', fmt='none', capsize=4)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)

	plt.show()


df = pd.read_excel('Final1.xlsx', header=None, sheet_name='n = 1 IMR', names=['Label', 'ID', 'Values'])
ID = df['ID']
label = df['Label']	
values = df['Values']

new_ID = create_ID(ID)
labels = configure_labels(label)
sublists = separate_values(values, 3)
mean, STD = find_mean_and_standard_deviation(sublists)
rel_mean, rel_STD = find_R_mean_and_R_STD(mean, STD)

print_table(labels, rel_mean, rel_STD, title='Title', xlabel='', ylabel='')