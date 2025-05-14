package ar.edu.itba.ss.coupled;

import ar.edu.itba.ss.Config;
import ar.edu.itba.ss.coupled.integrators.VerletCoupledIntegrator;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class Main {

    public static void main(String[] args) {
        Config.parseArguments(args);

        int n = Config.N;
        double m = Config.M2;
        double k = Config.K;
        double gamma = Config.GAMMA2;
        double a = Config.A2;
        double omega = Config.OMEGA;

        double dt = Config.DT2;
        double tMax = Config.T_MAX2;

        String timestamp = new SimpleDateFormat("yyyy-MM-dd_HH-mm-ss").format(new Date());
        String outputDir = String.format("%s/ej2/%s", Config.OUTPUT_DIR, timestamp);

        // Create base output directory
        File file = new File(outputDir);
        if (!file.exists() && !file.mkdirs()) {
            System.out.println("Error creating output directory: " + outputDir);
            System.exit(1);
        }

        saveConfig(outputDir, dt, tMax, k, omega);

        String fileName = String.format("%s/coupled_omega_%s_k_%s.txt", outputDir, omega, k);
        CoupledOscillators osc = new CoupledOscillators(n, m, k, gamma, a, omega);
        new SimulationCoupled(osc, dt, tMax, new VerletCoupledIntegrator(), fileName, true).run();
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
