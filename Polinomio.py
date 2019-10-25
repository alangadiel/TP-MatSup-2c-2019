class Polinomio():
	def __init__(self, coeficientes):
		"""Crea un polinomio a partir de una lista con sus coeficientes
		[1,2,3] => 1+2x+3x**2
		"""
		self.coefs = list(coeficientes)

	def __str__(self):
		res = ""
		if len(self.coefs)==0:
			return res
		else:
			for i in range(0,len(self.coefs)):
				if i==0:
					res += str(self.coefs[i])
				else:
					res += str(self.coefs[i]) + "x^{}".format(i)
				if i!=len(self.coefs)-1:
					res += " + "
			return res
	
	def __len__(self):
		return len(self.coefs)
	
	def grado(self):
		return len(self.coefs)-1
		
	def evaluar(self, x):
		res = 0
		for i in range(0, self.grado()+1):
			res += self.coefs[i]*x**i
		return res
	
	def __add__(self, otro):
		"""Suma 2 polinomios y devuelve un polinomio resultado de la suma"""
		coef_p1 = self.coefs
		coef_p2 = otro.coefs
		#expando la lista de coeficientes hasta que igualen al grado mas alto
		if len(coef_p1)!=len(coef_p2):
			if len(coef_p1)>len(coef_p2):
				coef_p2 = coef_p2 + [0]*(len(coef_p1) - len(coef_p2))
			else:
				coef_p1 = coef_p1 + [0]*(len(coef_p2) - len(coef_p1))
		res = Polinomio([0]*len(coef_p1))
		for i in range(0, len(res)):
			res.coefs[i] = res.coefs[i] + coef_p1[i] + coef_p2[i]
		return res
	
	def aumentargrado(self, i):
		pol = Polinomio([0]*len(self.coefs))
		pol = pol + self
		pol.coefs = [0]*i + pol.coefs
		return pol
	
	def multesc(self, k):
		pol = Polinomio(self.coefs)
		for i in range(0, len(pol.coefs)):
			pol.coefs[i] = pol.coefs[i]*k
		return pol
	
	def __mul__(self, otro):
		"""Multiplica 2 polinomios y devuelve un polinomio resultado de la multiplicacion"""
		pol = Polinomio([0])
		for i in range(0, len(otro.coefs)):
		#	print("Coeficiente: {}".format(otro.coefs[i]))
		#	print("Parte {0} = {1}".format(i,self.multesc(otro.coefs[i]).aumentargrado(i)))
			pol = pol + self.multesc(otro.coefs[i]).aumentargrado(i)
		#	print("Polinomio: {}".format(pol))
			
		return pol
