#This is a code that i wrote to understand
#the concepts in constraint satisfaction problems by using
#backtracking, LCV, MRV etc
#In this code there are given constraints and it should assign values accordingly

from collections import defaultdict

teachers = ["Mr.Smith", "Ms.Johnson", "Dr.Patel"]
subjects = ["Maths", "History", "Physics"]
domain = {
    "Mr.Smith": ["Maths", "Physics"],
    "Ms.Johnson": ["Maths", "History"],
    "Dr.Patel": ["Maths", "History", "Physics"]
}

def is_consistent(assignment, subject):
    return subject not in assignment.values()

def unassigned_teacher(assignment):
    unassigned = [t for t in teachers if t not in assignment]
    return min(unassigned, key=lambda k: len(domain[k]))

def order_domain_values(teacher, assignment):
    counts = defaultdict(int)
    for t in teachers:
        if t!=teacher and t not in assignment:
            for s in domain[t]:
                counts[s]+=1
    return sorted(domain[teacher], key=lambda s: counts[s], reverse=True)

def backtrack(assignment):
    if len(assignment) == len(teachers):
        return assignment
    teacher = unassigned_teacher(assignment)
    for subject in order_domain_values(teacher, assignment):
        if is_consistent(assignment, subject):
            assignment[teacher] = subject
            result = backtrack(assignment)
            if result:
                return result
            del assignment[teacher]
    return None

assignment = backtrack({})
for t in assignment:
    print(f"{t} will teach {assignment[t]}")

















