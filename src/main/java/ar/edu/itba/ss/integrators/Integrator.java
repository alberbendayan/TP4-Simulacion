package ar.edu.itba.ss.integrators;

import ar.edu.itba.ss.Oscillator;
import java.math.BigDecimal;

public interface Integrator {

    void initialize(Oscillator osc, BigDecimal x, BigDecimal v, BigDecimal dt);
    BigDecimal[] step(BigDecimal x, BigDecimal v, BigDecimal t);

}
