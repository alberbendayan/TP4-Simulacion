package ar.edu.itba.ss.integrators;

import ar.edu.itba.ss.Oscillator;
import java.math.BigDecimal;
import java.math.MathContext;
import java.math.RoundingMode;

public class VerletIntegrator implements Integrator {
    private static final MathContext MC = new MathContext(20, RoundingMode.HALF_UP);

    private Oscillator osc;
    private BigDecimal dt;
    private BigDecimal xPrev;

    public void initialize(Oscillator osc, BigDecimal x, BigDecimal v, BigDecimal dt) {
        this.osc = osc;
        this.dt = dt;
        BigDecimal a = osc.acceleration(x, v);
        BigDecimal dt2 = dt.multiply(dt);
        this.xPrev = x.subtract(v.multiply(dt))
                     .add(a.multiply(dt2).multiply(BigDecimal.valueOf(0.5)));
    }

    public BigDecimal[] step(BigDecimal x, BigDecimal v, BigDecimal t) {
        BigDecimal a = osc.acceleration(x, v);
        BigDecimal dt2 = dt.multiply(dt);
        BigDecimal xNext = BigDecimal.valueOf(2).multiply(x)
                                    .subtract(xPrev)
                                    .add(a.multiply(dt2));
        BigDecimal vNext = xNext.subtract(xPrev)
                               .divide(BigDecimal.valueOf(2).multiply(dt), MC);
        xPrev = x;
        return new BigDecimal[]{xNext, vNext};
    }
}
