package ar.edu.itba.ss.integrators;
import ar.edu.itba.ss.CoupledOscillators;
import java.math.BigDecimal;

public interface CoupledIntegrator {
    void initialize(CoupledOscillators osc, BigDecimal dt);
    void step(CoupledOscillators osc, BigDecimal t, BigDecimal dt);
}
