# k = 10
# def f(a, b):
#     sum = 0
#     for i in range(k):
#         sum_result += g(a, k)

#     return (g(a,b)/sum_result)

# def g(a, b):
#     return (f(a,b) / 


# predators = [] # an array of all of the predators
# victims = [] # an array of all of the victims

# victim_id = -1 # the postition in the array of the current victim being accounted for
# pref_summation = 0 # running summation of preference scores  --  --  Total sum = 1

# def preference_score(predator, victim_id, time):
#     victim_id += 1

#     if(victim_id == len(victims)): # the last predator
#         return 1 - pref_summation

#     else:  
#         result = functional_response(predator, victim_id, time) / 


# def functional_response(predator, victim_id, time):

import networkx as nx
import numpy as np
import random
import species
from species import *


"""
Calls scoring calculation on all species pairs
"""
def fill_score_matrix():
    # print(len(species))
    for iterator1 in range(0, len(species)): # iterators refer to species names
        for iterator2 in range(0, len(species)): 
            # print('iterator1 is: ', iterator1)
            # print('iterator2 is: ', iterator2)
            score = calculate_inter_species_score(species[iterator1], species[iterator2])
            score_matrix[iterator1, iterator2] = score
    score_matrix[0].fill(0)
    score_matrix[0,0] = 1.0


"""
Caclulates S_ij scores gives two species i & j
"""
def calculate_inter_species_score(i, j): 
    # print("i index is: ", i.get_index())
    # print("j index is: ", j.get_index())
    # print("i attributes are: ", i.get_attributes())
    # print("j attributes are: ", j.get_attributes())
    score = 0
    for iterator1 in range(attribute_count): 
        for iterator2 in range(attribute_count):
            attrib1 = i.get_attributes()[iterator1] # attrib from species i
            attrib2 = j.get_attributes()[iterator2] # attrib from species j
            score += attribute_pair_score[attrib1, attrib2] # running sum
    
    score = (1/attribute_count) * score
    # print(score, '\n')
    return max(0, score) # >= 0 ensures that i preys on j


"""
Calls function response calculation for all species pairs
"""
def fill_func_response_matrix():
    # print(calculate_functional_response(species[1], species[0]))
    for iterator1 in range(0, len(species)):
        for iterator2 in range(0, len(species)):
            functional_response_matrix[iterator1, iterator2] = calculate_functional_response(
                species[iterator1], species[iterator2]) # functional response matrix filled


"""
Calculates functional reponses
"""
def calculate_functional_response(i, j):
    i_index = i.get_index() # species i index
    j_index = j.get_index() # species j index

    # Numerator calculation
    spec_score = score_matrix[i_index, j_index] # S_ij
    pref_score = preference_matrix[i_index, j_index] # f_ij
    prey_pop = j.get_current_pop() # N_j
    numer = spec_score + pref_score + prey_pop

    # Denominator calculation
    competing_predators = list(Graph.successors(j)) # successor, returns children nodes of given node
    alpha_sum = 0 # competition alpha running sum
    score_sum = 0 # S_kj running sum
    preference_sum = 0 # f_kj running sum
    competitor_pop_sum = 0 # N_k running sum
    for competitor in competing_predators: # summing competition dynamics term
        alpha_sum += caclulate_competition_alpha(competitor, i) # alpha_ki
        score_sum += score_matrix[competitor.get_index(), j.get_index()] # S_kj
        preference_sum += preference_matrix[competitor.get_index(), j.get_index()] # f_kj
        competitor_pop_sum += competitor.get_current_pop() # N_k
    comp_dynamics = alpha_sum + score_sum + preference_sum + competitor_pop_sum
    denom = ecological_efficiency * j.get_current_pop() + comp_dynamics # b*N_j + comp_dynamics

    # print(j.get_current_pop())
    # print("numerator: ", numer)
    # print("denominator: ", denom)

    if (denom == 0):
        return 0
    else:
        return numer / denom


"""
Competition alpha
"""
def caclulate_competition_alpha(i, k):
    overlap = len(set(i.get_attributes()) & set(k.get_attributes())) # q_ki term
    # print("species attributes: ", i.get_attributes())
    # print("competitor attributes: ", k.get_attributes())
    # print("overlap: ", overlap)
    return competition_param + (1 - competition_param) * overlap # alpha_ki = c + (1 - c) * q_ki
 

"""
Population dynamics
"""
def calculate_population(i):
    for spec in species:
        pass


"""
Simulation parameter values
"""
total_resources = 10**4 # 10^4 resources
competition_param = .5 # c
ecological_efficiency = .1 # lambda
functional_response_saturation = .005 # b
time_steps = 10 # number of time steps


"""
Attributes matrix creation
"""
total_attribute_count = 500 # 500 total attributes
attribute_count = 10 # 10 attributes for each species
all_attributes = np.arange(500) # filling attribute list with just ints from 1-500
attribute_pair_score = np.full((total_attribute_count, total_attribute_count), 0.0) # initializing matrix of cross attribute scores
for iterator1 in range(total_attribute_count):
    for iterator2 in range(total_attribute_count):
        attribute_pair_score[iterator1, iterator2] = random.uniform(-1.0, 1.0) # random m_alpha,beta score -1 < m < 1


"""
Environment and Species 1 initialization
"""
max_species_index = 2
s0 = Species('s0', 0, total_resources, 0, total_resources, 0)
s1 = Species('s1', 1, 0, 0, 0, .2)
species = [s0, s1] #list of all species.
species_indexer = 1
# species_dict = {'s0' : s0, 's1': s1}


"""
Graph creation
"""
Graph = nx.DiGraph() # creating graph
Graph.add_node(s0) # adding environment species
Graph.add_node(s1) # first species
Graph.add_edge(s0, s1) # first edge from enviro -> first species


"""
 Inter Species score matrix, S_ij. Adding scores for first two species f
"""
score_matrix = np.full((200, 200), -1.0) # 200x200 array w/ values initialized to -1

# for iterator1 in range(2): #filling in environment and basal species calculations
#     for iterator2 in range(2):
#         score = calculate_inter_species_score(species[iterator1], species[iterator2])

# score = calculate_inter_species_score(species[iterator1], species[iterator2])
# score_matrix[iterator1, iterator2] = score
fill_score_matrix(); # filling scoring matrix S_ij


"""
Prey preference matrix, 'f_ij'
"""
preference_matrix = np.full((200,200), -1) # 200x200 array w/ values init to -1
preference_matrix[0,0] = 1 # environment 'feeds' off itself
preference_matrix[0,1] = 0 # environment doesn't feed off species 1
preference_matrix[1,0] = 1 # species 1 feeds entirely off environemnt
preference_matrix[1,1] = 0 # species 1 does not feed off itself


"""
Functional response matrix g_ij
"""
functional_response_matrix = np.full((200,200), -1.0) # 200x200 array w/ values init to -1
fill_func_response_matrix()


# print(" \n the functional responses are as follows:")
# print(functional_response_matrix[0])
# print(functional_response_matrix[1])

# print(preference_matrix)
# g_sum = 0
# for iterator1 in range(len(species)):
#     for predecessor in Graph.predecessors(species[iterator1]):
#         g_sum += functional_response_matrix[iterator1, predecessor.get_index()]

#     print("g sum is: ", g_sum)
#     for iterator2 in range(len(species)):
#         preference_matrix[iterator1, iterator2] = (functional_response_matrix[iterator1, iterator2] / g_sum)
# print(preference_matrix)

"""
Main simulation loop
"""
for t in range(time_steps): # iterating through each time step

    """
    Addition of new species
    """
    species_indexer += 1
    parent = species[random.randrange(1, len(species))] # selecting random parent species
    # child = parent.gen_child_species() # generating child species w/ single new attribute

    # child = copy.copy(parent) # copying original node
    child = Species('s' + str(species_indexer), species_indexer, 0, 0, 0, .2)
    new_attribs = parent.get_attributes() # editing attributes
    # print(new_attribs)
    new_attribs[random.randrange(10)] = random.randrange(500) # one random attribute set to new random attribute
    
    child.set_attributes(new_attribs)
    # child.set_name('s' + str(species_indexer)) # renaming child species
    # child.set_index(species_indexer)
    species.append(child) # adding new species
    species[species_indexer].set_attributes(species[species_indexer], new_attribs)
    for spec in species:
        print(spec.get_attributes())
    print('\n')
    # print(parent.get_attributes())
    # print(new_attribs)
    # print(child.get_attributes())
    # print(species[species_indexer].get_attributes(), '\n')
    # print(preference_matrix)
    # print(child.get_index())
    preference_matrix[child.get_index()] = preference_matrix[parent.get_index()] # child prefs originally equal to parent
    # print("new matrix now:")
    # print(preference_matrix)

    """
    Inserting species into graph
    """
    Graph.add_node(child) # adding node to graph
    for successor in Graph.successors(parent): # add edges between new species and its prey
        Graph.add_edge(child, successor) # child -> successor
    for predecessor in Graph.predecessors(parent):
        Graph.add_edge(predecessor, child) # predecessor -> child


    """
    Updating matrices in following order:
    1) score
    2) func. response
    3) preference
    """
    # print(score_matrix[1], '\n')
    # print('next matrix', '\n')
    fill_score_matrix()
    # print(score_matrix[1])
    fill_func_response_matrix()



# print(len(species))
# for spec in species:
#     print(spec.get_attributes())