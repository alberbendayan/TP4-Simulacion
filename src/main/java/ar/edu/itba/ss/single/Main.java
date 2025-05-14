package ar.edu.itba.ss.single;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;

import ar.edu.itba.ss.Config;
import ar.edu.itba.ss.single.integrators.BeemanIntegrator;
import ar.edu.itba.ss.single.integrators.Gear5Integrator;
import ar.edu.itba.ss.single.integrators.VerletIntegrator;

public class Main {

    public static void main(String[] args) {
        Config.parseArguments(args);

        double dt = Config.DT;
        double tMax = Config.T_MAX;
        double m = Config.M;
        double k = Config.K;
        double gamma = Config.GAMMA;
        double x0 = Config.X0;
        double v0 = Config.V0;

        String timestamp = new SimpleDateFormat("yyyy-MM-dd_HH-mm-ss").format(new Date());
        String outputDir = String.format("%s/ej1/%s", Config.OUTPUT_DIR, timestamp);

        // Create base output directory
        File file = new File(outputDir);
        if (!file.exists() && !file.mkdirs()) {
            System.out.println("Error creating output directory: " + outputDir);
            System.exit(1);
        }

        saveConfig(outputDir, dt, tMax);

        Oscillator osc = new Oscillator(m, k, gamma, x0, v0);
        new Simulation(osc, dt, tMax, new VerletIntegrator(), String.format("%s/output_verlet.txt", outputDir)).run();
        new Simulation(osc, dt, tMax, new BeemanIntegrator(), String.format("%s/output_beeman.txt", outputDir)).run();
        new Simulation(osc, dt, tMax, new Gear5Integrator(), String.format("%s/output_gear.txt", outputDir)).run();
    }

    public static void saveConfig(String outputDir, double dt, double tMax) {
        String fileName = String.format("%s/config.json", outputDir);
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(fileName))) {
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

}
