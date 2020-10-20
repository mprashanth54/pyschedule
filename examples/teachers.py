# test artefact for the case that pyschedule is
# read from folder
from pyschedule import Scenario, solvers, plotters, alt
import getopt
import sys
sys.path.append('../src')
opts, _ = getopt.getopt(sys.argv[1:], 't:', ['test'])

horizon = 18
S = Scenario('parallel_courses', horizon=horizon)

# size 2 means teacher can do two things in parallel
Teacher = S.Resource('T', size=2, periods=[0, 1, 2, 3, 4, 5, 7, 8, 9])

Courses_English = S.Tasks('CE', num=7, delay_cost=1,
                          plot_color='red', english=1)
Courses_Math = S.Tasks('CM', num=7, delay_cost=1, plot_color='green', math=1)

Courses_English += Teacher
Courses_Math += Teacher

S += Teacher['english'][0:horizon:1].max + \
    Teacher['math'][0:horizon:1].max <= 1


if solvers.mip.solve(S, time_limit=600, msg=0):
    if ('--test', '') in opts:
        assert(len(set(T.start_value for T in Courses_English)
                   & set(T.start_value for T in Courses_Math)) == 0)
        print('test passed')
    else:
        plotters.matplotlib.plot(S, show_task_labels=True)
else:
    print('no solution found')
    assert(1 == 0)
