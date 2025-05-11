package ar.edu.itba.ss;

import java.math.BigDecimal;
import java.math.MathContext;
import java.math.RoundingMode;

public class Config {
    private static final MathContext MC = new MathContext(20, RoundingMode.HALF_UP);

    // Simulation parameters
    static final BigDecimal DT = new BigDecimal("1e-5");
    static final BigDecimal T_MAX = new BigDecimal("5");
    static final String OUTPUT_DIR = "results";

    // Single oscillator parameters
    static final BigDecimal M = new BigDecimal("70.0");
    static final BigDecimal K = new BigDecimal("1e4");
    static final BigDecimal GAMMA = new BigDecimal("100.0");
    static final BigDecimal X0 = new BigDecimal("1.0");
    static final BigDecimal V0 = X0.multiply(GAMMA).divide(M.multiply(BigDecimal.valueOf(2)), MC).negate();

    // Coupled oscillators parameters
    static final int N = 100;
    static final BigDecimal M2 = new BigDecimal("0.00021");
    static final BigDecimal GAMMA2 = new BigDecimal("0.0003");
    static final BigDecimal A2 = new BigDecimal("1e-2");
    static final BigDecimal DT2 = new BigDecimal("1e-4");
    static final BigDecimal T_MAX2 = new BigDecimal("300.0");
}