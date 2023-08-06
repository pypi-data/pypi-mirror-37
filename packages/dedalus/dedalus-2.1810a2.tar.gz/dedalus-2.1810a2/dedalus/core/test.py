
import numpy as np
from mpi4py import MPI
#from dedalus import public as de

import logging
logger = logging.getLogger(__name__)
logger.info('Running test_cart')

comm = MPI.COMM_WORLD
mesh = np.array([8, 16])

logger.info('Creating comm cart')
comm_cart = comm.Create_cart(mesh)
logger.info('Finished creating comm cart')

logger.info('Creating comm subs')
comm_subs = []
for axis in range(comm_cart.dim):
    remain_dims = [0] * comm_cart.dim
    remain_dims[axis] = 1
    comm_subs.append(comm_cart.Sub(remain_dims))
logger.info('Finished creating comm subs')

