package ar.edu.itba.ss.integrators;

import ar.edu.itba.ss.Oscillator;
import java.math.BigDecimal;
import java.math.MathContext;
import java.math.RoundingMode;

public class BeemanIntegrator implements Integrator {
    private static final MathContext MC = new MathContext(20, RoundingMode.HALF_UP);

    private Oscillator osc;
    private BigDecimal dt;
    private BigDecimal aPrev;

    public void initialize(Oscillator osc, BigDecimal x, BigDecimal v, BigDecimal dt) {
        this.osc = osc;
        this.dt = dt;
        this.aPrev = osc.acceleration(x, v);
    }

    public BigDecimal[] step(BigDecimal x, BigDecimal v, BigDecimal t) {
        BigDecimal a = osc.acceleration(x, v);
        BigDecimal dt2 = dt.multiply(dt);
        
        // Calculate xNext
        BigDecimal term1 = v.multiply(dt);
        BigDecimal term2 = BigDecimal.valueOf(2.0/3.0).multiply(a);
        BigDecimal term3 = BigDecimal.valueOf(1.0/6.0).multiply(aPrev);
        BigDecimal xNext = x.add(term1)
                           .add(dt2.multiply(term2.subtract(term3)));
        
        // Calculate vNext
        BigDecimal aNext = osc.acceleration(xNext, v);  // v provisional
        BigDecimal term4 = BigDecimal.valueOf(1.0/3.0).multiply(aNext);
        BigDecimal term5 = BigDecimal.valueOf(5.0/6.0).multiply(a);
        BigDecimal term6 = BigDecimal.valueOf(1.0/6.0).multiply(aPrev);
        BigDecimal vNext = v.add(dt.multiply(term4.add(term5).subtract(term6)));

        aPrev = a;
        return new BigDecimal[]{xNext, vNext};
    }
}
