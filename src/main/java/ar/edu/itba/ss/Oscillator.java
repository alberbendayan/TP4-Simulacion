package ar.edu.itba.ss;

public class Oscillator {

    public final double m, k, gamma;
    public final double x0, v0;

    public Oscillator(double m, double k, double gamma, double x0, double v0) {
        this.m = m;
        this.k = k;
        this.gamma = gamma;
        this.x0 = x0;
        this.v0 = v0;
    }

    public double acceleration(double x, double v) {
        return (-k * x - gamma * v) / m;
    }

    public double analytical(double t) {
        double omega0 = Math.sqrt(k / m);
        double gamma_m = gamma / (2 * m);
        double omega_d = Math.sqrt(omega0 * omega0 - gamma_m * gamma_m);
        return Math.exp(-gamma_m * t) * (x0 * Math.cos(omega_d * t) +
                (v0 + gamma_m * x0) / omega_d * Math.sin(omega_d * t));
    }

    public double jerk(double x, double v) {
        double a = acceleration(x, v);
        return (-k * v - gamma * a) / m;
    }

    public double snap(double x, double v) {
        double a = acceleration(x, v);
        double j = jerk(x, v);
        return (-k * a - gamma * j) / m;
    }

    public double crackle(double x, double v) {
        double j = jerk(x, v);
        double s = snap(x, v);
        return (-k * j - gamma * s) / m;
    }
}
