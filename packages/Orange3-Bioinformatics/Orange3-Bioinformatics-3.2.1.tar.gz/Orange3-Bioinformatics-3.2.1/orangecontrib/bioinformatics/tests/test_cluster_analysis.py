import unittest
import os

from tempfile import mkstemp
from orangecontrib.bioinformatics.cluster_analysis import Cluster


class TestCluster(unittest.TestCase):
    gene_names = ['HBA1', 'HBA2', 'LTB', 'TMSB4X', 'HBB']
    gene_ids = [3039, 3040, 4050, 7114, 3040]

    def test_file_name(self):
        pass



if __name__ == '__main__':
    unittest.main()
