import itertools
from operators import ParetoDominance, EpsilonDominance


class Archive(object):
    """ Base archiving class based on platypus. An archive only containing non-dominated solutions.
        This base class realize the non-dominated sorting archive.
    """

    def __init__(self, dominance=ParetoDominance):
        super(Archive, self).__init__()
        self._dominance = dominance  # dominance comparator
        self._contents = []

    def add(self, individual):
        """
        
        :param individual: 
        :return: 
        """
        flags = [self._dominance.compare(individual, s) for s in self._contents]
        dominates = [x > 0 for x in flags]
        nondominated = [x == 0 for x in flags]

        if any(dominates):
            return False
        else:
            self._contents = list(itertools.compress(self._contents, nondominated)) + [individual]
            return True

    def append(self, solution):
        self.add(solution)

    def extend(self, solutions):
        for solution in solutions:
            self.append(solution)

    def remove(self, solution):
        try:
            self._contents.remove(solution)
            return True
        except ValueError:
            return False

    def size(self) -> int:
        return len(self._contents)

    def __len__(self):
        return len(self._contents)

    def __getitem__(self, key):
        return self._contents[key]

    def __iadd__(self, other):
        if hasattr(other, "__iter__"):
            for o in other:
                self.add(o)
        else:
            self.add(other)

        return self

    def __iter__(self):
        return iter(self._contents)


class EpsilonBoxArchive(Archive):

    def __init__(self, epsilons):
        super(EpsilonBoxArchive, self).__init__(EpsilonDominance(epsilons))
        self.improvements = 0

    def add(self, solution):
        flags = [self._dominance.compare(solution, s) for s in self._contents]
        dominates = [x == 1 for x in flags]
        nondominated = [x == 0 for x in flags]
        dominated = [x == 2 for x in flags]
        not_same_box = [not self._dominance.same_box(solution, s) for s in self._contents]

        if any(dominates):
            return False
        else:
            self._contents = list(itertools.compress(self._contents, nondominated)) + [solution]

            if dominated and not_same_box:
                self.improvements += 1
