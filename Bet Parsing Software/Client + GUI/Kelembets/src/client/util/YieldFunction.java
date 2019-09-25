package client.util;

import client.interfaces.Fork;

import java.util.List;

/**
 * Implements yield functions
 */
public class YieldFunction {

    public static Double average(Fork fork) {
        List<Double> yields = fork.getYields();
        double sum = 0;

        for (Double d : yields) {
            sum += d;
        }

        return sum / yields.size();
    }

    public static Double averageVariance(Fork fork) {
        List<Double> yields = fork.getYields();
        double sum = 0;

        for (Double d : yields) {
            sum += d;
        }

        sum = sum / yields.size();

        double res = 0;

        for (Double d : yields) {
            res += (d - sum) * (d - sum);
        }

        return res / yields.size();
    }

    public static Double weightedAverage(Fork fork) {
        List<Double> yields = fork.getYields();
        List<Double> probabilities = fork.getProbabilities();
        double sum = 0;

        for (int i = 0; i < yields.size(); i++) {
            sum += yields.get(i) * probabilities.get(i);
        }

        return sum;
    }

    public static Double weightedAverageVariance(Fork fork) {
        List<Double> yields = fork.getYields();
        List<Double> probabilities = fork.getProbabilities();
        double sum = 0;

        for (int i = 0; i < yields.size(); i++) {
            sum += yields.get(i) * probabilities.get(i);
        }

        double res = 0;
        for (int i = 0; i < yields.size(); i++) {
            res += (yields.get(i) - sum) * (yields.get(i) - sum);
        }

        return res / yields.size();
    }



    public static Double minimum(Fork fork) {
        List<Double> yields = fork.getYields();

        double min = yields.get(0);

        for (Double d : yields) {
            min = min > d ? d : min;
        }

        return min;
    }

}
