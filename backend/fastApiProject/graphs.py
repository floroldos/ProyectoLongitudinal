import re
import numpy as np
import matplotlib.pyplot as plt

file_path = 'ALGABO/longitudinal/backend/fastApiProject/log.txt'

with open(file_path, 'r') as file:
    data = file.read()

steps = [int(x) for x in re.findall(r'- (\d+)', data)]

mu = np.mean(steps)  # Media
sigma = np.std(steps)  # Desviación estándar

# Rango de valores para la gráfica
x = np.linspace(mu - 4*sigma, mu + 4*sigma, 1000)
y = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma)**2)

# Gráfica
plt.plot(x, y, label='Campana de Gauss')
plt.title('Distribución Normal de los Pasos del Cubo de Rubik')
plt.xlabel('Número de pasos')
plt.ylabel('Densidad de probabilidad')
plt.axvline(mu, color='red', linestyle='--', label=f'Media = {mu:.2f}')
plt.legend()
plt.grid(True)
plt.show()

print(f'La media de los pasos es: {mu:.2f}')
print(f'La desviación estándar de los pasos es: {sigma:.2f}')
