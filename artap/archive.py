import itertools, operator
from .operators import ParetoDominance, EpsilonDominance
from random import choice, sample


class Archive(object):
    """ Base archiving class based on platypus. An archive only containing non-dominated solutions.
        This base class realize the non-dominated sorting archive.
    """

    def __init__(self, dominance=EpsilonDominance(epsilons=[0.1, 0.1])):
        super(Archive, self).__init__()
        self._dominance = dominance  # dominance comparator
        self._contents = []

    def add(self, individual):
        """
        Archive acceptance procedure is implemented here, this procedure accepts the individual if it is dominates some
        individual and at least non-dominatey by any other member of the list, however it not preserves the length of
        the _contents list.

        :param individual: the examined Individual object from the offsprings.
        :return: 
        """

        is_dominated = False
        is_contained = False

        if len(self._contents) == 0:
            self._contents.append(individual)
            return True
        else:
            number_of_deleted_solutions = 0

            # New copy of list and enumerate
            for index, current_solution in enumerate(list(self._contents)):
                is_dominated_flag = self._dominance.compare(individual.costs_signed, current_solution.costs_signed)
                if is_dominated_flag == 1:
                    del self._contents[index - number_of_deleted_solutions]
                    number_of_deleted_solutions += 1
                elif is_dominated_flag == 2:
                    is_dominated = True
                    break
                elif is_dominated_flag == 0:
                    if individual.costs_signed == current_solution.costs_signed:
                        is_contained = True
                        break

        if not is_dominated and not is_contained:
            self._contents.append(individual)
            return True

        return False

    def rand_choice(self):
        """
        Gives back a random element for the selector operator, here we don't need to
        compare the different levels.
        """
        return choice(self._contents)

    def rand_sample(self, nr=2):
        """Returns an nr long random list of the population """
        return sample(self._contents, nr)

    def truncate(self, size, getter, larger_preferred=True):
        """ Truncates the contents to the given value, which is usually the number of particles/individuals in a
            population. """

        result = sorted(self._contents, key=lambda x: x.features[getter])

        if larger_preferred:
            result.reverse()

        self._contents = result[:size]
        return

    def append(self, individual):
        self.add(individual)

    def extend(self, individuals):
        for individual in individuals:
            self.append(individual)

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
