import json
import numpy as np
import requests
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from scipy.special import spherical_jn, spherical_yn
from scipy.constants import pi, c

# Класс для расчета ЭПР
class RCS_Calculator:
    def __init__(self, diameter, fmin, fmax):
        self.diameter = diameter
        print(diameter)
        self.fmin = fmin
        print(fmin)
        self.fmax = fmax
        print(fmax)

    def calculate_rcs(self, frequency):
        r = self.diameter / 2
        k = 2 * pi * frequency / c
        lmbd = c / frequency
        n_max = int(np.ceil(k * r)) + 10

        sigma = 0
        for n in range(1, n_max):
            kr = k * r
            jn = spherical_jn(n, kr)
            yn = spherical_yn(n, kr)
            hn = jn + 1j * yn

            jn_1 = spherical_jn(n-1, kr)
            yn_1 = spherical_yn(n-1, kr)
            hn_1 = jn_1 + 1j * yn_1

            an = jn / hn
            bn = (kr * jn_1 - n * jn) / (kr * hn_1 - n * hn)

            # Используем только вещественную часть
            sigma += ((-1)**n * (n + 0.5) * (bn.real - an.real))**2

        return (lmbd**2 / pi) * sigma

    def get_rcs_data(self):
        frequencies = np.linspace(self.fmin, self.fmax, 630)
        rcs_values = [self.calculate_rcs(f) for f in frequencies]
        return frequencies, rcs_values

# Загрузка и парсинг файла
def download_and_parse_file(url, variant_number):
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Ошибка загрузки файла: {response.status_code}")
    
    root = ET.fromstring(response.content)
    variant = root.find(f".//variant[@number='{variant_number}']")
    if variant is None:
        raise ValueError(f"Не удалось найти данные для варианта {variant_number}")
    
    diameter = float(variant.get('D'))
    fmin = float(variant.get('fmin'))
    fmax = float(variant.get('fmax'))
    
    return diameter, fmin, fmax


# Сохранение результатов в JSON
def save_results_to_json(filename, frequencies, rcs_values):
    data = {
        "freq": frequencies.tolist(),
        "lambda": (c / frequencies).tolist(),
        "rcs": rcs_values
    } 
    
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    
# Построение графика
def plot_rcs(frequencies, rcs_values):
    plt.plot(frequencies, rcs_values)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("RCS (m^2)")
    plt.title("RCS of a Perfectly Conducting Sphere")
    plt.grid(True)
    plt.show()

# Основная функция
def main():
    variant_number = 4
    url = "https://jenyay.net/uploads/Student/Modelling/task_rcs.xml"

    # Загрузка и парсинг файла
    diameter, fmin, fmax = download_and_parse_file(url, variant_number)

    # Расчет ЭПР
    rcs_calculator = RCS_Calculator(diameter, fmin, fmax)
    frequencies, rcs_values = rcs_calculator.get_rcs_data()

    # Сохранение результатов
    save_results_to_json("rcs_results.json", frequencies, rcs_values)

    # Построение графика
    plot_rcs(frequencies, rcs_values)
    

if __name__ == "__main__":
    main()
