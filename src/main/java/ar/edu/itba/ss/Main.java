package ar.edu.itba.ss;

import ar.edu.itba.ss.integrators.BeemanIntegrator;
import ar.edu.itba.ss.integrators.Gear5Integrator;
import ar.edu.itba.ss.integrators.VerletIntegrator;

import java.io.File;

public class Main {

    public static void main(String[] args) {
        double m = 70.0;
        double k = 10e4;
        double gamma = 100;
        double A = 1.0;  // amplitud inicial
        double x0 = A;
        double v0 = -A * gamma / (2 * m);  // según el modelo analítico

        Oscillator osc = new Oscillator(m, k, gamma, x0, v0);
        double dt = 0.001;
        double tMax = 5.0;

        File dir = new File("results");
        if (!dir.exists())
            dir.mkdirs();

        new Simulation(osc, dt, tMax, new VerletIntegrator(), "results/output_verlet.txt").run();
        new Simulation(osc, dt, tMax, new BeemanIntegrator(), "results/output_beeman.txt").run();
        new Simulation(osc, dt, tMax, new Gear5Integrator(), "results/output_gear.txt").run();
    }

}

