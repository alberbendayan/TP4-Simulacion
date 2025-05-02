package ar.edu.itba.ss.integrators;

import ar.edu.itba.ss.Oscillator;

public class VerletIntegrator implements Integrator {

    private Oscillator osc;
    private double dt;
    private double xPrev;

    public void initialize(Oscillator osc, double x, double v, double dt) {
        this.osc = osc;
        this.dt = dt;
        double a = osc.acceleration(x, v);
        this.xPrev = x - v * dt + 0.5 * a * dt * dt;
    }

    public double[] step(double x, double v, double t) {
        double a = osc.acceleration(x, v);
        double xNext = 2 * x - xPrev + dt * dt * a;
        double vNext = (xNext - xPrev) / (2 * dt);
        xPrev = x;
        return new double[]{xNext, vNext};
    }

}
