package ar.edu.itba.ss.coupled.integrators;

import ar.edu.itba.ss.coupled.CoupledOscillators;

public class VerletCoupledIntegrator implements CoupledIntegrator {

    private double[] prevPositions;

    @Override
    public void initialize(CoupledOscillators osc, double dt) {
        int N = osc.getN();
        double[] x = osc.getPositions();  // Already a clone
        double[] v = osc.getVelocities();  // Already a clone
        double[] a = osc.getAccelerations();  // Already a clone
        prevPositions = new double[N];
        for (int i = 0; i < N; i++) {
            prevPositions[i] = x[i] - v[i] * dt + 0.5 * a[i] * dt * dt;
        }
    }

    @Override
    public void step(CoupledOscillators osc, double t, double dt) {
        int N = osc.getN();
        double[] x = osc.getPositions();  // Already a clone
        double[] a = osc.getAccelerations();  // Already a clone
        double[] newPos = new double[N];

        // Calculate new positions
        for (int i = 0; i < N; i++) {
            newPos[i] = 2 * x[i] - prevPositions[i] + a[i] * dt * dt;
        }

        // Calculate velocities using central difference
        double[] newVel = new double[N];
        for (int i = 0; i < N; i++) {
            newVel[i] = (newPos[i] - prevPositions[i]) / (2 * dt);
        }

        // Store current positions for next step
        prevPositions = x;  // x is already a clone
        
        // Update state and compute new accelerations
        osc.updateState(newPos, newVel);
        osc.computeAccelerations(t + dt);
    }

}
