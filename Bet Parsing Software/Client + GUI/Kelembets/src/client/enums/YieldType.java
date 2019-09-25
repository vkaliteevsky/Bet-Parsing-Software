package client.enums;

import client.interfaces.Fork;
import client.util.YieldFunction;

import java.util.function.Function;

/**
 * Enum of yield types (and corresponding functions).
 */
public enum YieldType {
    AVERAGE("Average", YieldFunction::average),
    AVERAGE_VARIANCE("Average variance", YieldFunction::averageVariance),
    WEIGHTED_AVERAGE("W. Average", YieldFunction::weightedAverage),
    WEIGHTED_AVERAGE_VARIANCE("W. average variance", YieldFunction::weightedAverageVariance),
    MINIMUM("Minimum", YieldFunction::minimum);

    private final Function<Fork, Double> function;
    private final String humanName;

    private YieldType(String humanName, Function<Fork, Double> func) {
        this.humanName = humanName;
        this.function = func;
    }

    public Double apply(Fork fork) {
        return function.apply(fork);
    }

    public Function<Fork, Double> getFunction() {
        return function;
    }

    @Override
    public String toString() {
        return humanName;
    }
}
