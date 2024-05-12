from ntd1 import DataLoader
from ntd2 import RCS
from ntd3 import ResultWriter
from ntd4 import Plotter
import numpy as np


def main():
    url = "https://jenyay.net/uploads/Student/Modelling/task_rcs.xml"
    variant_number = 4
    
    loader = DataLoader(url)
    D, fmin, fmax = loader.parse_xml(variant_number)

    frequencies = np.linspace(fmin, fmax, num=1000)
    rcs_calculator = RCS(D / 2)
    results = []
    for freq in frequencies:
        rcs = rcs_calculator.calculate_rcs(freq)
        results.append({"freq": freq, "lambda": 3e8 / freq, "rcs": rcs})

    writer = ResultWriter("rcs_results.json")
    writer.write_to_json({"data": results})

    plotter = Plotter()
    plotter.plot_rcs_vs_frequency(results)

if __name__ == "__main__":
    main()
