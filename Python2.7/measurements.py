from time import time
import cProfile


from Python.naive import NaiveSearch
from Python.rabin_karp import RabinKarp
from Python.kmp import KnuthMorrisPratt
from Python.boyer_moore_horspool import BoyeerMooreHorspool
from Python.boyer_moore import BoyerMoore
from Pyopencl.naive.naive_pocl import NaiveSearchPOCL
from Pyopencl.kmp.kmp_pocl import KnuthMorrisPrattPOCL
from Pyopencl.bmh.bmh_pocl import BoyeerMooreHorspoolPOCL


class Measurements:
    """ Implement all needed Measurements and illustrate results """

    def __init__(self, text, in_dir, out_dir, pieces_number=10000, start=25, end=200, step=25, device_type=1):
        # initialize objects of basic algorithms
        self.naive = NaiveSearch(text)
        self.rk = RabinKarp(text)
        self.kmp = KnuthMorrisPratt(text)
        self.bmh = BoyeerMooreHorspool(text)
        self.bm = BoyerMoore(text)

        # initialize objects of PyopenCL versions
        self.naive_pocl = NaiveSearchPOCL(text, pieces_number=pieces_number, device_type=device_type)
        self.kmp_pocl = KnuthMorrisPrattPOCL(text, pieces_number=pieces_number, device_type=device_type)
        self.bmh_pocl = BoyeerMooreHorspoolPOCL(text, pieces_number=pieces_number, device_type=device_type)

        self.data_dir = in_dir
        self.res_dir = out_dir
        self.start = start
        self.end = end
        self.step = step

    def naive_measurements(self):
        print "Naive algorithm Measurements:"
        results = self._measure(self.naive)
        self._write_res_to("naive.txt", results)

    def rk_measurements(self):
        print("Rabin-Karp algorithm Measurements:")
        results = self._measure(self.rk)
        self._write_res_to("rk.txt", results)

    def kmp_measurements(self):
        print "Knuth-Morris-Pratt algorithm Measurements:"
        results = self._measure(self.kmp)
        self._write_res_to("kmp.txt", results)

    def bmh_measurements(self):
        print "Boyer-Moore-Horspool algorithm Measurements:"
        results = self._measure(self.bmh)
        self._write_res_to("bmh.txt", results)

    def bm_measurements(self):
        print "Boyer-Moore algorithm Measurements:"
        results = self._measure(self.bm)
        self._write_res_to("bm.txt", results)

    def naive_pocl_measurements(self):
        print "Naive POCL algorithm Measurements:"
        results = self._measure(self.naive_pocl)
        self._write_res_to("naive_pocl.txt", results)

    def kmp_pocl_measurements(self):
        print "Knuth-Morris-Pratt POCL algorithm Measurements:"
        results = self._measure(self.kmp_pocl)
        self._write_res_to("kmp_pocl.txt", results)

    def bmh_pocl_measurements(self):
        print "Boyer-Moore-Horspool POCL algorithm Measurements:"
        results = self._measure(self.bmh_pocl)
        self._write_res_to("bmh_pocl.txt", results)

    def run_all_basic(self):
        """ measurements for basic version """
        self.naive_measurements()
        self.kmp_measurements()
        self.bmh_measurements()
        # self.rk_measurements()
        # self.bm_measurements

    def run_all_pocl(self):
        """ measurements for PyOpenCL version """
        print "Naive PyopenCL algorithm Measurements:"
        self.naive_pocl_measurements()
        print "Knuth-Morris-Pratt PyopenCL algorithm Measurements:" 
        self.kmp_pocl_measurements()
        print "Boyer-Moore-Horspool PyopenCL algorithm Measurements:" 
        self.bmh_pocl_measurements()

    def _measure(self, obj):
        """ common method for measuring time """
        results = []
        for size in range(self.start, self.end+1, self.step):
            print "size: %d" % (size)
            patterns = self._read_patterns(size)
            interm_res = []
            for i in range(0, len(patterns)):
		start = time()
        	obj.all_matches(patterns[i])
            	end = time()
            interm_res.append(end-start)
            results.append(1.0*sum(interm_res)/len(interm_res))
        return results

    def _read_patterns(self, size):
        """ read patterns from file """
        file_name = self.data_dir + str(size) + ".txt"
        with open(file_name, 'r') as file:
            patterns = [pat.strip() for pat in file]
        return patterns

    def _write_res_to(self, out_file, results):
        """ write measurements to particular file """
        with open(self.res_dir + "/" + out_file, 'w+') as file:
            file.write("\t".join(str(size) for size in range(self.start, self.end+1, self.step)) + "\n")
            file.write("\t".join(str(res) for res in results) + "\n")


def read_data(file_name):
    """ read all data from file """
    with open(file_name, 'r') as file:
        data = file.read()
    return data


def main():
    genome = read_data("Measurements/data/processed.txt")
    measurements = Measurements(genome, "Measurements/data/25-200/", "Measurements/results/25-200",
                                pieces_number=1000, start=25, end=200, step=25, device_type=2)
    # measurements.run_all_basic()
    # measurements.naive_measurements()
    # measurements.kmp_measurements()
    # measurements.bmh_measurements()

    # measurements.naive_pocl_measurements()
    # measurements.kmp_pocl_measurements()
    # measurements.bmh_pocl_measurements()

    measurements2 = Measurements(genome, "Measurements/data/250-2000/", "Measurements/results/250-2000",
                                 pieces_number=1000, start=250, end=2000, step=250, device_type=2)
    # measurements2.run_all_basic()
    # measurements2.naive_measurements()
    # measurements2.kmp_measurements()
    # measurements2.bmh_measurements()

    measurements2.naive_pocl_measurements()
    measurements2.kmp_pocl_measurements()
    # measurements2.bmh_pocl_measurements()
    


if __name__ == "__main__":
    #cProfile.run('main()')
    main()
