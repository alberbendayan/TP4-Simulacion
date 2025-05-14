package ar.edu.itba.ss.single.integrators;

import ar.edu.itba.ss.single.Oscillator;

public class BeemanIntegrator implements Integrator {

    private Oscillator osc;
    private double dt;
    private double aPrev;

    public void initialize(Oscillator osc, double x, double v, double dt) {
        this.osc = osc;
        this.dt = dt;
        this.aPrev = osc.acceleration(x, v);
    }

    public double[] step(double x, double v, double t) {
        double a = osc.acceleration(x, v);
        double xNext = x + v * dt + (2.0 / 3.0 * a - 1.0 / 6.0 * aPrev) * dt * dt;

        // Predecir velocidad para estimar aNext
        double vPred = v + (3.0 / 2.0 * a - 1.0 / 2.0 * aPrev) * dt;

        double aNext = osc.acceleration(xNext, vPred);

        double vNext = v + (1.0 / 3.0 * aNext + 5.0 / 6.0 * a - 1.0 / 6.0 * aPrev) * dt;

        aPrev = a;
        return new double[]{xNext, vNext};
    }

}
