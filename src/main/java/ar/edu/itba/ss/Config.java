package ar.edu.itba.ss;

public class Config {

    // Simulation parameters
    public static String OUTPUT_DIR = "results";

    // Single oscillator parameters
    public static double SINGLE_M = 70.0;
    public static double SINGLE_K = 1e4;
    public static double SINGLE_GAMMA = 100.0;
    public static double SINGLE_X0 = 1.0;
    public static double SINGLE_V0 = -SINGLE_X0 * SINGLE_GAMMA / (2 * SINGLE_M);
    public static double SINGLE_DT = 0.01;
    public static double SINGLE_T_MAX = 5.0;

    // Coupled oscillators parameters
    public static int COUPLED_N = 1000;
    public static double COUPLED_M = 0.00021;
    public static double COUPLED_K = 102.3;
    public static double COUPLED_GAMMA = 0.0003;
    public static double COUPLED_A = 0.01;
    public static double COUPLED_L0 = 0.001;
    public static double COUPLED_DT = 1e-4;
    public static double COUPLED_T_MAX = 20.0;
    public static double COUPLED_OMEGA = 2.0 * Math.PI;

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
                        Config.SINGLE_DT = Double.parseDouble(value);
                        Config.COUPLED_DT = Config.SINGLE_DT;
                    } catch (NumberFormatException e) {
                        System.out.println("Invalid value for dt: " + value);
                    }
                    break;

                case "T_MAX":
                    try {
                        Config.SINGLE_T_MAX = Double.parseDouble(value);
                        Config.COUPLED_T_MAX = Config.SINGLE_T_MAX;
                    } catch (NumberFormatException e) {
                        System.out.println("Invalid value for tMax: " + value);
                    }
                    break;

                case "M":
                    try {
                        Config.SINGLE_M = Double.parseDouble(value);
                        Config.COUPLED_M = Config.SINGLE_M;
                    } catch (NumberFormatException e) {
                        System.out.println("Invalid value for M: " + value);
                    }
                    break;

                case "K":
                    try {
                        Config.SINGLE_K = Double.parseDouble(value);
                        Config.COUPLED_K = Config.SINGLE_K;
                    } catch (NumberFormatException e) {
                        System.out.println("Invalid value for K: " + value);
                    }
                    break;

                case "GAMMA":
                    try {
                        Config.SINGLE_GAMMA = Double.parseDouble(value);
                        Config.COUPLED_GAMMA = Config.SINGLE_GAMMA;
                    } catch (NumberFormatException e) {
                        System.out.println("Invalid value for gamma: " + value);
                    }
                    break;

                case "X0":
                    try {
                        Config.SINGLE_X0 = Double.parseDouble(value);
                    } catch (NumberFormatException e) {
                        System.out.println("Invalid value for x0: " + value);
                    }
                    break;

                case "V0":
                    try {
                        Config.SINGLE_V0 = Double.parseDouble(value);
                    } catch (NumberFormatException e) {
                        System.out.println("Invalid value for v0: " + value);
                    }
                    break;

                case "OMEGA":
                    try {
                        Config.COUPLED_OMEGA = Double.parseDouble(value);
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
