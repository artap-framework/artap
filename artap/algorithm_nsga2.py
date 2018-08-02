# TODO: delete file
from .problem import Problem
from .population import Population
from .algorithm import Algorithm
import random
import pylab as plt

#
def Rosenbrock(x_list):
    # -30 <= xi <= 30
    # global minimal is at [1,1,..] where value = 0
    x1 = 0.0
    for i in range(0,len(x_list)-1):
        x1 = x1 + 100*(x_list[i]*x_list[i]-x_list[i+1])*(x_list[i]*x_list[i]-x_list[i+1]) +\
             (1-x_list[i])*(1-x_list[i])
    return [x1]
    
def Binh_and_Korn(x_list):
    # 0 <= x <=5, 0 <= y <= 3
    x = x_list[0]
    y = x_list[1]
    f1 = 4*pow(x,2) + 4*pow(y,2)
    f2 = pow(x-5,2)+pow(y-5,2)
    target = [f1,f2]
    return target


def Binh_and_Korn_constraints(x_list):
    # 0 <= x <=5, 0 <= y <= 3
    x = x_list[0]
    y = x_list[1]
    g1 = max(0, 25 - pow(x-5,2) - pow(y,2))
    g2 = max(0, pow(x-8,2)+pow(y+3,2) - 7.7)
    violation = [g1,g2]
    return violation

class NSGA2Individual(object):
    def __init__(self, temp):
        self.parameter = temp[:]
        self.target = get_target(self.parameter)
        self.violation = get_violation(self.parameter)
        self.front_rank = 0
        self.domination_counter = 0
        self.crowding_distance = 0
        self.set = set()

    def show(self):
        print(self.parameter, self.target)

def get_target(parameter):
    #return Rosenbrock(parameter)
    return Binh_and_Korn(parameter)


def get_violation(parameter):
    #return [0]
    return Binh_and_Korn_constraints(parameter)

class NSGA2(Algorithm):

    def __init__(self, problem :Problem, name = "NSGA2 Algorithm"):
        self.p_size = 300 # population size
        self.parameter_num = 2 # dimension of parameters to be optimized
        self.target_num = 2 # dimension of target function
        self.parameter_lower_bound = [ 0, 0 ]
        self.parameter_upper_bound = [ 5, 3 ]

        self.iteration = 10
        
        self.prob_cross = 0.6
        self.prob_mutation = 0.05

    def run(self):
        parents = self.initial_population()
        children = set()

        for it in range(1, self.iteration+1):
        
            all_population = parents | children
            self.fast_non_dominated_sort(all_population)
            self.calculate_crowd_dis(all_population)
        
            parents = set()
            front = 1
            while len(parents) < self.p_size:
                for ind in all_population:
                    if ind.front_rank == front:
                        parents.add(ind)
                        if len(parents) == self.p_size:
                            break
                front = front + 1

            #draw the scatter diagram of population
            X,Y,C = [],[],[] 
            for p in parents:
                if True: #p.front_rank == 1 :
                    X.append(p.target[0])
                    Y.append(p.target[1])
                    C.append(p.front_rank)
            plt.figure(figsize=[20, 16])
            plt.scatter(X,Y, s=10, c=C)
            plt.xlim(0,200), plt.xticks([])
            plt.ylim(0,80), plt.yticks([])
            plt.savefig('scatter_'+str(it)+'.png',dpi=48)

            # calculate the indicator of population
            best = [float('inf') for i in range(0, self.target_num)]
            mean = [0 for i in range(0, self.target_num)]
            for p in parents:
                for i in range(0, self.target_num):
                    if p.target[i] < best[i]:
                        best[i] = p.target[i]
                    mean[i] = mean[i] + p.target[i]
            for i in range(0, self.target_num):
                mean[i] = mean[i] / self.p_size
            
            print('the',it,'th generation')
            print('best_target:',best,' mean_target:',mean)

            children = self.generate(parents)   

    def initial_population(self):
        population = []
        for i in range(0, self.p_size):
            temp = []
            for j in range(0, self.parameter_num):
                lb = self.parameter_lower_bound[j]
                ub = self.parameter_upper_bound[j]
                temp.append(random.uniform(lb,ub))
            ind = NSGA2Individual(temp)
            population.append(ind)
        return set(population) 


    def is_dominate(self, p, q):
        dominate = False
        
        for i in range(0,len(p.target)):
            if p.target[i] > q.target[i] :
                return False
            if p.target[i] < q.target[i] :
                dominate = True
                
        for i in range(0,len(p.violation)):
            if p.violation[i] > q.violation[i] :
                return False
            if p.violation[i] < q.violation[i] :
                dominate = True
                
        return dominate


    def fast_non_dominated_sort(self, population):
        f_set = set()
        rank = 1
        for p in population:
            for q in population:
                if p is q :
                    continue
                if self.is_dominate(p,q):
                    p.set.add(q)
                elif self.is_dominate(q,p):
                    p.domination_counter = p.domination_counter + 1
            if p.domination_counter == 0 :
                p.front_rank = rank
                f_set.add(p)

        while not len(f_set)==0 :
            rank = rank + 1
            temp_set = set()
            for p in f_set :
                for q in p.set :
                    q.domination_counter = q.domination_counter - 1
                    if q.domination_counter==0 and q.front_rank==0 :
                        q.front_rank = rank
                        temp_set.add(q)
            f_set = temp_set


    def calculate_crowd_dis(self, population):
        infinite = 100000.0 # a large number as infinte
        
        for dim in range(0, self.parameter_num):
            new_list = self.sort_by_coordinate(population,dim)
            
            new_list[0].crowding_distance += infinite
            new_list[-1].crowding_distance += infinite
            max_distance = new_list[0].parameter[dim] - new_list[-1].parameter[dim]
            for i in range(1,len(new_list)-1):
                distance = new_list[i-1].parameter[dim] - new_list[i+1].parameter[dim]
                if max_distance == 0 :
                    new_list[i].crowding_distance = 0
                else :
                    new_list[i].crowding_distance += distance/max_distance
                
        for p in population :
            p.crowding_distance = p.crowding_distance / self.parameter_num


    def sort_by_coordinate(self, population, dim): # selection sort, which can be replaced with quick sort
        p_list = []
        for p in population:
            p_list.append(p)

        for i in range(0,len(p_list)-1):
            for j in range(i+1,len(p_list)):
                if p_list[i].parameter[dim] < p_list[j].parameter[dim]:
                    temp = p_list[i]
                    p_list[i] = p_list[j]
                    p_list[j] = temp
                    
        return p_list


    def tournment_select(self, parents, part_num=2): # binary tournment selection
        
        participants = random.sample(parents, part_num)
        best = participants[0]
        best_rank = participants[0].front_rank
        best_crowding_distance = participants[0].crowding_distance
        
        for p in participants[1:] :
            if p.front_rank < best_rank or \
            (p.front_rank == best_rank and p.crowding_distance > best_crowding_distance):
                best = p
                best_rank = p.front_rank
                best_crowding_distance = p.crowding_distance
                
        return best


    def generate(self, parents):
        # generate two children from two parents
        
        children = set()
        while len(children) < self.p_size:
            parent1 = self.tournment_select(parents)
            parent2 = self.tournment_select(parents)
            while parent1 == parent2 :
                parent2 = self.tournment_select(parents)
                
            child1,child2 = self.cross(parent1, parent2)
            child1 = self.mutation(child1)
            child2 = self.mutation(child2)

            children.add(child1)
            children.add(child2)
        return children


    def cross(self, p1, p2): # the random linear operator
        if random.uniform(0,1) >= self.prob_cross:
            return p1,p2
        
        parameter1,parameter2 = [],[]
        linear_range = 2
        alpha = random.uniform(0,linear_range)
        for j in range(0,len(p1.parameter)):
            parameter1.append(alpha*p1.parameter[j] +
                            (1-alpha)*p2.parameter[j] )
            parameter2.append((1-alpha)*p1.parameter[j] +
                            alpha*p2.parameter[j] )
        c1 = Individual(parameter1)
        c2 = Individual(parameter2)
        return c1,c2


    def mutation(self, p): # uniform random mutation
        mutation_space = 0.1
        parameter = []
        for i in range(0,len(p.parameter)):
            if random.uniform(0,1) < self.prob_mutation:
                para_range = mutation_space*(self.parameter_upper_bound[i]-self.parameter_lower_bound[i])
                mutation = random.uniform(-para_range,para_range)
                parameter.append(p.parameter[i]+mutation)
            else :
                parameter.append(p.parameter[i])

        p_new = NSGA2Individual(parameter)            
        return p_new
