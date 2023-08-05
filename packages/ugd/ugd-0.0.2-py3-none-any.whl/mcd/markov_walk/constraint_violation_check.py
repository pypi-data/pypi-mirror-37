import numpy as np

# fixme: this has to be an interface which can be customized
def no_violations(violation_matrix):
    return np.all(violation_matrix==0)

