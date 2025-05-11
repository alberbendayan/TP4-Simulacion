package ar.edu.itba.ss.integrators;

import ar.edu.itba.ss.CoupledOscillators;
import java.math.BigDecimal;
import java.math.MathContext;
import java.math.RoundingMode;

public class VerletCoupledIntegrator implements CoupledIntegrator {
    private static final MathContext MC = new MathContext(20, RoundingMode.HALF_UP);

    private BigDecimal[] prevPositions;

    @Override
    public void initialize(CoupledOscillators osc, BigDecimal dt) {
        int N = osc.getN();
        BigDecimal[] x = osc.getPositions();
        BigDecimal[] v = osc.getVelocities();
        BigDecimal[] a = osc.getAccelerations();
        prevPositions = new BigDecimal[N];
        BigDecimal dt2 = dt.multiply(dt);
        
        for (int i = 0; i < N; i++) {
            prevPositions[i] = x[i].subtract(v[i].multiply(dt))
                                 .add(a[i].multiply(dt2).multiply(BigDecimal.valueOf(0.5)));
        }
    }

    @Override
    public void step(CoupledOscillators osc, BigDecimal t, BigDecimal dt) {
        int N = osc.getN();
        BigDecimal[] x = osc.getPositions();
        BigDecimal[] a = osc.getAccelerations();
        BigDecimal[] newPos = new BigDecimal[N];
        BigDecimal dt2 = dt.multiply(dt);

        for (int i = 0; i < N; i++) {
            newPos[i] = BigDecimal.valueOf(2).multiply(x[i])
                                   .subtract(prevPositions[i])
                                   .add(a[i].multiply(dt2));
        }

        BigDecimal[] newVel = new BigDecimal[N];
        for (int i = 0; i < N; i++) {
            newVel[i] = newPos[i].subtract(prevPositions[i])
                                .divide(BigDecimal.valueOf(2).multiply(dt), MC);
        }

        prevPositions = x;
        osc.updateState(newPos, newVel);
        osc.computeAccelerations(t.add(dt));
    }
}
