class Polinomio():
	def __init__(coeficientes, self):
		"""Crea un polinomio a partir de una lista con sus coeficientes
		[1,2,3] => 1+2x+3x**2
		"""
		self.coefs = coeficientes

	def grado(self):
		return self.coefs.len()-1
		
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
		if length(coef_p1)!=length(coef_p2):
			if length(coef_p1)>length(coef_p2):
				coef_p2 = coef_p2 + [0]*(length(coef_p1) - length(coef_p2))
			else:
				coef_p1 = coef_p1 + [0]*(length(coef_p1) - length(coef_p1))
		res = Polinomio([0]*length(coef_p1))
		for i in range(0, length(res)):
			res.coefs[i] = res.coefs[i] + coef_p1[i] + coef_p2[i]
		return res
	
	def aumentargrado(self, i):
		pol = Polinomio([0]*length(self.coef))
		pol = pol + self
		pol.coef = [0]*i + pol.coef
		return pol
	
	def multesc(self, k):
		pol = Polinomio(self.coef)
		for i in self.coef:
			i = i*k
		return pol
	
	def __mult__(self, otro):
		"""Multiplica 2 polinomios y devuelve un polinomio resultado de la multiplicacion"""
		pol = Polinomio([0])
		for i in range(o, length(otro.coef)):
			pol = pol + self.multesc(otro.coef[i]).aumentargrado(i)
		return pol
