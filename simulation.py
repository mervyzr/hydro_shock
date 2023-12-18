import time
from datetime import timedelta

import numpy as np

import configs as cfg
import functions as fn
import solvers as solver
import plotting_functions as plotter

##############################################################################

config = "sod"
cells = 100
cfl = .5
gamma = 1.4

livePlot = True

##############################################################################

if config == "sin":
    # sin-wave
    startPos = 0
    endPos = 1
    shockPos = 1
    tEnd = 2
elif config == "sedov":
    # sedov shock
    startPos = -10
    endPos = 10
    shockPos = 1
    tEnd = .6
else:
    # sod shock
    startPos = 0
    endPos = 1
    shockPos = .5
    tEnd = .2


# Main code
def runSimulation(N, _config=config, _cfl=cfl, _gamma=gamma, _startPos=startPos, _endPos=endPos, _shockPos=shockPos, _tEnd=tEnd):
    simulation = {}
    N += (N%2)  # Make N into an even number
    domain = cfg.initialise(N, _config, _gamma, _startPos, _endPos, _shockPos)
    
    # Compute dx and set t = 0
    dx = abs(_endPos-_startPos)/N
    t = 0

    if livePlot:
        fig, ax, plots = plotter.initiateLivePlot(_startPos, _endPos, N)

    while t <= _tEnd:
        # Saves each instance of the system at time t
        tube = fn.convertConservative(domain, _gamma)
        simulation[t] = np.copy(tube)

        if livePlot:
            plotter.updatePlot(tube, t, fig, ax, plots)

        # Compute the numerical fluxes at each interface
        hydroTube = solver.plmSolver(domain, _config, _gamma)
        fluxes = hydroTube.calculateRiemannFlux()

        # Compute new time step
        dt = _cfl * dx/hydroTube.eigmax

        # Update the new solution with the computed time step and the (numerical fluxes?)
        domain -= ((dt/dx) * np.diff(fluxes, axis=0))
        t += dt
    return simulation

##############################################################################

lap = time.time()
run = runSimulation(cells, config)
print(f"[Test={config}, N={cells}; {len(run)} files]  Elapsed: {str(timedelta(seconds=time.time()-lap))} s")
#plotter.makeVideo([run], start=startPos, end=endPos)

"""runs = []
for n in [20, 100, 300, 1000, 4096]:
    config = "sod"
    lap = time.time()
    run = runSimulation(n, config)
    print(f"[Test={config}, N={n}; {len(run)} files]  Elapsed: {str(timedelta(seconds=time.time()-lap))} s")
    runs.append(run)

#plotter.plotQuantities(runs, index=-1, start=startPos, end=endPos)
#plotter.plotSolutionErrors(runs, start=startPos, end=endPos)
#plotter.makeVideo(run, start=startPos, end=endPos)
"""