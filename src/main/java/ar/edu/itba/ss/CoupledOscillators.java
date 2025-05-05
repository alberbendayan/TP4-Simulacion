package ar.edu.itba.ss;

public class CoupledOscillators {
    private final int N;
    private final double m, k, gamma, A, omega;
    private double[] positions, velocities, accelerations;

    public CoupledOscillators(int N, double m, double k, double gamma, double A, double omega) {
        this.N = N;
        this.m = m;
        this.k = k;
        this.gamma = gamma;
        this.A = A;
        this.omega = omega;
        this.positions = new double[N];
        this.velocities = new double[N];
        this.accelerations = new double[N];
    }

    public void initialize() {
        for (int i = 0; i < N; i++) {
            positions[i] = 0.0;
            velocities[i] = 0.0;
        }
        computeAccelerations(0.0);
    }

    public void computeAccelerations(double t) {
        for (int i = 0; i < N; i++) {
            double yi = positions[i];
            double vi = velocities[i];
            double yiMinus = (i == 0) ? 0.0 : positions[i - 1];
            double yiPlus = (i == N - 1) ? A * Math.sin(omega * t) : positions[i + 1];
            accelerations[i] = (-k * (2 * yi - yiMinus - yiPlus) - gamma * vi) / m;
        }
    }

    public double[] getPositions() {
        return positions;
    }

    public double[] getVelocities() {
        return velocities;
    }

    public double[] getAccelerations() {
        return accelerations;
    }

    public void updateState(double[] newPos, double[] newVel) {
        this.positions = newPos;
        this.velocities = newVel;
    }

    public int getN() {
        return N;
    }
}
