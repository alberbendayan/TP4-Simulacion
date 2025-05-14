package ar.edu.itba.ss.coupled.integrators;

import ar.edu.itba.ss.coupled.CoupledOscillators;

public interface CoupledIntegrator {

    void initialize(CoupledOscillators osc, double dt);
    void step(CoupledOscillators osc, double t, double dt);

}
