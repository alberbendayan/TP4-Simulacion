package ar.edu.itba.ss.coupled;

import ar.edu.itba.ss.Config;
import ar.edu.itba.ss.coupled.integrators.VerletIntegrator;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class Main {

    public static void main(String[] args) {
        Config.parseArguments(args);

        int n = Config.COUPLED_N;
        double m = Config.COUPLED_M;
        double k = Config.COUPLED_K;
        double gamma = Config.COUPLED_GAMMA;
        double a = Config.COUPLED_A;
        double omega = Config.COUPLED_OMEGA;

        double dt = Config.COUPLED_DT;
        double tMax = Config.COUPLED_T_MAX;

        String timestamp = new SimpleDateFormat("yyyy-MM-dd_HH-mm-ss").format(new Date());
        String outputDir = String.format("%s/ej2/%s", Config.OUTPUT_DIR, timestamp);

        // Create base output directory
        File file = new File(outputDir);
        if (!file.exists() && !file.mkdirs()) {
            System.out.println("Error creating output directory: " + outputDir);
            System.exit(1);
        }

        saveConfig(outputDir, dt, tMax, k, omega);

        String fileName = String.format("%s/output.txt", outputDir);
        Oscillator osc = new Oscillator(n, m, k, gamma, a, omega);
        new Simulation(osc, dt, tMax, new VerletIntegrator(), fileName).run();
    }

    private static void saveConfig(String outputDir, double dt, double tMax, double k, double omega) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(outputDir + "/config.json"))) {
            writer.write("{\n");
            writer.write("  \"oscillatorType\": \"coupled\",\n");
            writer.write("  \"simulation\": {\n");
            writer.write("    \"dt\": " + dt + ",\n");
            writer.write("    \"tMax\": " + tMax + "\n");
            writer.write("  },\n");
            writer.write("  \"parameters\": {\n");
            writer.write("    \"N\": " + Config.COUPLED_N + ",\n");
            writer.write("    \"m\": " + Config.COUPLED_M + ",\n");
            writer.write("    \"k\": " + k + ",\n");
            writer.write("    \"gamma\": " + Config.COUPLED_GAMMA + ",\n");
            writer.write("    \"A\": " + Config.COUPLED_A + ",\n");
            writer.write("    \"omega\": " + omega + "\n");
            writer.write("  }\n");
            writer.write("}\n");
        } catch (IOException e) {
            System.err.println("Error saving configuration: " + e.getMessage());
        }
    }

}
