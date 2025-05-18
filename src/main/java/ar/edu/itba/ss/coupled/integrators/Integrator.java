package ar.edu.itba.ss.coupled.integrators;

import ar.edu.itba.ss.coupled.Oscillator;

public interface Integrator {

    void initialize(Oscillator osc, double dt);
    void step(Oscillator osc, double t, double dt);

}
