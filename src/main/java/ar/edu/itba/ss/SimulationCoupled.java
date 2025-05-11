package ar.edu.itba.ss;

import ar.edu.itba.ss.integrators.CoupledIntegrator;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.math.BigDecimal;
import java.math.MathContext;
import java.math.RoundingMode;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Locale;

public class SimulationCoupled {
    private static final MathContext MC = new MathContext(20, RoundingMode.HALF_UP);

    private final CoupledOscillators osc;
    private final BigDecimal dt, tMax;
    private final CoupledIntegrator integrator;
    private final String outputFile;
    private final boolean saveAll;

    public SimulationCoupled(CoupledOscillators osc, BigDecimal dt, BigDecimal tMax, CoupledIntegrator integrator,
            String outputFile, boolean saveAll) {
        this.osc = osc;
        this.dt = dt;
        this.tMax = tMax;
        this.integrator = integrator;
        this.outputFile = outputFile;
        this.saveAll = saveAll;
    }

    public void run() {
        try {
            // Create output directory if it doesn't exist
            Path outputPath = Paths.get(outputFile);
            Files.createDirectories(outputPath.getParent());

            try (PrintWriter writer = new PrintWriter(new FileWriter(outputFile))) {
                osc.initialize();
                integrator.initialize(osc, dt);
                BigDecimal t = BigDecimal.ZERO;

                while (t.compareTo(tMax) <= 0) {
                    BigDecimal[] pos = osc.getPositions();
                    BigDecimal[] vel = osc.getVelocities();
                    if (saveAll) {
                        // Save time and all particle positions
                        writer.printf(Locale.US, "%.8f", t.doubleValue());
                        for (int i = 0; i < pos.length; i++) {
                            writer.printf(Locale.US, "\t%.8f", pos[i].doubleValue());
                        }
                        writer.println();
                    } else {
                        // Save only time and last particle position
                        writer.printf(Locale.US, "%.8f\t%.8f\t%.8f%n", 
                            t.doubleValue(), 
                            pos[pos.length - 1].doubleValue(), 
                            vel[pos.length - 1].doubleValue());
                    }
                    integrator.step(osc, t, dt);
                    t = t.add(dt);
                }
            }
        } catch (IOException e) {
            System.err.println("Error writing simulation output: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
