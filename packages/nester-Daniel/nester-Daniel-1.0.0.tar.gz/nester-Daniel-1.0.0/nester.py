#Módulo de teste
def print_lol(a):
    #Função de exibição de listas complexas"""
	for b in a:
		if isinstance(b, list):
			print_lol(b)
		else:
			print(b)
