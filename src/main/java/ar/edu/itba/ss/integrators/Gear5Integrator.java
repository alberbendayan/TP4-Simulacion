package ar.edu.itba.ss.integrators;

import ar.edu.itba.ss.CoupledOscillators;
import ar.edu.itba.ss.Oscillator;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.math.MathContext;

public class Gear5Integrator implements Integrator {

    private Oscillator osc;
    private BigDecimal dt;
    private BigDecimal[] r = new BigDecimal[6];  // r0 to r5
    private static final MathContext MC = new MathContext(20, RoundingMode.HALF_UP);

    public void initialize(Oscillator osc, BigDecimal x, BigDecimal v, BigDecimal dt) {
        this.osc = osc;
        this.dt = dt;
        r[0] = x;
        r[1] = v;
        r[2] = osc.acceleration(x, v);
        r[3] = osc.jerk(x, v);
        r[4] = osc.snap(x, v);
        r[5] = osc.crackle(x, v);
    }

    public BigDecimal[] step(BigDecimal x, BigDecimal v, BigDecimal t) {
        BigDecimal[] pred = new BigDecimal[6];
        BigDecimal dt1 = dt;
        BigDecimal dt2 = dt.multiply(dt).divide(BigDecimal.valueOf(2), MC);
        BigDecimal dt3 = dt.multiply(dt).multiply(dt).divide(BigDecimal.valueOf(6), MC);
        BigDecimal dt4 = dt.multiply(dt).multiply(dt).multiply(dt).divide(BigDecimal.valueOf(24), MC);
        BigDecimal dt5 = dt.multiply(dt).multiply(dt).multiply(dt).multiply(dt).divide(BigDecimal.valueOf(120), MC);

        // Predict
        pred[0] = r[0].add(dt1.multiply(r[1], MC))
                     .add(dt2.multiply(r[2], MC))
                     .add(dt3.multiply(r[3], MC))
                     .add(dt4.multiply(r[4], MC))
                     .add(dt5.multiply(r[5], MC));
        pred[1] = r[1].add(dt1.multiply(r[2], MC))
                     .add(dt2.multiply(r[3], MC))
                     .add(dt3.multiply(r[4], MC))
                     .add(dt4.multiply(r[5], MC));
        pred[2] = r[2].add(dt1.multiply(r[3], MC))
                     .add(dt2.multiply(r[4], MC))
                     .add(dt3.multiply(r[5], MC));
        pred[3] = r[3].add(dt1.multiply(r[4], MC))
                     .add(dt2.multiply(r[5], MC));
        pred[4] = r[4].add(dt1.multiply(r[5], MC));
        pred[5] = r[5];

        BigDecimal aReal = osc.acceleration(pred[0], pred[1]);
        BigDecimal deltaA = aReal.subtract(pred[2]);
        BigDecimal deltaR2 = deltaA.multiply(dt).multiply(dt).divide(BigDecimal.valueOf(2), MC);

        // Correction coefficients
        BigDecimal[] alpha = {
            BigDecimal.valueOf(3.0).divide(BigDecimal.valueOf(16), MC),
            BigDecimal.valueOf(251.0).divide(BigDecimal.valueOf(360), MC),
            BigDecimal.ONE,
            BigDecimal.valueOf(11.0).divide(BigDecimal.valueOf(18), MC),
            BigDecimal.valueOf(1.0).divide(BigDecimal.valueOf(6), MC),
            BigDecimal.valueOf(1.0).divide(BigDecimal.valueOf(60), MC)
        };

        for (int i = 0; i <= 5; i++) {
            BigDecimal factor = BigDecimal.ONE.divide(dt, MC).pow(i);
            r[i] = pred[i].add(alpha[i].multiply(deltaR2, MC).multiply(factor, MC));
        }

        return new BigDecimal[]{r[0], r[1]};
    }

    public static interface CoupledIntegrator {
        void initialize(CoupledOscillators osc, BigDecimal dt);
        void step(CoupledOscillators osc, BigDecimal t, BigDecimal dt);
    }
}
