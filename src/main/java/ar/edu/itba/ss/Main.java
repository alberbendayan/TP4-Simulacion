package ar.edu.itba.ss;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.math.BigDecimal;
import java.math.MathContext;
import java.math.RoundingMode;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

import ar.edu.itba.ss.integrators.BeemanIntegrator;
import ar.edu.itba.ss.integrators.Gear5Integrator;
import ar.edu.itba.ss.integrators.VerletCoupledIntegrator;
import ar.edu.itba.ss.integrators.VerletIntegrator;

public class Main {
    private static final MathContext MC = new MathContext(20, RoundingMode.HALF_UP);

    public static void main(String[] args) {
        try {
            String outputDir = Config.OUTPUT_DIR;
            BigDecimal dt = Config.DT;
            BigDecimal tMax = Config.T_MAX;
            BigDecimal dt2 = Config.DT2;
            BigDecimal tMax2 = Config.T_MAX2;

            // Create base output directory
            Files.createDirectories(Paths.get(outputDir));

            if (args[0].equals("1")) {
                try {
                    dt = new BigDecimal(args[1]);
                } catch (NumberFormatException e) {
                    System.out.println(
                            "El segundo argumento debe ser un número válido para dt. Usando dt default: " + dt);
                }

                String timestamp = new SimpleDateFormat("yyyy-MM-dd_HH-mm-ss").format(new Date());
                String directory = String.format(Locale.US, "%s/ej1/%s", outputDir, timestamp);
                Files.createDirectories(Paths.get(directory));

                Oscillator osc = new Oscillator(
                        Config.M,
                        Config.K,
                        Config.GAMMA,
                        Config.X0,
                        Config.V0);
                new Simulation(osc, dt, tMax, new VerletIntegrator(), directory + "/output_verlet.txt").run();
                new Simulation(osc, dt, tMax, new BeemanIntegrator(), directory + "/output_beeman.txt").run();
                new Simulation(osc, dt, tMax, new Gear5Integrator(), directory + "/output_gear.txt").run();
                System.out.println("Termine el 1");

                // Save single oscillator config
                saveSingleOscillatorConfig(directory, dt, tMax);
            } else if (args[0].equals("2")) {
                if (args.length < 3) {
                    System.out.println("Falta el segundo argumento: omega. Ej: java Main 2 2.5 1e4 [saveAll]");
                    return;
                }

                BigDecimal omega;
                BigDecimal k;
                boolean saveAll = false;
                try {
                    omega = new BigDecimal(args[1]);
                    k = new BigDecimal(args[2]);
                    if (args.length > 3) {
                        saveAll = Boolean.parseBoolean(args[3]);
                    }
                } catch (NumberFormatException e) {
                    System.out.println("El segundo argumento debe ser un número válido para omega.");
                    return;
                }

                String timestamp = new SimpleDateFormat("yyyy-MM-dd_HH-mm-ss").format(new Date());
                String directory = String.format(Locale.US, "%s/ej2/%s", outputDir, timestamp);
                Files.createDirectories(Paths.get(directory));
                String filename = directory + "/coupled_omega_" + String.format(Locale.US, "%.4f", omega.doubleValue())
                        +
                        "_k_" + String.format(Locale.US, "%.4f", k.doubleValue()) + ".txt";

                CoupledOscillators coupledOsc = new CoupledOscillators(
                        Config.N,
                        Config.M2,
                        k,
                        Config.GAMMA2,
                        Config.A2,
                        omega);
                new SimulationCoupled(coupledOsc, dt2, tMax2, new VerletCoupledIntegrator(), filename, saveAll).run();

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

    private static void saveSingleOscillatorConfig(String outputDir, BigDecimal dt, BigDecimal tMax) {
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

    private static void saveCoupledOscillatorsConfig(String outputDir, BigDecimal dt, BigDecimal tMax, BigDecimal k,
            BigDecimal omega) {
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
