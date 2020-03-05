# import sys
import z3
# sys.path.append('/Users/thestlucas/Desktop/ProbLogic/parseR/')
# from tools import parse_pddl

from itertools import combinations
import re

########################################################################################################################

def get_predicates_pddlpy(domprob):
	predicates = []
	for op in domprob.operators():
		for o in domprob.ground_operator(op):
			for i in list(o.precondition_pos):
				# s = "_"
				#
				# s = s.join(i)
				predicates.append(i[0])
	for op in domprob.operators():
		for o in domprob.ground_operator(op):
			for i in list(o.effect_pos):
				predicates.append(i[0])
	for op in domprob.operators():
		for o in domprob.ground_operator(op):
			for i in list(o.effect_neg):
				predicates.append(i[0])


	predicates = list(set(predicates))

	for v in predicates:
		v = str(v).lower()
		v = re.sub('[\\{\}<>-_()]', ' ', v)
		v = v.replace('-', '')
		v = v.strip()
		v = v[:v.find(" ")]
	return predicates



def convert_to_symbols(sentence):
	return '_'.join(sentence).upper()


def convert_to_symbolic(x):

	x = re.sub('[\(\)\{\}<>-]', '', x)
	if ',' in x:
		x = x.split(", ")
		x = '_'.join(x)
	else:
		x = x.split(" ")
		x = '_'.join(x)
	x = x.upper()
	return x


def make_successor_symbols(symbs, t):
	symbs = [str(i) for i in symbs]
	dct = {}
	for i in range(t):
		dct[i] = [item + '_{}'.format(i) for item in symbs]
	return dct

def init_states(task):
	init = list(task.initial_state)
	symbs_init = []
	for i in init:
		symbs_init.append(convert_to_symbolic(i))

	Init = make_successor_symbols(symbs_init, 1)[0]

	facts = list(task.facts)
	facts = [re.sub('[\(\)\{\}<>-]', '', facts[i]).upper() for i in range(len(list(facts))) ]
	symbs_facts = []
	for i in facts:
		symbs_facts.append(convert_to_symbolic(i))

	Facts = make_successor_symbols(symbs_facts, 1)[0]
	Facts = [convert_to_symbolic(j) for j in Facts]


	initial_conds = []
	for i in Facts:
		if i not in Init:
			initial_conds.append(z3.Not(z3.Bool(str(i))))
	for i in Init:
		initial_conds.append(z3.Bool(str(i)))
	return initial_conds



def goal_state(task, t):
	goal = list(task.goals)
	symbs_goal = []
	for i in goal:
		symbs_goal.append(convert_to_symbolic(i))

	Goal = make_successor_symbols(symbs_goal, t+1)[t]
	Goal = [z3.Bool(str(convert_to_symbolic(j))) for j in Goal]
	return Goal






def Preconditons(task,domprob, horizon):

	def action_preconditions(task, t):

		for op in task.operators:
			preconds_temp = [convert_to_symbolic(i) for i in list(op.preconditions)]
			if preconds_temp:
				for p in preconds_temp:
					yield z3.Implies(z3.Bool(str(make_successor_symbols([convert_to_symbolic(op.name)],t)[t-1][0])), z3.And([z3.Bool(str(z)) for z in make_successor_symbols([p],t)[t-1]]))
			# elif not preconds_temp:
			#     yield z3.Implies(z3.Bool(str(make_successor_symbols([convert_to_symbolic(op.name)],t)[t-1][0])), z3.Bool('True'))

		if not preconds_temp:

			for op in list( domprob.operators()):
				for i in list(domprob.ground_operator(op))[0].precondition_pos:

					element = next(iter(i))
					element, = element

					preconds_temp2 = [convert_to_symbolic(element)]
					if preconds_temp2:
						for p in preconds_temp2:
							yield z3.Implies(
								z3.Bool(str(make_successor_symbols([convert_to_symbolic(op)], t)[t - 1][0])),
								z3.And([z3.Bool(str(z)) for z in make_successor_symbols([p], t)[t - 1]]))


	pres = []
	for i in range(horizon):
		pres.append(list(action_preconditions(task, i+1)))
	pres = [item for sublist in pres for item in sublist]

	return pres

def Add_Effects(task, domprob, horizon):

	def action_effects(task, t):
		#
		# for op in task.operators:
		# 	effects_temp = [convert_to_symbolic(i) for i in list(op.add_effects)]
		# 	if effects_temp:
		# 		for e in effects_temp:
		# 			yield z3.Implies(z3.Bool(str(make_successor_symbols([convert_to_symbolic(op.name)],t)[t-1][0])), z3.And([z3.Bool(str(z)) for z in make_successor_symbols([e],t+1)[t]]))
	#             elif not effects_temp:
	#                 yield z3.Implies(z3.Bool(str(make_successor_symbols([convert_to_symbolic(op.name)],t)[t-1][0])), z3.Bool('True'))

		for op in list(domprob.operators()):
			effects_temp = []
			for i in list(domprob.ground_operator(op)):
				if not all(elem == list(i.variable_list.values())[0] for elem in list(i.variable_list.values())):
					tem = '_'.join(list(i.variable_list.values()))
					names = str(op).upper() + '_' + tem
					effects_temp = ['_'.join(j).upper() for j in list(i.effect_pos)]

				if effects_temp:
					for e in effects_temp:
						yield z3.Implies(
							z3.Bool(str(make_successor_symbols([convert_to_symbolic(names)], t)[t - 1][0])),
							z3.And([z3.Bool(str(z)) for z in make_successor_symbols([e], t + 1)[t]]))


	effs = []
	for i in range(horizon):
		effs.append(list(action_effects(task, i+1)))



	effs = [item for sublist in effs for item in sublist]

	return effs



def Del_Effects(task, domprob, horizon):

	def action_effects(task, t):

	# 	for op in task.operators:
	# 		effects_temp = [z3.Bool(convert_to_symbolic(i)) for i in list(op.del_effects)]
	# 		if effects_temp:
	# 			for e in effects_temp:
	# 				yield z3.Implies(z3.Bool(str(make_successor_symbols([convert_to_symbolic(op.name)],t)[t-1][0])), z3.And([z3.Not(z3.Bool(z)) for z in make_successor_symbols([e],t+1)[t]]))
	# #             elif not effects_temp:
	#                 yield z3.Implies(z3.Bool(str(make_successor_symbols([convert_to_symbolic(op.name)],t)[t-1][0])), z3.Bool('True'))

		for op in list(domprob.operators()):
			effects_temp = []
			for i in list(domprob.ground_operator(op)):
				if not all(elem == list(i.variable_list.values())[0] for elem in list(i.variable_list.values())):

					tem = '_'.join(list(i.variable_list.values()))
					names = str(op).upper() + '_' + tem
					effects_temp = ['_'.join(j).upper() for j in list(i.effect_neg)]

				if effects_temp:
					for e in effects_temp:
						yield z3.Implies(z3.Bool(str(make_successor_symbols([convert_to_symbolic(names)],t)[t-1][0])),
										 z3.And([z3.Not(z3.Bool(z)) for z in make_successor_symbols([e],t+1)[t]]))


	effs = []
	for i in range(horizon):
		effs.append(list(action_effects(task, i+1)))



	effs = [item for sublist in effs for item in sublist]

	return effs


def Frames_addeff(task, domprob, horizon):
	def frames_addeff(task, t):
		# predicates = [convert_to_symbolic(i) for i in list(task.facts)]
		# for p in predicates:
		# 	temp = []
		# 	for op in task.operators:
		# 		effects_temp = [convert_to_symbolic(i) for i in list(op.add_effects)]
		# 		if p in effects_temp:
		# 			temp.append(convert_to_symbolic(op.name))
		# 	if temp:
		# 		yield z3.Implies(z3.And(z3.Not(z3.Bool(str(make_successor_symbols([p],t)[t-1][0]))), z3.Bool(make_successor_symbols([p],t+1)[t][0])), z3.Or([z3.Bool(str(k)) for k in make_successor_symbols(temp,t)[t-1] ])   )
	#             elif not temp:
	#                 yield ~expr(make_successor_symbols(p,t)[t-1][0])&expr(make_successor_symbols(p,t+1)[t][0]) |'==>'| Symbol('True')
		predicates = [convert_to_symbolic(i) for i in list(task.facts)]
		for p in predicates:
			temp = []
			for op in list(domprob.operators()):
				effects_temp = []
				for i in list(domprob.ground_operator(op)):
					if not all(elem == list(i.variable_list.values())[0] for elem in list(i.variable_list.values())):

						tem = '_'.join(list(i.variable_list.values()))
						names = str(op).upper() + '_' + tem
						effects_temp = ['_'.join(j).upper() for j in list(i.effect_pos)]
						if p in effects_temp:
							temp.append(convert_to_symbolic(names))
			if temp:
				yield z3.Implies(z3.And(z3.Not(z3.Bool(str(make_successor_symbols([p],t)[t-1][0]))), z3.Bool(make_successor_symbols([p],t+1)[t][0])),
								 z3.Or([z3.Bool(str(k)) for k in make_successor_symbols(temp,t)[t-1] ])   )
		#


	frames = []
	for i in range(horizon):
		frames.append(list(frames_addeff(task, i+1)))



	frames = [item for sublist in frames for item in sublist]

	return frames


def Frames_deleff(task, domprob, horizon):
	def frames_deleff(task, t):
		predicates = [convert_to_symbolic(i) for i in list(task.facts)]
		for p in predicates:
			temp = []
			for op in list(domprob.operators()):
				for i in list(domprob.ground_operator(op)):
					if not all(elem == list(i.variable_list.values())[0] for elem in list(i.variable_list.values())):

						tem = '_'.join(list(i.variable_list.values()))
						names = str(op).upper() + '_' + tem
						effects_temp = ['_'.join(j).upper() for j in list(i.effect_neg)]
						if p in effects_temp:
							temp.append(convert_to_symbolic(names))
			if temp:
				yield z3.Implies(z3.And(z3.Bool(str(make_successor_symbols([p], t)[t - 1][0])),
										z3.Not(z3.Bool(make_successor_symbols([p], t + 1)[t][0]))),
								 z3.Or([z3.Bool(str(k)) for k in make_successor_symbols(temp, t)[t - 1]]))

	#             elif not temp:
	#                 yield expr(make_successor_symbols(p, t)[t - 1][0]) & ~expr(make_successor_symbols(p, t + 1)[t][0]) | '==>' | Symbol('True')


	frames = []
	for i in range(horizon):
		frames.append(list(frames_deleff(task, i+1)))



	frames = [item for sublist in frames for item in sublist]

	return frames


def exclusion_axioms(task, t):
	actions = []
	axioms =  []
	for op in task.operators:
		actions.append(convert_to_symbolic(op.name))
	actions = list(combinations(actions, 2))
	for act in actions:
		temp = make_successor_symbols(act, t)
		for i in temp:
			axioms.append(temp[i])
	for i in range(len(axioms)):
		axioms[i] = [z3.Bool(convert_to_symbolic(j)) for j in axioms[i]]
		axioms[i] = [z3.Or(z3.Not(axioms[i][0]) , z3.Not(axioms[i][1]))]

	axioms = [item for sublist in axioms for item in sublist]

	return axioms














