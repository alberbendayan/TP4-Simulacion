package ar.edu.itba.ss;

import java.math.BigDecimal;
import java.math.MathContext;
import java.math.RoundingMode;

public class CoupledOscillators {
    private static final MathContext MC = new MathContext(20, RoundingMode.HALF_UP);
    
    private final int N;
    private final BigDecimal m, k, gamma, A, omega;
    private BigDecimal[] positions, velocities, accelerations;

    public CoupledOscillators(int N, BigDecimal m, BigDecimal k, BigDecimal gamma, BigDecimal A, BigDecimal omega) {
        this.N = N;
        this.m = m;
        this.k = k;
        this.gamma = gamma;
        this.A = A;
        this.omega = omega;
        this.positions = new BigDecimal[N];
        this.velocities = new BigDecimal[N];
        this.accelerations = new BigDecimal[N];
    }

    public void initialize() {
        for (int i = 0; i < N; i++) {
            positions[i] = BigDecimal.ZERO;
            velocities[i] = BigDecimal.ZERO;
        }
        computeAccelerations(BigDecimal.ZERO);
    }

    public void computeAccelerations(BigDecimal t) {
        for (int i = 0; i < N; i++) {
            BigDecimal yi = positions[i];
            BigDecimal vi = velocities[i];
            BigDecimal yiMinus = (i == 0) ? A.multiply(BigDecimal.valueOf(Math.sin(omega.multiply(t).doubleValue()))) : positions[i - 1];
            BigDecimal yiPlus = (i == N - 1) ? BigDecimal.ZERO : positions[i + 1];
            
            BigDecimal term1 = BigDecimal.valueOf(2).multiply(yi).subtract(yiMinus).subtract(yiPlus);
            BigDecimal term2 = k.multiply(term1);
            BigDecimal term3 = gamma.multiply(vi);
            accelerations[i] = term2.add(term3).negate().divide(m, MC);
        }
    }

    public BigDecimal[] getPositions() {
        return positions;
    }

    public BigDecimal[] getVelocities() {
        return velocities;
    }

    public BigDecimal[] getAccelerations() {
        return accelerations;
    }

    public void updateState(BigDecimal[] newPos, BigDecimal[] newVel) {
        this.positions = newPos;
        this.velocities = newVel;
    }

    public int getN() {
        return N;
    }
}
