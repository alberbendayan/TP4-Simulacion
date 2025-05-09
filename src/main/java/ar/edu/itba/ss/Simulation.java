package ar.edu.itba.ss;

import ar.edu.itba.ss.integrators.Integrator;

import java.io.*;
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
            try (PrintWriter writer = new PrintWriter(new FileWriter(outputFile))) {
                double x = osc.x0;
                double v = osc.v0;
                double t = 0.0;

                integrator.initialize(osc, x, v, dt);

                while (t <= tMax) {
                    double analytical = osc.analytical(t);
                    writer.printf(Locale.US,"%.8f\t%.8f\t%.8f\t%.8f%n", t, x, v, analytical);
                    double[] next = integrator.step(x, v, t);
                    x = next[0];
                    v = next[1];
                    t += dt;
                }
            }
        } catch (IOException e) {
            System.err.println("Error writing simulation output: " + e.getMessage());
            e.printStackTrace();
        }
    }

}

