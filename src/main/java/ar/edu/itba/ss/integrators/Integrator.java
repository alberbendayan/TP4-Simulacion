package ar.edu.itba.ss.integrators;

import ar.edu.itba.ss.Oscillator;

public interface Integrator {

    void initialize(Oscillator osc, double x, double v, double dt);
    double[] step(double x, double v, double t);

}
