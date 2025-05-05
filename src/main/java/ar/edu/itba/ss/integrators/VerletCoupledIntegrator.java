package ar.edu.itba.ss.integrators;

import ar.edu.itba.ss.CoupledOscillators;

public class VerletCoupledIntegrator implements CoupledIntegrator {

    private double[] prevPositions;

    @Override
    public void initialize(CoupledOscillators osc, double dt) {
        int N = osc.getN();
        double[] x = osc.getPositions();
        double[] v = osc.getVelocities();
        double[] a = osc.getAccelerations();
        prevPositions = new double[N];
        for (int i = 0; i < N; i++) {
            prevPositions[i] = x[i] - v[i] * dt + 0.5 * a[i] * dt * dt;
        }
    }

    @Override
    public void step(CoupledOscillators osc, double t, double dt) {
        int N = osc.getN();
        double[] x = osc.getPositions();
        double[] a = osc.getAccelerations();
        double[] newPos = new double[N];
        for (int i = 0; i < N; i++) {
            newPos[i] = 2 * x[i] - prevPositions[i] + a[i] * dt * dt;
        }

        double[] newVel = new double[N];
        for (int i = 0; i < N; i++) {
            newVel[i] = (newPos[i] - prevPositions[i]) / (2 * dt);
        }

        prevPositions = x;
        osc.updateState(newPos, newVel);
        osc.computeAccelerations(t + dt);
    }
}
