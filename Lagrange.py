
def InterpolarLagrange(datos):
	""" Pseudocodigo de la funcion
	
	datos.sort() 								# si los datos vienen desordenados
	polint = Polinomio([0])						# Lo inicializo en cero, le voy sumando luego
	n = datos.len() 							# cantidad de pares X,Y para el grado del polinomio
	for i in range(0, n+1):
		ai = yi
		Li = Polinomio([1])
		for j in range(0, n+1):
			if( i == j):
				continue 						#saltea el paso en q coinciden los indices
			polaux = Polinomio( [-xj , 1] )
			Li.multpol(polaux)
		LiXi = Li.evaluar(xi)
		ai = ai/LiXi
		Li.multesc(ai)
		polint.sumarpol(Li)						#suma el polinomio correspondiente a Yi al polinomio interpolante
	return polint
	"""

	return
