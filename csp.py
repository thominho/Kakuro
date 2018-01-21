"""CSP (Constraint Satisfaction Problems) problems and solvers. (Chapter 6)."""

from utils import *
import search
import math, random, sys, time, bisect, string

class CSP(search.Problem):
    """This class describes finite-domain Constraint Satisfaction Problems.
    A CSP is specified by the following inputs:
        vars        A list of variables; each is atomic (e.g. int or string).
        domains     A dict of {var:[possible_value, ...]} entries.
        neighbors   A dict of {var:[var,...]} that for each variable lists
                    the other variables that participate in constraints.
        constraints A function f(A, a, B, b) that returns true if neighbors
                    A, B satisfy the constraint when they have values A=a, B=b
    In the textbook and in most mathematical definitions, the
    constraints are specified as explicit pairs of allowable values,
    but the formulation here is easier to express and more compact for
    most cases. (For example, the n-Queens problem can be represented
    in O(n) space using this notation, instead of O(N^4) for the
    explicit representation.) In terms of describing the CSP as a
    problem, that's all there is.

    However, the class also supports data structures and methods that help you
    solve CSPs by calling a search function on the CSP.  Methods and slots are
    as follows, where the argument 'a' represents an assignment, which is a
    dict of {var:val} entries:
        assign(var, val, a)     Assign a[var] = val; do other bookkeeping
        unassign(var, a)        Do del a[var], plus other bookkeeping
        nconflicts(var, val, a) Return the number of other variables that
                                conflict with var=val
        curr_domains[var]       Slot: remaining consistent values for var
                                Used by constraint propagation routines.
    The following methods are used only by graph_search and tree_search:
        actions(state)          Return a list of actions
        result(state, action)   Return a successor of state
        goal_test(state)        Return true if all constraints satisfied
    The following are just for debugging purposes:
        nassigns                Slot: tracks the number of assignments made
        display(a)              Print a human-readable representation

    >>> search.depth_first_graph_search(australia)
    <Node (('WA', 'B'), ('Q', 'B'), ('T', 'B'), ('V', 'B'), ('SA', 'G'), ('NT', 'R'), ('NSW', 'R'))>
    """

    def __init__(self, vars, domains, neighbors, constraints):
        "Construct a CSP problem. If vars is empty, it becomes domains.keys()."
        vars = vars or domains.keys()
        self.algorithm= "bt"
        update(self, vars=vars, domains=domains,
               neighbors=neighbors, constraints=constraints,
               initial=(), curr_domains=None, nassigns=0,nconfl=0)

    def assign(self, var, val, assignment):
        "Add {var: val} to assignment; Discard the old value if any."
        assignment[var] = val
        self.nassigns += 1
        if(self.nassigns%1000==0):
           print self.nassigns

    def unassign(self, var, assignment):
        """Remove {var: val} from assignment.
        DO NOT call this if you are changing a variable to a new value;
        just call assign for that."""
        if var in assignment:
            del assignment[var]

    def nconflicts(self, var, val, assignment):
        "Return the number of conflicts var=val has with other variables."
        # Subclasses may implement this more efficiently
        self.nconfl = self.nconfl + 1
        if(self.nconfl%1000==0):
           print self.nconfl
        def conflict(var2):
            return (var2 in assignment
                    and not self.constraints(var, val, var2, assignment[var2]))
        return count_if(conflict, self.neighbors[var])

    def display(self, assignment):
        "Show a human-readable representation of the CSP."
        # Subclasses can print in a prettier way, or display with a GUI
        print 'CSP:', self, 'with assignment:', assignment

    ## These methods are for the tree- and graph-search interface:

    def actions(self, state):
        """Return a list of applicable actions: nonconflicting
        assignments to an unassigned variable."""
        if len(state) == len(self.vars):
            return []
        else:
            assignment = dict(state)
            var = find_if(lambda v: v not in assignment, self.vars)
            return [(var, val) for val in self.domains[var]
                    if self.nconflicts(var, val, assignment) == 0]

    def result(self, state, (var, val)):
        "Perform an action and return the new state."
        return state + ((var, val),)

    def goal_test(self, state):
        "The goal is to assign all vars, with all constraints satisfied."
        assignment = dict(state)
        elapsed_time = time.time() - start_time
        print "elapsed_time = ",elapsed_time,"secs"
        print "No of final assigns ",self.nassigns
        print "No of final conflicts",self.nconfl
        return (len(assignment) == len(self.vars) and
                every(lambda var: self.nconflicts(var, assignment[var],
                                                  assignment) == 0,
                      self.vars))

    ## These are for constraint propagation

    def support_pruning(self):
        """Make sure we can prune values from domains. (We want to pay
        for this only if we use it.)"""
        if self.curr_domains is None:
            self.curr_domains = dict((v, list(self.domains[v]))
                                     for v in self.vars)

    def suppose(self, var, value):
        "Start accumulating inferences from assuming var=value."
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals

    def prune(self, var, value, removals):
        "Rule out var=value."
        self.curr_domains[var].remove(value)
        if removals is not None: removals.append((var, value))

    def choices(self, var):
        "Return all values for var that aren't currently ruled out."
        return (self.curr_domains or self.domains)[var]

    def infer_assignment(self):
        "Return the partial assignment implied by the current inferences."
        self.support_pruning()
        return dict((v, self.curr_domains[v][0])
                    for v in self.vars if 1 == len(self.curr_domains[v]))

    def restore(self, removals):
        "Undo a supposition and all inferences from it."
        for B, b in removals:
            self.curr_domains[B].append(b)

    ## This is for min_conflicts search

    def conflicted_vars(self, current):
        "Return a list of variables in current assignment that are in conflict"
        return [var for var in self.vars
                if self.nconflicts(var, current[var], current) > 0]

#______________________________________________________________________________
# Constraint Propagation with AC-3

def AC3(csp, queue=None, removals=None):
    """[Fig. 6.3]"""
    if queue is None:
        queue = [(Xi, Xk) for Xi in csp.vars for Xk in csp.neighbors[Xi]]
    csp.support_pruning()
    while queue:
        (Xi, Xj) = queue.pop()
        if revise(csp, Xi, Xj, removals):
            if not csp.curr_domains[Xi]:
                return False
            for Xk in csp.neighbors[Xi]:
                if Xk != Xi:
                    queue.append((Xk, Xi))
    return True

def revise(csp, Xi, Xj, removals):
    "Return true if we remove a value."
    revised = False
    for x in csp.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        if every(lambda y: not csp.constraints(Xi, x, Xj, y),
                 csp.curr_domains[Xj]):
            csp.prune(Xi, x, removals)
            revised = True
    return revised

#______________________________________________________________________________
# CSP Backtracking Search

# Variable ordering

def first_unassigned_variable(assignment, csp):
    "The default variable order."
    return find_if(lambda var: var not in assignment, csp.vars)

def mrv(assignment, csp):
    "Minimum-remaining-values heuristic."
    return argmin_random_tie(
        [v for v in csp.vars if v not in assignment],
        lambda var: num_legal_values(csp, var, assignment))

def num_legal_values(csp, var, assignment):
    return len(csp.domains[var])

# Value ordering

def unordered_domain_values(var, assignment, csp):
    "The default value order."
    return csp.choices(var)

def lcv(var, assignment, csp):
    "Least-constraining-values heuristic."
    return sorted(csp.choices(var),
                  key=lambda val: csp.nconflicts(var, val, assignment))

# Inference

def no_inference(csp, var, value, assignment, removals):
    return True

def forward_checking(csp, var, value, assignment, removals):
    "Prune neighbor values inconsistent with var=value."
    if(csp.algorithm!="fcmrv"):
        for B in csp.neighbors[var]:
            if B not in assignment:
                for b in csp.curr_domains[B][:]:
                    if not csp.constraints(var, value, B, b):
                        csp.prune(B, b, removals)
                if not csp.curr_domains[B]:
                    return False
    else:
        for B in csp.neighbors[var]:
            if B not in assignment:
                for b in csp.curr_domains[B][:]:
                    if not csp.constraints(var, value, assignment,csp.neighbors,4):
                        csp.prune(B, b, removals)
                if not csp.curr_domains[B]:
                    return False
    return True

def mac(csp, var, value, assignment, removals):
    "Maintain arc consistency."
    return AC3(csp, [(X, var) for X in csp.neighbors[var]], removals)

# The search, proper

def backtracking_search(csp,
                        select_unassigned_variable = first_unassigned_variable,
                        order_domain_values = unordered_domain_values,
                        inference = no_inference,variaty=0):
    """[Fig. 6.5]
    >>> backtracking_search(australia) is not None
    True
    >>> backtracking_search(australia, select_unassigned_variable=mrv) is not None
    True
    >>> backtracking_search(australia, order_domain_values=lcv) is not None
    True
    >>> backtracking_search(australia, select_unassigned_variable=mrv, order_domain_values=lcv) is not None
    True
    >>> backtracking_search(australia, inference=forward_checking) is not None
    True
    >>> backtracking_search(australia, inference=mac) is not None
    True
    >>> backtracking_search(usa, select_unassigned_variable=mrv, order_domain_values=lcv, inference=mac) is not None
    True
    """

    def backtrack(assignment):
        if len(assignment) == len(csp.vars):
            return assignment
        var = select_unassigned_variable(assignment, csp)
        for value in order_domain_values(var, assignment, csp):
            if 0 == csp.nconflicts(var, value, assignment):
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)
                if inference(csp, var, value, assignment, removals):
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                csp.restore(removals)
        csp.unassign(var, assignment)
        return None
    if(variaty==4):
            csp.algorithm="fcmrv"
    result = backtrack({})
    print "No of final assigns ",csp.nassigns
    print "No of final conflicts",csp.nconfl
    return result


class UniversalDict:
    """A universal dict maps any key to the same value. We use it here
    as the domains dict for CSPs in which all vars have the same domain.
    >>> d = UniversalDict(42)
    >>> d['life']
    42
    """
    def __init__(self, value): self.value = value
    def __getitem__(self, key): return self.value
    def __repr__(self): return '{Any: %r}' % self.value
