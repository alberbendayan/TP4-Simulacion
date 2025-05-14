package ar.edu.itba.ss.single.integrators;

import ar.edu.itba.ss.single.Oscillator;

public class Gear5Integrator implements Integrator {

    private Oscillator osc;
    private double dt;
    private double[] r = new double[6];  // r0 to r5

    public void initialize(Oscillator osc, double x, double v, double dt) {
        this.osc = osc;
        this.dt = dt;
        r[0] = x;
        r[1] = v;
        r[2] = osc.acceleration(x, v);
        r[3] = osc.jerk(x, v);
        r[4] = osc.snap(x, v);
        r[5] = osc.crackle(x, v);
    }

    public double[] step(double x, double v, double t) {
        double[] pred = new double[6];
        double dt1 = dt, dt2 = dt * dt / 2, dt3 = dt * dt * dt / 6, dt4 = dt * dt * dt * dt / 24, dt5 = dt * dt * dt * dt * dt / 120;

        // Predict
        pred[0] = r[0] + dt1 * r[1] + dt2 * r[2] + dt3 * r[3] + dt4 * r[4] + dt5 * r[5];
        pred[1] = r[1] + dt1 * r[2] + dt2 * r[3] + dt3 * r[4] + dt4 * r[5];
        pred[2] = r[2] + dt1 * r[3] + dt2 * r[4] + dt3 * r[5];
        pred[3] = r[3] + dt1 * r[4] + dt2 * r[5];
        pred[4] = r[4] + dt1 * r[5];
        pred[5] = r[5];

        double aReal = osc.acceleration(pred[0], pred[1]);
        double deltaA = aReal - pred[2];
        double deltaR2 = deltaA * dt * dt / 2;

        // Correction coefficients
        double[] alpha = {3.0 / 16, 251.0 / 360, 1.0, 11.0 / 18, 1.0 / 6, 1.0 / 60};

        for (int i = 0; i <= 5; i++) {
            r[i] = pred[i] + alpha[i] * deltaR2 * Math.pow(1.0 / dt, i);
        }

        return new double[]{r[0], r[1]};
    }

}
