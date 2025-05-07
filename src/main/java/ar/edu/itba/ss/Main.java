package ar.edu.itba.ss;

import java.io.File;
import java.text.DecimalFormat;
import java.text.DecimalFormatSymbols;
import java.util.Locale;

import ar.edu.itba.ss.integrators.BeemanIntegrator;
import ar.edu.itba.ss.integrators.Gear5Integrator;
import ar.edu.itba.ss.integrators.VerletCoupledIntegrator;
import ar.edu.itba.ss.integrators.VerletIntegrator;

public class Main {

    public static void main(String[] args) {
        if (args[0].equals("1")) {
            double m = 70.0;
            double k = 1e4;
            double gamma = 100;
            double A = 1.0; // amplitud inicial
            double x0 = A;
            double v0 = (-A * gamma) / (2 * m); // según el modelo analítico

            Oscillator osc = new Oscillator(m, k, gamma, x0, v0);
            double dt = 0.01;
            try {
                dt = Double.parseDouble(args[1]);
            } catch (NumberFormatException e) {
                System.out.println("El segundo argumento debe ser un número válido para dt. dt default: 0.01");
            }
            double tMax = 5.0;
            DecimalFormat df = new DecimalFormat("#.############", new DecimalFormatSymbols(Locale.US));
            String directory = "results/" + df.format(dt) + "/";
            File dir = new File(directory);
            if (!dir.exists())
                dir.mkdirs();

            new Simulation(osc, dt, tMax, new VerletIntegrator(), directory + "output_verlet.txt").run();
            new Simulation(osc, dt, tMax, new BeemanIntegrator(), directory + "output_beeman.txt").run();
            new Simulation(osc, dt, tMax, new Gear5Integrator(), directory + "output_gear.txt").run();
            System.out.println("Termine el 1");
        } else if (args[0].equals("2")) {
            if (args.length < 3) {
                System.out.println("Falta el segundo argumento: omega. Ej: java Main 2 2.5 1e4");
                return;
            }

            double omega;
            double k;
            try {
                omega = Double.parseDouble(args[1]);
                k = Double.parseDouble(args[2]);
            } catch (NumberFormatException e) {
                System.out.println("El segundo argumento debe ser un número válido para omega.");
                return;
            }

            int N = 1000;
            double m2 = 0.00021;
            double gamma2 = 0.0003;
            double A2 = 1e-2;
            double dt = 1e-4;
            double tMax = 300.0;

            DecimalFormat df = new DecimalFormat("0000.0000", new DecimalFormatSymbols(Locale.US));
            String directory = "results/ej2/";
            File dir = new File(directory);
            if (!dir.exists())
                dir.mkdirs();
            String filename = directory + "coupled_omega_" + df.format(omega) + "_k_" + df.format(k) + ".txt";
            CoupledOscillators coupledOsc = new CoupledOscillators(N, m2, k, gamma2, A2, omega);
            new SimulationCoupled(coupledOsc, dt, tMax, new VerletCoupledIntegrator(), filename).run();

        } else {
            System.out.println("Argumento invalido. Use 1 para el primer ejercicio y 2 para el segundo.");
        }
    }

}
