package ar.edu.itba.ss;

public class Config {

    // Simulation parameters
    static final double DT = 0.01;
    static final double T_MAX = 5;
    static final String OUTPUT_DIR = "results";

    // Single oscillator parameters
    static final double M = 70.0;
    static final double K = 1e4;
    static final double GAMMA = 100.0;
    static final double X0 = 1.0;
    static final double V0 = -X0 * GAMMA / (2 * M);

    // Coupled oscillators parameters
    static final int N = 1000;
    static final double M2 = 0.00021;
    static final double GAMMA2 = 0.0003;
    static final double A2 = 1e-2;
    static final double DT2 = 1e-4;
    static final double T_MAX2 = 300.0;

}