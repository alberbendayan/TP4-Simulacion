package ar.edu.itba.ss.integrators;
import ar.edu.itba.ss.CoupledOscillators;

public interface CoupledIntegrator {
    void initialize(CoupledOscillators osc, double dt);
    void step(CoupledOscillators osc, double t, double dt);
}
