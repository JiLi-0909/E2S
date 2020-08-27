#!/bin/env dls-python
"fast non-dominated sorting genetic algorithm II"

import random, sys

# colour display codes
ansi_red = "\x1B[31m"
ansi_normal = "\x1B[0m"

# cache of solutions
memo = {}

class solution(tuple):
    pass

def make_solution(x, y):
    p = solution(y)
    p.x = x
    return p

def dom(a, b):
    "a weakly dominates b"
    # An individule which is the same in all respects
    # does not dominate the other individule
    if all([a0 == b0 for (a0, b0) in zip(a, b)]):
        return False
    # but if any respect is better then the other
    # individule is dominated
    d = True
    for (a0, b0) in zip(a, b):
        d = (a0 <= b0) and d
    return d

def test_front(fs):
    "check that no member of the non-dominated front dominates another"
    for p0 in fs:
        for p1 in fs:
            if dom(p0, p1):
                print("front violation!", p0, p1)
                sys.exit(1)

def find_nondominated_front(P):
    # front is empty
    front = []
    for p0 in P:
        # add p0 to front temporarily
        front.append(p0)
        for p1 in P:
            if dom(p1, p0):
                # it's dominated, take it off the front
                front.pop()
                # p0 has been rejected, no need to keep looking
                break
    # check here
    # test_front(front)
    return front

def fast_non_dominated_sort(P):
    Fs = []
    P = set(P)
    i = 0
    while len(P) > 0:
        F = find_nondominated_front(list(P))
        P = P - set(F)
        # assign non-dominated rank
        for f in F:
            f.rank = i
        Fs.append(F)
        i += 1
    return Fs

def crowding_distance_assignment(front):
    l = len(front)
    for f in front:
        f.distance = 0
    # sort by each objective in turn
    for m in range(len(front[0])):
        s = sorted(front, key = lambda x: x[m])
        s[0].distance = float('inf')
        s[-1].distance = float('inf')
        for i in range(1, l-1):
            s[i].distance = s[i].distance + s[i + 1][m] - s[i - 1][m]

def crowded_comparison_key(x):
    # prefer low rank, then large distance (less crowded)
    return (x.rank, -x.distance)

def binary_tournament_selection(pop):
    # already sorted by fitness
    idx = range(len(pop))
    p1 = random.choice(idx)
    p2 = random.choice(idx)
    return pop[min(p1, p2)]

def selection(pop):
    return [binary_tournament_selection(pop) for n in range(len(pop))]

def polynomial_mutation(p):
    pmut_real = options["pmut_real"]
    eta_m = options["eta_m"]
    min_realvar = options["min_realvar"]
    max_realvar = options["max_realvar"]
    N = len(p)
    q = p[:]
    for n in range(N):
        if random.random() > pmut_real:
            continue
        y = p[n]
        yl = min_realvar[n]
        yu = max_realvar[n]
        delta1 = (y-yl)/(yu-yl)
        delta2 = (yu-y)/(yu-yl)
        rnd = random.random()
        mut_pow = 1.0/(eta_m+1.0)
        if rnd <= 0.5:
            xy = 1.0-delta1
            val = 2.0*rnd+(1.0-2.0*rnd)*(pow(xy,(eta_m+1.0)))
            deltaq = pow(val,mut_pow) - 1.0
        else:
            xy = 1.0-delta2
            val = 2.0*(1.0-rnd)+2.0*(rnd-0.5)*(pow(xy,(eta_m+1.0)))
            deltaq = 1.0 - (pow(val,mut_pow))
        y = y + deltaq*(yu-yl)
        if y<yl:
            y = yl
        if y>yu:
            y = yu
        q[n] = y
    return q

def crossover(pop):
    Q = []
    for n in range(len(pop)/2):
        (c1, c2) = sbx20(pop[n], pop[n+1])
        Q.append(c1)
        Q.append(c2)
    return Q

def sbx20(p1, p2):
    pcross_real = options["pcross_real"]
    eta_c = options["eta_c"]
    min_realvar = options["min_realvar"]
    max_realvar = options["max_realvar"]
    # copy parents
    child1 = p1[:]
    child2 = p2[:]
    # crossover?
    if random.random() > pcross_real:
        return (child1, child2)
    # floating point epsilon
    EPS = 2 ** -52
    # number of variables
    N = len(child1)
    for n in range(N):
        # 50% chance of crossing this variable
        if random.random() > 0.5:
            continue
        # identical to machine precision, no crossover
        if abs(p1[n] - p2[n]) < EPS:
            continue
        y1 = min(p1[n], p2[n])
        y2 = max(p1[n], p2[n])
        yl = min_realvar[n]
        yu = max_realvar[n]
        rand = random.random()
        beta = 1.0 + (2.0*(y1-yl)/(y2-y1))
        alpha = 2.0 - pow(beta,-(eta_c+1.0))
        if rand <= 1.0/alpha:
            betaq = pow ((rand*alpha),(1.0/(eta_c+1.0)))
        else:
            betaq = pow ((1.0/(2.0 - rand*alpha)),(1.0/(eta_c+1.0)))
        c1 = 0.5*((y1+y2)-betaq*(y2-y1))
        beta = 1.0 + (2.0*(yu-y2)/(y2-y1))
        alpha = 2.0 - pow(beta,-(eta_c+1.0))
        if rand <= 1.0/alpha:
            betaq = pow ((rand*alpha),(1.0/(eta_c+1.0)))
        else:
            betaq = pow ((1.0/(2.0 - rand*alpha)),(1.0/(eta_c+1.0)))
        c2 = 0.5*((y1+y2)+betaq*(y2-y1))
        # bounds
        if c1<yl:
            c1=yl
        if c2<yl:
            c2=yl
        if c1>yu:
            c1=yu
        if c2>yu:
            c2=yu
        if random.random() > 0.5:
            child1[n] = c2
            child2[n] = c1
        else:
            child1[n] = c1
            child2[n] = c2
    return (child1, child2)

def mutation(pop):
    return [polynomial_mutation(p) for p in pop]

def memo_lookup(pop):
    done = []
    todo = []
    for p in pop:
        p = tuple(p)
        if p in memo:
            done.append((make_solution(p, memo[p])))
        else:
            todo.append(p)
    return (done, todo)

def evaluate(pop):



    "evaluate population"
    print('File nsga.py, fct evaluate(pop)')
    print(' the input population is:')
    for k in pop:
        print k

    # now add memoization
    result = []

    # get any cached results
    # (randomly some members don't get mutated or crossed over)
    #(already_done, todo) = memo_lookup(pop)

    # calculate new points
    ys = options['evaluate'](pop)
    

    # store results in cache
    for (x, y) in zip(pop, ys):
      #  memo[x] = y
        result.append(make_solution(x, y))

    #result = result + already_done
    print('#############################################')
    print(' File nsga.py:')
    print(' le resultat de evaluate(pop) dans est:')
    for k in result:
        print(k)
    print('#############################################')

    return result

################################################################################################








######################################################################################################################
##############################                                                    ####################################
##############################                                                    ####################################
##############################                                                    ####################################
######################################################################################################################


def make_new_pop(pop):

    # only need inputs at this stage
    # (we are already sorted by fitness)
    print('*********************************************')
    print('File nsga.py - old pop:')
    print(len(pop))
    print(pop)
    pop = [list(p.x) for p in pop]

    pop = selection(pop)
    pop = crossover(pop)
    pop = mutation(pop)
    print('File nsga.py - new pop:')
    print(len(pop))
    print(pop)
    print('*********************************************')
    # now evaluate the new populuation members
    pop = evaluate(pop)

    return pop


######################################################################################################################
##############################                                                    ####################################
##############################                                                    ####################################
##############################                                                    ####################################
######################################################################################################################


def random_population():
    "produce a random population within bounds"
    S = options["population_size"]
    min_realvar = options["min_realvar"]
    max_realvar = options["max_realvar"]
    N = len(min_realvar)
    X0 = []
    for s in range(S):
        x = [0] * N
        for n in range(N):
            lb = min_realvar[n]
            ub = max_realvar[n]
            x[n] = lb + (random.random()) * (ub - lb)
        X0.append(x)
    print('la population X0 est :')
    print(X0)
    return X0


######################################################################################################################
##############################                                                    ####################################
##############################                                                    ####################################
##############################                                                    ####################################
######################################################################################################################


def set_population_from_individules(pop):
    individules = options["individules"]
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    print('individuleS (pluriel!!) vaut : ', individules)
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    for i, individule in enumerate(individules):  # FBT : enumerate en python permet de recuperer a la fois l'index (dans la variable "i") et l'entree correspndante a cet index dans "individule" sans "s")
        pop[i] = individule
        print(' i vaut :  ', i)
        print(' et pop[i] vaut :',pop[i])
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    return pop


######################################################################################################################
##############################                                                    ####################################
##############################                                                    ####################################
##############################                                                    ####################################
######################################################################################################################


def load_input(filename):
    options = {}
    # load variables in file into options structure
    execfile(filename, options)
    # some checks (better find out about missing parameters now than later)
    schema = (("pmut_real", "float"),
              ("pcross_real", "float"),
              ("eta_m", "float"),
              ("eta_c", "float"),
              ("evaluate", "function"),
              ("min_realvar", "array"),
              ("max_realvar", "array"),
              ("population_size", "int"),
              ("generations", "int"),
              ("individules", "array"),
              ("seed", "int"),
              )

    fail = False
    print "NSGA-II"
    print "======="
    for (name, check) in schema:
        if not name in options:
            print "%sERROR: input '%s' is missing%s" % (ansi_red, name, ansi_normal)
            fail = True
        else:
            print "%s: %s" % (name, options[name])

    l1 = len(options["min_realvar"])
    l2 = len(options["max_realvar"])

    if l1 != l2:
        print "%sERROR: min_realvar is not the same length as max_realvar\n" \
              "(should be number of INPUT variables)%s" % (ansi_red, ansi_normal)
        fail = True

    for (ml, mu) in zip(options["min_realvar"], options["max_realvar"]):
        if ml > mu:
            print "%sERROR: Maximum value must be greater than minimum value, but " \
                  "specified value is (%f < %f)%s" % (ansi_red, ml, mu, ansi_normal)

    for i in options["individules"]:
        if len(i) != l1:
            print "%sERROR: an individule must have the same length as" \
                  " the number of paramters%s" % (ansi_red, ansi_normal)
            fail = True
        for (ml, mu, ii) in zip(options["min_realvar"], options["max_realvar"], i):
            if not ml <= ii <= mu:
                print "%sERROR: Individual out of range with paramter value %f%s" \
                        % (ansi_red, ii, ansi_normal)
                fail=True

    if len(options["individules"]) > options["population_size"]:
        print "%sERROR: more individules specified than population %s" % (ansi_red, ansi_normal)
        fail = True

    if fail:
        sys.exit(1)
    print('--------------------------------|||||||||||||||||||||||||||||||||||||||||||||----------------------------------------------------')
    print('les options viennent ici, avant le calcul des generations')
    print('----------------------------------||||||||||||||||||||||||||||||||||||||||||||||----------------------------------------------------')
    return options



######################################################################################################################
##############################                                                    ####################################
##############################                                                    ####################################
##############################                                                    ####################################
######################################################################################################################



def dump_fronts(fronts, generation):

    INDEX_FORMAT_CODE = '%06d'
    f = file('fronts.' + INDEX_FORMAT_CODE  % generation, "w")
    f.write("fronts = (\n")
    for i, front in enumerate(fronts):
        f.write("( # Front %d\n" % i)
        for ff in front:
            f.write("    (%s, %s),\n" % (tuple(ff.x[:]), ff[:]))
        f.write("),\n")
    f.write(")\n")
    f.close()




#def dump_fronts(fronts, generation):
#
#    f = file("fronts.%d" % generation, "w")
#    f.write("fronts = (\n")
#    for i, front in enumerate(fronts):
#        f.write("( # Front %d\n" % i)
#        for ff in front:
#            f.write("    (%s, %s),\n" % (ff.x[:], ff[:]))
#        f.write("),\n")
#    f.write(")\n")
#    f.close()


######################################################################################################################
##############################                                                    ####################################
##############################                                                    ####################################
##############################                                                    ####################################
######################################################################################################################


def nsga2():

    "Non-dominated sorting genetic algorithm II main loop"
    
    if not sys.argv[1:]:
        print 'Usage: ' + sys.argv[0] + ' <nsga_input_file.py>'
        print
        print 'Non-dominated Sorting Genetic Algorithm II'
        sys.exit(1)

    # load problem #FBT: ie load the problem-file to solve
    global options
    options = load_input(sys.argv[1])

    # seed the random number generator to ensure repeatble results
    random.seed(options['seed'])

    # initialize population
    X0 = random_population()
    X0 = set_population_from_individules(X0)
    P = evaluate(X0)
    print('*************************************')
    print('File nsga.py, line: P = evaluate(X0)')
    print('length of P after evaluate(X0):')
    print(len(P))
    print('*************************************')
    Q = []

    # for each generation
    for t in range(options["generations"]):

        # combine parent and child populations
        R = P + Q

        print('*************************************')
        print('File nsga.py:')
        print('length of R after: R = P + Q')
        print(len(R))
        print('*************************************')

        # remove duplicates
        R = list(set(R))
        print('FBT: R = list(set(R)         :', len(R))

        # find all non-dominated fronts
        fronts = fast_non_dominated_sort(R)

        # calculate the density of solutions around each point
        for f in fronts:
            crowding_distance_assignment(f)

        # sort first by rank (which front) then by sparsity
        R.sort(key = crowded_comparison_key)
        print('FBT: R.sort(key = crowded_comparison_key) ', len(R))

        # take the best solutions that fit in our population size
        P = R[:options["population_size"]]
        print('FBT:  P = R[:options["population_size"]] ', len(P))

        print('*************************************')
        print('File nsga.py, line 466:')
        print('length of P before make_new_pop(P) is:')
        print(len(P))
        print('*************************************')
        # tournament, crossover, mutation
        Q = make_new_pop(P)

        # print out all solutions by front
        dump_fronts(fronts, t)

        print "generation %d" % t

    print "DONE"


######################################################################################################################
##############################                                                    ####################################
##############################                                                    ####################################
##############################                                                    ####################################
######################################################################################################################


if __name__ == "__main__":
    nsga2()

