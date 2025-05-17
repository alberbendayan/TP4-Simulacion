package ar.edu.itba.ss.coupled;

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
        // Initially all particles are at rest at their equilibrium positions
        for (int i = 0; i < N; i++) {
            positions[i] = 0.0;
            velocities[i] = 0.0;
        }
        // Compute initial accelerations based on t=0
        computeAccelerations(0.0);
    }

    public void computeAccelerations(double t) {
        for (int i = 0; i < N; i++) {
            double yi = positions[i];
            double vi = velocities[i];
            
            // For i=N-1 (last particle), yi+1 is fixed at 0
            // For i=0 (first particle), yi-1 is the forcing function A*sin(ωt)
            double yiMinus = (i == 0) ? A * Math.sin(omega * t) : positions[i - 1];
            double yiPlus = (i == N - 1) ? 0.0 : positions[i + 1];
            
            // Fi = -k(yi-yi-1) - k(yi-yi+1) - γvi
            double force = -k * (yi - yiMinus) - k * (yi - yiPlus) - gamma * vi;
            accelerations[i] = force / m;
        }
    }

    public double[] getPositions() {
        return positions.clone();
    }

    public double[] getVelocities() {
        return velocities.clone();
    }

    public double[] getAccelerations() {
        return accelerations.clone();
    }

    public void updateState(double[] newPos, double[] newVel) {
        this.positions = newPos.clone();
        this.velocities = newVel.clone();
    }

    public int getN() {
        return N;
    }

}
