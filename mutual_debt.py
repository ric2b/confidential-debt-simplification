from collections import defaultdict
from operator import itemgetter

def compute_totals(totals_dict: defaultdict(int), uome_list: list) -> dict:
	#Receive in input a dictionary containing previous computed totals and a list of UOMe with this form: {collector, debtor, value}.
	#The output is a dictionary that associates to each user (debtor or collector) his own total.
	
	for uome in uome_list:
		totals_dict[uome[0]] -= uome[2] 
		totals_dict[uome[1]] += uome[2]
		
	return totals_dict
	
def debtors_and_collectors(totals_dict:dict) -> (list, list):
	#Receive input a dictionary with a total associated to each user. 
	#Outputs are two dictionaries listing debtors and collectors with their respective total debt or credit
	
	debtors = [] 
	collectors = []
	
	for user in totals_dict:
		if totals_dict[user] > 0:
			debtors.append([user, totals_dict[user]])
		elif totals_dict[user] < 0:
			collectors.append([user, -totals_dict[user]])
	
	debtors.sort(key=itemgetter(1), reverse = True)
	collectors.sort(key=itemgetter(1), reverse = True)
	
	return debtors, collectors
	
def debt_simplification(debtors: list, collectors: list) -> (list):
	#Inputs are two dictionaries containing debtors and collectors.
	#The output is a list of simplified UOMe {collector, debtor, value}
	
	new_UOMe = []
	
	for collector in collectors:
		for debtor in debtors:
			credit, debt = collector[1], debtor[1]
			
			if credit != 0 and debt != 0:
				if credit >= debt:
					new_UOMe.append([collector[0], debtor[0], debt])
					debtor[1] = 0
					collector[1] -= debt
				else:
					debtor[1] -= credit 
					collector[1] = 0
					new_UOMe.append([collector[0], debtor[0], debt-credit])
		
	return new_UOMe


if __name__ == '__main__':

	prev_totals = defaultdict(int)
	uome_list = [['A','B', 5], ['B','A', 2], ['B','C', 1], ['C', 'A', 4]]

	totals = compute_totals(prev_totals, uome_list)
	print(totals)
	debtors, collectors = debtors_and_collectors(totals)
	semplif = debt_simplification(debtors, collectors)
	print(semplif)



