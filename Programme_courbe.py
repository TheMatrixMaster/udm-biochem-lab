import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

pd.options.display.max_columns = 100
pd.options.display.max_rows = 100

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

def configure_labels(label, cut='Ia J', fill=''):
	label = label.dropna()
	n_label = []
	for n, l in enumerate(label):
		l1 = l.replace(cut, fill)
		n_label.append(l1)
	return n_label	

def split_and_sort_ID(dataframe, ID):
	letters = []
	numbers = []
	for id_ in ID:
		new_ID = list(id_)
		letters.append(new_ID[0])
		s = ''
		numbers.append(int(s.join(new_ID[1:])))

	dataframe['letters'] = letters	
	dataframe['numbers'] = numbers
	new_df = dataframe.sort_values(by=['letters', 'numbers'])
	return new_df

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

def helper_func(ind, list_):
	x = []
	for l in list_:
		new_l = l/ind
		x.append(new_l)
	return x	

def find_R_mean_and_R_STD(mean, STD):
	rel_mean = []
	rel_STD = []
	submeans = separate_values(mean, 5)
	for list_ in submeans:
		indicator = list_[0]
		for number in list_:
			r = number / indicator
			rel_mean.append(r)

	for i, number in enumerate(mean):
		s = STD[i] / number * rel_mean[i]
		rel_STD.append(s)			

	rel_mean = separate_values(rel_mean, 5)
	return rel_mean, rel_STD	


def print_graph(n_days, rel_mean, title='', xlabel='', ylabel=''):
	plt.plot(n_days, rel_mean[0], color='r', label='V NTC')
	plt.plot(n_days, rel_mean[1], color='b', label='V shS1')
	plt.plot(n_days, rel_mean[2], color='k', label='5A NTC')
	plt.plot(n_days, rel_mean[3], color='g', label='5A shS1')

	plt.scatter(n_days, rel_mean[0], color='r')
	plt.scatter(n_days, rel_mean[1], color='b')
	plt.scatter(n_days, rel_mean[2], color='k')
	plt.scatter(n_days, rel_mean[3], color='g')

	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.legend()
	plt.title(title)

	plt.show()


df = pd.read_excel('Courbe_Croissance.xlsx', header=0, sheet_name='Sheet2', names=['Label', 'ID', 'Sample#', 'Values', 'Mean', 'STD'])
df = df.drop(columns=['Sample#', 'Mean', 'STD'])
ID = df['ID']
df = split_and_sort_ID(df, ID)

label = df['Label']	
values = df['Values']

labels = configure_labels(label)
sublists = separate_values(values, 3)

mean, STD = find_mean_and_standard_deviation(sublists)
rel_mean, rel_STD = find_R_mean_and_R_STD(mean, STD)

#print(df.head(n=100))
#print(rel_mean)
n_days = [0, 2, 4, 6, 8]
print_graph(n_days, rel_mean, title='Title', xlabel='', ylabel='')


