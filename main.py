from new_Encoder_breakdown_rules import *
import pddlpy
from parseR.tools import parse_pddl
from collections import defaultdict
from z3 import *



def main():
	#Parse PDDL file and given horizon length:
	path_domain1 = './original_domain.pddl'
	path_instance = './prob4.pddl'
	h = 6 #Horizon


	task1 = parse_pddl(path_domain1,path_instance)
	domprob = pddlpy.DomainProblem(path_domain1,path_instance)

	#Construct formulae for given planning problem:
	F1_kb1 = goal_state(task1, h,)

	F2_kb1 = init_states(task1)

	F3_kb1 = Preconditons(task1,domprob, h)

	F4_kb1 = Add_Effects(task1, domprob, h)

	F5_kb1 = Frames_addeff(task1, domprob, h)

	F6_kb1 = Del_Effects(task1, domprob, h)

	F7_kb1 = Frames_deleff(task1, domprob, h)

	F8_kb1 =  exclusion_axioms(task1, h)


	F_1 = [F1_kb1, F2_kb1, F3_kb1, F4_kb1, F5_kb1, F6_kb1, F7_kb1, F8_kb1]
	F_1 = [item for sublist in F_1 for item in sublist]
	KB = list(set(F_1))
	
	with open('KB.txt', 'w') as the_file:
		for k in KB:
			the_file.write(str(k)+' ')

if __name__ == '__main__':
	main()



