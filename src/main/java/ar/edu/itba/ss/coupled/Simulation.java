package ar.edu.itba.ss.coupled;

import ar.edu.itba.ss.coupled.integrators.Integrator;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Locale;

public class Simulation {

    private final Oscillator osc;
    private final double dt, tMax;
    private final Integrator integrator;
    private final String outputFile;

    public Simulation(Oscillator osc, double dt, double tMax, Integrator integrator, String outputFile) {
        this.osc = osc;
        this.dt = dt;
        this.tMax = tMax;
        this.integrator = integrator;
        this.outputFile = outputFile;
    }

    public void run() {
        try {
            // Create output directory if it doesn't exist
            Path outputPath = Paths.get(outputFile);
            Files.createDirectories(outputPath.getParent());

            try (PrintWriter writer = new PrintWriter(new FileWriter(outputFile))) {
                osc.initialize();
                integrator.initialize(osc, dt);
                double t = 0.0;

                while (t <= tMax) {
                    double[] pos = osc.getPositions();

                    // Save time and all particle positions
                    writer.printf(Locale.US, "%s", t);
                    for (double po : pos)
                        writer.printf(Locale.US, "\t%s", po);
                    writer.println();

                    integrator.step(osc, t, dt);
                    t += dt;
                }
            }
        } catch (IOException e) {
            System.err.println("Error writing simulation output: " + e.getMessage());
            e.printStackTrace();
        }
    }

}
