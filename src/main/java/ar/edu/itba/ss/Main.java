package ar.edu.itba.ss;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.text.DecimalFormat;
import java.text.DecimalFormatSymbols;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

import ar.edu.itba.ss.integrators.BeemanIntegrator;
import ar.edu.itba.ss.integrators.Gear5Integrator;
import ar.edu.itba.ss.integrators.VerletCoupledIntegrator;
import ar.edu.itba.ss.integrators.VerletIntegrator;

public class Main {

    public static void main(String[] args) {
        try {
            String outputDir = Config.OUTPUT_DIR;
            double dt = Config.DT;
            double tMax = Config.T_MAX;
            double dt2 = Config.DT2;
            double tMax2 = Config.T_MAX2;

            // Create base output directory
            Files.createDirectories(Paths.get(outputDir));

            if (args[0].equals("1")) {
                try {
                    dt = Double.parseDouble(args[1]);
                } catch (NumberFormatException e) {
                    System.out.println("El segundo argumento debe ser un número válido para dt. Usando dt default: " + dt);
                }

                String timestamp = new SimpleDateFormat("yyyy-MM-dd_HH-mm-ss").format(new Date());
                String directory = String.format(Locale.US, "%s/ej1/%s", outputDir, timestamp);
                Files.createDirectories(Paths.get(directory));

                Oscillator osc = new Oscillator(Config.M, Config.K, Config.GAMMA, Config.X0, Config.V0);
                new Simulation(osc, dt, tMax, new VerletIntegrator(), directory + "/output_verlet.txt").run();
                new Simulation(osc, dt, tMax, new BeemanIntegrator(), directory + "/output_beeman.txt").run();
                new Simulation(osc, dt, tMax, new Gear5Integrator(), directory + "/output_gear.txt").run();
                System.out.println("Termine el 1");

                // Save single oscillator config
                saveSingleOscillatorConfig(directory, dt, tMax);
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

                DecimalFormat df = new DecimalFormat("0000.0000", new DecimalFormatSymbols(Locale.US));
                String directory = outputDir + "/ej2";
                Files.createDirectories(Paths.get(directory));
                String filename = directory + "/coupled_omega_" + df.format(omega) + "_k_" + df.format(k) + ".txt";

                CoupledOscillators coupledOsc = new CoupledOscillators(Config.N, Config.M2, k, Config.GAMMA2, Config.A2,
                        omega);
                new SimulationCoupled(coupledOsc, dt2, tMax2, new VerletCoupledIntegrator(), filename).run();

                // Save coupled oscillators config
                saveCoupledOscillatorsConfig(directory, dt2, tMax2, k, omega);
            } else {
                System.out.println("Argumento invalido. Use 1 para el primer ejercicio y 2 para el segundo.");
            }
        } catch (Exception e) {
            System.err.println("Error creating directories: " + e.getMessage());
            e.printStackTrace();
        }
    }

    private static void saveSingleOscillatorConfig(String outputDir, double dt, double tMax) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(outputDir + "/config.json"))) {
            writer.write("{\n");
            writer.write("  \"oscillatorType\": \"single\",\n");
            writer.write("  \"simulation\": {\n");
            writer.write("    \"dt\": " + dt + ",\n");
            writer.write("    \"tMax\": " + tMax + "\n");
            writer.write("  },\n");
            writer.write("  \"parameters\": {\n");
            writer.write("    \"m\": " + Config.M + ",\n");
            writer.write("    \"k\": " + Config.K + ",\n");
            writer.write("    \"gamma\": " + Config.GAMMA + ",\n");
            writer.write("    \"x0\": " + Config.X0 + ",\n");
            writer.write("    \"v0\": " + Config.V0 + "\n");
            writer.write("  }\n");
            writer.write("}\n");
        } catch (IOException e) {
            System.err.println("Error saving configuration: " + e.getMessage());
        }
    }

    private static void saveCoupledOscillatorsConfig(String outputDir, double dt, double tMax, double k, double omega) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(outputDir + "/config.json"))) {
            writer.write("{\n");
            writer.write("  \"oscillatorType\": \"coupled\",\n");
            writer.write("  \"simulation\": {\n");
            writer.write("    \"dt\": " + dt + ",\n");
            writer.write("    \"tMax\": " + tMax + "\n");
            writer.write("  },\n");
            writer.write("  \"parameters\": {\n");
            writer.write("    \"N\": " + Config.N + ",\n");
            writer.write("    \"m\": " + Config.M2 + ",\n");
            writer.write("    \"k\": " + k + ",\n");
            writer.write("    \"gamma\": " + Config.GAMMA2 + ",\n");
            writer.write("    \"A\": " + Config.A2 + ",\n");
            writer.write("    \"omega\": " + omega + "\n");
            writer.write("  }\n");
            writer.write("}\n");
        } catch (IOException e) {
            System.err.println("Error saving configuration: " + e.getMessage());
        }
    }
}
