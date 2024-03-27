import numpy as np
from scipy.stats import norm
from scipy.stats import chi2

#Util

def truncate(number):
  """
  Trunca un número a 5 decimales.

  Parámetros:
  number (float): El número que se va a truncar.

  Retorna:
  float: El número truncado a 5 decimales.
  """
  return float(f'%.{5}f'%(number))

#Pseudo-random number generation

def generateNumbersByMeanSquares(seed, min, max, quantity):
  """
  Genera números pseudoaleatorios utilizando el método de los cuadrados medios.

  Parámetros:
  seed (int): La semilla inicial para la generación de números pseudoaleatorios.
  min (float): El límite inferior del rango en el que se generan los números.
  max (float): El límite superior del rango en el que se generan los números.
  quantity (int): La cantidad de números pseudoaleatorios a generar.

  Retorna:
  tuple: Una tupla con los siguientes elementos:
    - Ri (list): Lista de números pseudoaleatorios Ri.
    - Xi (list): Lista de valores Xi utilizados en la generación.
    - extractionArr (list): Lista de valores extraídos.
    - extensionArr (list): Lista de longitudes de los valores extraídos.
    - xsquareArr (list): Lista de valores al cuadrado.
    - Ni (list): Lista de números pseudoaleatorios en el rango [min, max].
  """
  Ri = []
  Xi = []
  extractionArr = []
  extensionArr = []
  xsquareArr = []
  xi = seed

  for i in range(quantity):
    Xi.append(xi)
    xi, ri, xsquare, extension, extraction = extractNumber(xi)
    extractionArr.append(extraction)
    extensionArr.append(extension)
    xsquareArr.append(xsquare)
    Ri.append(ri)
  Ni = [min+(max - min)*num for num in Ri]
  return Ri, Xi, extractionArr, extensionArr, xsquareArr, Ni

def extractNumber(xi):
  """
  Extrae un número de una secuencia Xi utilizando el método de los cuadrados medios.

  Parámetros:
  xi (int): El número Xi a extraer.

  Retorna:
  tuple: Una tupla con los siguientes elementos:
    - xi (int): El próximo valor de Xi.
    - ri (float): El número pseudoaleatorio Ri.
    - xsquare (int): El valor de Xi al cuadrado.
    - extension (int): La longitud de xsquare.
    - extraction (str): El valor extraído de xsquare.
  """
  xsquare = np.square(xi)
  extension = len(str(xsquare))
  if(extension >= 6):
    pos = extension - 6
    extraction = str(xsquare)[pos:pos+4]
  elif(extension < 6):
    quantityCharacters = extension - 2
    extraction = str(xsquare)[0:quantityCharacters]
  xi = int(extraction)
  ri = truncate(int(extraction) / 10000)

  return xi, ri, xsquare, extension, extraction

def generateNumbersByLinearCongruential(Xo, k, c, g, min, max, quantity):
  """
  Genera números pseudoaleatorios utilizando el método de congruencia lineal.

  Parámetros:
  Xo (int): La semilla inicial para la generación de números pseudoaleatorios.
  k (int): El valor de k para la generación.
  c (int): El valor de c para la generación.
  g (int): El valor de g para la generación.
  min (float): El límite inferior del rango en el que se generan los números.
  max (float): El límite superior del rango en el que se generan los números.
  quantity (int): La cantidad de números pseudoaleatorios a generar.

  Retorna:
  tuple: Una tupla con los siguientes elementos:
    - Ri (list): Lista de números pseudoaleatorios Ri.
    - Xi (list): Lista de valores Xi utilizados en la generación.
    - Ni (list): Lista de números pseudoaleatorios en el rango [min, max].
  """
  if(not isinstance(g, int) or not(g >= 0)):
    return "Ingrese otro parametro para g"
  m = np.power(2, g)
  a = 1 + 2 * k
  if(not isinstance(k, int) or not(k >= 0 and k < m)):
    return "Ingrese otro parametro para k"
  if(not(a >= 0 and a < m)):
    return "Ingrese otro parametro para k (a)"
  if(not isinstance(Xo, int) or not(Xo >= 0 and Xo < m)):
    return "Ingrese otro parametro para Xo"
  if(not isinstance(c, int) or not(c >=0 and c < m)):
    return "Ingrese otro parametro para c"

  Xi =[]
  Ri = []
  for i in range(0, quantity):
    Xi.append(((a * Xo) + c) % m)
    Xo = Xi[i]
    Ri.append(truncate(Xi[i] / (m - 1)))
  Ni = [min+(max - min)*num for num in Ri]

  return Ri, Xi, Ni

def generateNumbersByMultiplicativeCongruential(Xo, t, g, min, max, quantity):
  """
  Genera números pseudoaleatorios utilizando el método de congruencia multiplicativa.

  Parámetros:
  Xo (int): La semilla inicial para la generación de números pseudoaleatorios.
  t (int): El valor de t para la generación.
  g (int): El valor de g para la generación.
  min (float): El límite inferior del rango en el que se generan los números.
  max (float): El límite superior del rango en el que se generan los números.
  quantity (int): La cantidad de números pseudoaleatorios a generar.

  Retorna:
  tuple: Una tupla con los siguientes elementos:
    - Ri (list): Lista de números pseudoaleatorios Ri.
    - Xi (list): Lista de valores Xi utilizados en la generación.
    - Ni (list): Lista de números pseudoaleatorios en el rango [min, max].
  """
  a = (8 * t) + 3
  m = np.power(2, g)
  Xi = []
  Ri = []
  for i in range(0, quantity):
    Xi.append((Xo * a) % m)
    Ri.append(truncate(Xi[i] / (m - 1)))
    Xo = Xi[i]
  Ni = [min+(max - min)*num for num in Ri]

  return Ri, Xi, Ni


# Genera números pseudoaleatorios distribuidos uniformemente en un rango dado.
# Parámetros:
#   min: Valor mínimo del rango.
#   max: Valor máximo del rango.
#   quantity: Cantidad de números a generar.
# Retorna:
#   Ri: Números pseudoaleatorios generados.
#   Xi: No se usa en esta función.
#   Ni: No se usa en esta función.
def generateNumbersByUniformDistribution(min, max, quantity):
  Ri, Xi, Ni = generateNumbersTested(1,3,6,7,min,max,quantity,10)
  return Ri, Xi, Ni

# Genera números pseudoaleatorios distribuidos normalmente.
# Parámetros:
#   desv: Desviación estándar de la distribución normal.
#   mean: Media de la distribución normal.
#   quantity: Cantidad de números a generar.
# Retorna:
#   Ri: Números pseudoaleatorios generados.
#   Xi: No se usa en esta función.
#   normalDistribuition: Números generados con distribución normal.
def generateNumbersByNormalDistribution(desv, mean, quantity):
  Ri, Xi, Ni = generateNumbersTested(1,3,6,7,3,5,quantity,10)
  normalDistribuition = [norm.ppf(num, loc=mean, scale=desv) for num in Ri]
  return Ri, Xi, normalDistribuition
  
# Realiza la prueba de media para los números pseudoaleatorios generados.
# Parámetros:
#   Ri: Números pseudoaleatorios generados.
# Retorna:
#   Tuple: Resultado de la prueba, alpha, tamaño de la muestra, media, valor auxiliar, Z, límite inferior, límite superior.
def meanTest(Ri):
  size = len(Ri)
  alpha = 0.05
  mean = np.mean(Ri)
  aux = 1 - (alpha / 2)
  Z = truncate(norm.ppf(aux))
  Li = (1 / 2) - (Z * (1 / np.sqrt(12 * size)))
  Ls = (1 / 2) + (Z * (1 / np.sqrt(12 * size)))
  return mean >= Li and mean <= Ls, alpha, size, mean, aux, Z, Li, Ls

# Realiza la prueba de varianza para los números pseudoaleatorios generados.
# Parámetros:
#   Ri: Números pseudoaleatorios generados.
# Retorna:
#   Tuple: Resultado de la prueba, alpha, tamaño de la muestra, varianza, media, alpha/2, 1-(alpha/2), valor de chi-cuadrado inferior, valor de chi-cuadrado superior, límite inferior real, límite superior real.
def varianceTest(Ri):
  size = len(Ri)
  alpha = 0.05
  var = np.var(Ri)
  xsquare = truncate(chi2.isf((alpha / 2), size -1))
  xsquareAux = truncate(chi2.isf(1 - (alpha / 2), size -1))
  LIR = xsquare / (12 * (size-1))
  LSR = xsquareAux / (12 * (size - 1))
  return var >= LSR and var <= LIR, alpha, size, var, np.mean(Ri), alpha/2, 1-(alpha/2), xsquare, xsquareAux, LIR, LSR

# Realiza la prueba de chi-cuadrado para verificar la uniformidad de los números pseudoaleatorios generados.
# Parámetros:
#   Ri: Números pseudoaleatorios generados.
#   nIntervals: Número de intervalos para la prueba.
# Retorna:
#   Tuple: Resultado de la prueba, intervalos, frecuencias observadas, frecuencia esperada, valores de chi-cuadrado, suma de frecuencias, frecuencia esperada real, suma de valores de chi-cuadrado, grados de libertad, valor crítico de chi-cuadrado.
def testChi2Uniformity(Ri, nIntervals):
  minRi = min(Ri)
  initial = minRi
  maxRi = max(Ri)

  sizeInterval = truncate((maxRi - minRi) / nIntervals)
  intervals = createIntervals(nIntervals, sizeInterval, initial)
  frequencies = classifyNumbers(intervals, Ri, minRi, maxRi)
  sumFrequencies = sum(frequencies.values())
  expectedFrequency = sumFrequencies / nIntervals
  chi2Values = []
  for i in frequencies.values():
    chi2Values.append( np.square(i - expectedFrequency) / expectedFrequency)

  return (chi2.isf(0.05, nIntervals - 1)) > sum(chi2Values), intervals, frequencies, expectedFrequency, chi2Values, sum(frequencies.values()), expectedFrequency, sum(chi2Values), nIntervals - 1, chi2.isf(0.05, nIntervals - 1)

# Crea los intervalos para la prueba de chi-cuadrado.
# Parámetros:
#   nIntervals: Número de intervalos.
#   sizeInterval: Tamaño de cada intervalo.
#   initial: Valor inicial del primer intervalo.
# Retorna:
#   Lista de tuplas: Intervalos creados.
def createIntervals(nIntervals, sizeInterval, initial):
  intervals = []
  for i in range(0, nIntervals):
    final = initial + sizeInterval
    intervals.append((truncate(initial), truncate(final)))
    initial = final
  return intervals

# Clasifica los números generados en los intervalos para la prueba de chi-cuadrado.
# Parámetros:
#   intervals: Intervalos a considerar.
#   Ni: Números a clasificar.
#   minNi: Valor mínimo de Ni.
#   maxNi: Valor máximo de Ni.
# Retorna:
#   Diccionario: Frecuencias observadas en cada intervalo.
def classifyNumbers(intervals, Ni, minNi, maxNi):
  frequencies = {interval: 0 for interval in intervals}
  frequencies[intervals[0]] += 1
  frequencies[intervals[len(intervals) - 1]] += 1
  for value in Ni:
      for interval in intervals:
          if value != minNi and value != maxNi and interval[0] < value <= interval[1]:
              frequencies[interval] += 1
              break
  return frequencies


def testKS(Ri, nIntervals):
    """
    Este método calcula la prueba de Kolmogorov-Smirnov (KS) para una secuencia de números Ri.

    Args:
        Ri (list): Una secuencia de números.
        nIntervals (int): El número de intervalos para dividir los datos.

    Returns:
        tuple: Una tupla que contiene un valor booleano que indica si la prueba pasa, 
               seguido de una serie de resultados de la prueba.
    """
    minRi = min(Ri)
    maxRi = max(Ri)
    initial = minRi
    sizeInterval = truncate((maxRi - minRi) / nIntervals)

    intervals = createIntervals(nIntervals, sizeInterval, initial)
    frequencies = classifyNumbers(intervals, Ri, minRi, maxRi)
    expectedFrequencies = [truncate((len(Ri)* (i+1)) / nIntervals) for i in range(0, nIntervals)]

    cumulativeFrequency = []
    actualValue = 0
    for i in frequencies.values():
        actualValue += i
        cumulativeFrequency.append(actualValue)

    percentageObtained = [i / len(Ri) for i in cumulativeFrequency]
    percentageExpected = [i / len(Ri) for i in expectedFrequencies]
    difference = [truncate(np.abs(percentageExpected[i] - percentageObtained[i])) for i in range(0, len(percentageObtained))]

    dicKS = {1:0.97500, 2:0.84189, 3:0.70760, 4:0.62394, 5:0.56328, 6:0.51926, 7:0.48342, 8:0.45427, 9:0.43001, 10:0.40925, 11:0.39122, 12:0.37543, 13:0.36143, 14:0.34890, 15:0.33750, 16:0.32733, 17:0.31796, 18:0.30936, 19:0.30143, 20:0.29408, 21:0.28724, 22:0.28087, 23:0.27491, 24:0.26931, 25:26404, 26:24908, 27:0.25438, 28:0.24993, 29:0.24571, 30:0.24170, 31:0.23788, 32:0.23424, 33:0.23076, 34:0.22743, 35:0.22425, 36:0.22119, 37:0.21826, 38:0.21544, 39:0.21273, 40:0.21012, 41:0.20760, 42:0.20517, 43:0.20283, 44:0.20056, 45:0.19837, 46:0.19625, 47:0.19420, 48:0.19221, 49:0.19028, 50:0.18841}
    maxDiff = max(difference)

    if(len(Ri) <= 50):
        dMaxP = dicKS[len(Ri)]
        return maxDiff < dMaxP, len(Ri), np.mean(Ri), minRi, maxRi, intervals, frequencies, cumulativeFrequency, percentageObtained, expectedFrequencies, percentageExpected, difference, maxDiff, dMaxP
    return maxDiff < 1.36/np.sqrt(len(Ri)), len(Ri), np.mean(Ri), minRi, maxRi, intervals, frequencies, cumulativeFrequency, percentageObtained, expectedFrequencies, percentageExpected, difference, maxDiff, 1.36/np.sqrt(len(Ri))


def classifyNumberPoker(number):
    """
    Clasifica un número en una categoría de poker basado en la frecuencia de sus dígitos.

    Args:
        number (int): Un número entero.

    Returns:
        str: La categoría de poker ("D", "O", "T", "K", "F", "P", "Q").
    """
    numberStr = str(number)[2:]
    if(len(numberStr) < 5):
        while (len(numberStr) < 5):
            numberStr += '0'

    numbers = {i: 0 for i in range(0, 10)}

    for value in numberStr:
        numbers[int(value)] += 1

    numbers = [i for i in numbers.values() if i > 0]
    if(len(numbers) == 5):
        return "D"
    elif(5 in numbers) :
        return "Q"
    elif(4 in numbers):
        return "P"
    elif(3 in numbers):
        if(2 in numbers):
            return "F"
        return "K"
    elif(numbers.count(2) == 2):
        return "T"
    return "O"


def testPoker(Ri):
    """
    Realiza una prueba de poker en una secuencia de números Ri.

    Args:
        Ri (list): Una secuencia de números.

    Returns:
        tuple: Una tupla que contiene un valor booleano que indica si la prueba pasa, 
               seguido de una serie de resultados de la prueba.
    """
    classification = [classifyNumberPoker(i) for i in Ri]
    classificationCount = {"D":0,"O":0,"T":0,"K":0,"F":0,"P":0,"Q":0}
    for i in classification:
        classificationCount[i] += 1

    classificationProb = {"D":0.3024,"O":0.5040,"T":0.1080,"K":0.0720,"F":0.0090,"P":0.0045,"Q":0.0001}
    Ei = {key : truncate(value*len(Ri)) for key, value in classificationProb.items()}
    aux = {key : truncate(np.square(Ei[key] - value)/Ei[key] ) for key, value in classificationCount.items()}

    sigma = sum(aux.values())
    xsquare = chi2.isf(0.05, 6)
    if sigma < xsquare:
        return True, len(Ri), classificationCount.keys(), classificationCount.values(), classificationProb.values(), Ei.values(), aux.values(), sigma, xsquare
    return False, len(Ri), classificationCount.keys(), classificationCount.values(), classificationProb.values(), Ei.values(), aux.values(), sigma, xsquare

def testNumbers(Ri, nIntervals):
  """
  Comprueba varias pruebas estadísticas para una secuencia de números pseudoaleatorios Ri.

  Args:
  - Ri (list): Secuencia de números pseudoaleatorios a probar.
  - nIntervals (int): Número de intervalos para la prueba de Chi-cuadrado.

  Returns:
  - bool: True si todas las pruebas son exitosas, False si alguna falla.
  """
  
  return meanTest(Ri)[0] and varianceTest(Ri)[0] and testChi2Uniformity(Ri, nIntervals)[0] and testKS(Ri, nIntervals)[0] and testPoker(Ri)[0]

def getRepetitions(ri):
  """
  Obtiene una lista de repeticiones consecutivas en una secuencia de números.

  Args:
  - ri (list): Secuencia de números a analizar.

  Returns:
  - list: Lista de repeticiones consecutivas.
  """
  first = ri[0]
  result = [first]
  for i in range(1, len(ri)):
    if(first == ri[i]):
      break
    if(ri[i] == 0.0 or ri[i] == 1.0):
      continue
    if("-" in str(ri[i])):
      continue
    result.append(truncate(ri[i]))
  return result

def sinRepetidos(ri):
  """
  Elimina los elementos duplicados de una lista.

  Args:
  - ri (list): Lista con elementos duplicados.

  Returns:
  - list: Lista sin elementos duplicados.
  """
  lista_sin_repetidos = []
  for elemento in ri:
    if elemento not in lista_sin_repetidos:
        lista_sin_repetidos.append(elemento)
  return lista_sin_repetidos

def generateNumbersTested(Xo, k, c, g, min, max, quantity, nIntervals):
  """
  Genera una cantidad específica de números pseudoaleatorios y los prueba.

  Args:
  - Xo (int): Semilla inicial.
  - k (int): Multiplicador.
  - c (int): Incremento.
  - g (int): Número de bits para la máscara de bits.
  - min (int): Valor mínimo generado.
  - max (int): Valor máximo generado.
  - quantity (int): Cantidad de números a generar y probar.
  - nIntervals (int): Número de intervalos para la prueba de Chi-cuadrado.

  Returns:
  - tuple: Tupla con tres listas: números pseudoaleatorios (Ri), valores generados (Xi), y frecuencias de ocurrencia (Ni).
  """
  
  ri_result = []
  xi_result = []
  ni_result = []
  while(len(ri_result) <= quantity):
    data = generateNumbersByLinearCongruential(Xo, k, c, g, min, max, 50)
    ri = data[0]
    xi = data[1]
    ni = data[2]
    ri = getRepetitions(ri)

    if(len(ri) == 1):
      continue
    if testNumbers(ri, nIntervals):
      for num in ri:
        ri_result.append(num)
      for num in xi:
        xi_result.append(num)
      for num in ni:
        ni_result.append(num)
    
    m = np.power(2, g)
    Xo = Xo + 50
    if m <= Xo:
      while( m <= Xo):
        g = g + 1
        m = np.power(2, g)
  
  return ri_result[0:quantity], xi_result, ni_result

#Frog Problem

def simulateJumps1D(nJumps):
  """
  Simula el salto de una rana en una dimensión.

  Args:
  - nJumps (int): Número de saltos a simular.

  Returns:
  - list: Lista con la posición de la rana después de cada salto.
  """
  ri = generateNumbersTested(1,3,6,7,3,5, nJumps, 10)[0]
  jumps = [ -1 if num < 0.5 else 1 for num in ri]
  sum = 0
  result = [sum]
  for num in jumps:
    sum += num
    result.append(sum)
  return result
