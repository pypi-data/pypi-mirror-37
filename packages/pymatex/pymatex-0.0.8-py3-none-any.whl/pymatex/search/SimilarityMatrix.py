import csv


class SimilarityMatrix:

    def __init__(self, path=None):

        if path is None:
            path = 'SimilarityMatrix.txt'

        with open(path, 'r') as f:
            csvreader = csv.reader(f, delimiter=';')

            colnames = next(csvreader)[1:]
            self.colnames = [colname.strip() for colname in colnames]
            self.data = [None for _ in range(len(self.colnames) * len(self.colnames))]

            for i, row in enumerate(csvreader):
                row_name = row[0]
                assert row_name in self.colnames
                assert len(row) == len(self.colnames) + 1

                for j, value in enumerate(row[1:]):
                    int_value = int(value)
                    index = i * len(self.colnames) + j
                    self.data[index] = int_value

            assert i == len(self.colnames) - 1

            assert self.is_symmetric()

    def get_similarity_between(self, lhs_node, rhs_node):
        lhs_index = self.colnames.index(lhs_node)
        rhs_index = self.colnames.index(rhs_node)

        index = lhs_index * len(self.colnames) + rhs_index
        return self.data[index]

    def is_symmetric(self):
        for i in range(len(self.colnames)):
            for j in range(len(self.colnames)):
                index_1 = i * len(self.colnames) + j
                index_2 = j * len(self.colnames) + i
                if self.data[index_1] != self.data[index_2]:
                    print("No symmetric value for: {} and {}".format(self.colnames[i], self.colnames[j]))
                    return False
        return True
