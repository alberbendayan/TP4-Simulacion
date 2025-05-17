package ar.edu.itba.ss;

public class Config {

    // Simulation parameters
    public static String OUTPUT_DIR = "results";
    public static double DT = 0.01;
    public static double T_MAX = 5;

    // Single oscillator parameters
    public static double M = 70.0;
    public static double K = 1e4;
    public static double GAMMA = 100.0;
    public static double X0 = 1.0;
    public static double V0 = -X0 * GAMMA / (2 * M);

    // Coupled oscillators parameters
    public static int N = 1000;
    public static double M2 = 0.00021;  // 0.21g -> kg
    public static double K2 = 102.3;    // kg/s²
    public static double GAMMA2 = 0.0003;  // 0.3g/s -> kg/s
    public static double A2 = 0.01;     // m
    public static double L0 = 0.001;     // m
    public static double DT2 = 1e-4;
    public static double T_MAX2 = 20.0; // s
    public static double OMEGA = 6.0 * Math.PI;   // rad/s

    public static void parseArguments(String[] args) {

        for (String arg : args) {
            String[] parts = arg.split("=");
            if (parts.length != 2) {
                System.out.println("Invalid argument format: " + arg);
                continue;
            }

            String key = parts[0];
            String value = parts[1];

            switch (key) {
                case "DT":
                    try {
                        Config.DT = Double.parseDouble(value);
                    } catch (NumberFormatException e) {
                        System.out.println("Invalid value for dt: " + value);
                    }
                    break;

                case "T_MAX":
                    try {
                        Config.T_MAX = Double.parseDouble(value);
                    } catch (NumberFormatException e) {
                        System.out.println("Invalid value for tMax: " + value);
                    }
                    break;

                case "M":
                    try {
                        Config.M = Double.parseDouble(value);
                    } catch (NumberFormatException e) {
                        System.out.println("Invalid value for M: " + value);
                    }
                    break;

                case "K":
                    try {
                        Config.K = Double.parseDouble(value);
                    } catch (NumberFormatException e) {
                        System.out.println("Invalid value for K: " + value);
                    }
                    break;

                case "GAMMA":
                    try {
                        Config.GAMMA = Double.parseDouble(value);
                    } catch (NumberFormatException e) {
                        System.out.println("Invalid value for gamma: " + value);
                    }
                    break;

                case "X0":
                    try {
                        Config.X0 = Double.parseDouble(value);
                    } catch (NumberFormatException e) {
                        System.out.println("Invalid value for x0: " + value);
                    }
                    break;

                case "V0":
                    try {
                        Config.V0 = Double.parseDouble(value);
                    } catch (NumberFormatException e) {
                        System.out.println("Invalid value for v0: " + value);
                    }
                    break;

                case "OMEGA":
                    try {
                        Config.OMEGA = Double.parseDouble(value);
                    } catch (NumberFormatException e) {
                        System.out.println("Invalid value for omega: " + value);
                    }
                    break;

                default:
                    System.out.println("Unknown argument: " + key);
            }
        }
    }

}
