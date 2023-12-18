import numpy as np
from scipy.optimize import root_scalar
def rope_recalculate(elements,velocities,t,l):
    dm=0.0001
    forces=calculate_forces(elements,l,velocities,dm)
    elements=elements+velocities*t+forces*(t**2)/(2*dm)
    velocities=velocities+forces*t/dm
    return elements,velocities
def calculate_forces(elements,l,velocities,dm):
    forces=[[0,0]]
    g=np.array([0,0.015])
    for i in range(1,len(elements)):
        force=dm*g
        v1=force/np.linalg.norm(force)
        r=elements[i]-elements[i-1]
        v2=r/np.linalg.norm(r)
        angle=np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0))
        force_x=v2*np.linalg.norm(force)*np.cos(angle)
        force_y=force-force_x
        forces.append(force_y)
    forces=np.array(forces)
    #forces+=-velocities*b
    return forces
