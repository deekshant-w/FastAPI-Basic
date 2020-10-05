__me = ['deekshant wadhwa','deekshant','wadhwa','dk','dkw','dikshant']

def IsItMe(val):
	if(val.lower().strip() in __me):
		return 1
	return 0