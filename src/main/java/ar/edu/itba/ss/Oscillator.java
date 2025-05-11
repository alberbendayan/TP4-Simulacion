package ar.edu.itba.ss;

import java.math.BigDecimal;
import java.math.MathContext;
import java.math.RoundingMode;

public class Oscillator {
    private static final MathContext MC = new MathContext(20, RoundingMode.HALF_UP);

    public final BigDecimal m, k, gamma;
    public final BigDecimal x0, v0;

    public Oscillator(BigDecimal m, BigDecimal k, BigDecimal gamma, BigDecimal x0, BigDecimal v0) {
        this.m = m;
        this.k = k;
        this.gamma = gamma;
        this.x0 = x0;
        this.v0 = v0;
    }

    public BigDecimal acceleration(BigDecimal x, BigDecimal v) {
        return x.multiply(k).add(v.multiply(gamma)).negate().divide(m, MC);
    }

    public BigDecimal analytical(BigDecimal t) {
        BigDecimal omega0 = BigDecimal.valueOf(Math.sqrt(k.divide(m, MC).doubleValue()));
        BigDecimal gamma_m = gamma.divide(BigDecimal.valueOf(2).multiply(m), MC);
        BigDecimal omega_d = BigDecimal.valueOf(Math.sqrt(
                omega0.multiply(omega0).subtract(gamma_m.multiply(gamma_m)).doubleValue()));

        BigDecimal expTerm = BigDecimal.valueOf(Math.exp(-gamma_m.multiply(t).doubleValue()));
        BigDecimal cosTerm = BigDecimal.valueOf(Math.cos(omega_d.multiply(t).doubleValue()));
        BigDecimal sinTerm = BigDecimal.valueOf(Math.sin(omega_d.multiply(t).doubleValue()));

        BigDecimal firstTerm = x0.multiply(cosTerm);
        BigDecimal secondTerm = v0.add(gamma_m.multiply(x0))
                .divide(omega_d, MC)
                .multiply(sinTerm);

        return expTerm.multiply(firstTerm.add(secondTerm));
    }

    public static interface CoupledIntegrator {
        void initialize(CoupledOscillators osc, BigDecimal dt);

        void step(CoupledOscillators osc, BigDecimal t, BigDecimal dt);
    }

    public BigDecimal jerk(BigDecimal x, BigDecimal v) {
        BigDecimal a = acceleration(x, v);
        return k.multiply(v).add(gamma.multiply(a)).negate().divide(m, MC);
    }

    public BigDecimal snap(BigDecimal x, BigDecimal v) {
        BigDecimal a = acceleration(x, v);
        BigDecimal j = jerk(x, v);
        return k.multiply(a).add(gamma.multiply(j)).negate().divide(m, MC);
    }

    public BigDecimal crackle(BigDecimal x, BigDecimal v) {
        BigDecimal j = jerk(x, v);
        BigDecimal s = snap(x, v);
        return k.multiply(j).add(gamma.multiply(s)).negate().divide(m, MC);
    }
}
