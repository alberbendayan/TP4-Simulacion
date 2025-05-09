package ar.edu.itba.ss;

import ar.edu.itba.ss.integrators.CoupledIntegrator;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Locale;

public class SimulationCoupled {

    private final CoupledOscillators osc;
    private final double dt, tMax;
    private final CoupledIntegrator integrator;
    private final String outputFile;

    public SimulationCoupled(CoupledOscillators osc, double dt, double tMax, CoupledIntegrator integrator, String outputFile) {
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
                    double[] vel = osc.getVelocities();
                    // Guardamos la posición y velocidad de una partícula central (por ejemplo, i=500)
                    writer.printf(Locale.US, "%.8f\t%.8f\t%.8f%n", t, pos[999], vel[999]);
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
