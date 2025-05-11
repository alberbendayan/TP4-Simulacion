package ar.edu.itba.ss;

import ar.edu.itba.ss.integrators.Integrator;
import java.io.*;
import java.math.BigDecimal;
import java.math.MathContext;
import java.math.RoundingMode;
import java.util.Locale;

public class Simulation {
    private static final MathContext MC = new MathContext(20, RoundingMode.HALF_UP);

    private final Oscillator osc;
    private final BigDecimal dt, tMax;
    private final Integrator integrator;
    private final String outputFile;

    public Simulation(Oscillator osc, BigDecimal dt, BigDecimal tMax, Integrator integrator, String outputFile) {
        this.osc = osc;
        this.dt = dt;
        this.tMax = tMax;
        this.integrator = integrator;
        this.outputFile = outputFile;
    }

    public void run() {
        try {
            try (PrintWriter writer = new PrintWriter(new FileWriter(outputFile))) {
                BigDecimal x = osc.x0;
                BigDecimal v = osc.v0;
                BigDecimal t = BigDecimal.ZERO;

                integrator.initialize(osc, x, v, dt);

                while (t.compareTo(tMax) <= 0) {
                    BigDecimal analytical = osc.analytical(t);
                    writer.printf(Locale.US,"%s\t%s\t%s\t%s%n", 
                        t.toString(), x.toString(), v.toString(), analytical.toString());
                    BigDecimal[] next = integrator.step(x, v, t);
                    x = next[0];
                    v = next[1];
                    t = t.add(dt);
                }
            }
        } catch (IOException e) {
            System.err.println("Error writing simulation output: " + e.getMessage());
            e.printStackTrace();
        }
    }

}

