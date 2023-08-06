import sys
import numpy as np
import time
import examples.examples_all_functions as exf

# read the command line arguments into an array
xs = np.asarray([float(x) for x in sys.argv[1:]])

# evaluate the cost, i.e. the parabola
cost = exf.parabolic_cost_function(x=xs)

# In order to demonstrate uncertain evaluation times, we shall use a random sleep in each cost function.
# In this case, each function evaluation can take between 0-10 sec
time.sleep(np.random.random() * 10.)

# Write into a result file. Note that this script is evaluated in its respective folder and so
# the result.txt file will be in the generated folder and not the home directory of running example3.py
with open('result.txt', 'w') as f:
    f.write(str(cost) + '\n')
