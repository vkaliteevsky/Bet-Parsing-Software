package client.impl;

import client.enums.Bookmaker;
import client.enums.FilterCategory;
import client.enums.YieldType;
import client.interfaces.Filter;
import client.interfaces.Fork;
import client.util.YieldFunction;

import java.util.*;
import java.util.function.Function;

/**
 * Implementation of Filter interface.
 */
public class DefaultFilter implements Filter<Object[]> {
    private final FilterCategory filterCategory;
    private Object[] filterItems;
    private Class filterItemsClass;
    private int filterItemsCapacity;
    private static Function<Fork, Double> yieldFilterFunction = YieldFunction::weightedAverage;

    public DefaultFilter(FilterCategory filterCategory, Object[] filterItems) {
        this.filterCategory = filterCategory;
        this.filterItems = filterItems;
        this.filterItemsCapacity = (filterItems != null) ? filterItems.length : 0;

        switch (this.filterCategory) {
            case REQUIRED_BOOKMAKERS:
            case HIDDEN_BOOKMAKERS:
                this.filterItemsClass = Bookmaker.class;
                break;
            case OUTCOMES_NUMBER:
                this.filterItemsClass = Integer.class;
                break;
            case TIME:
                this.filterItemsClass = Long.class;
                break;
            case HIDE_FORKS_WITH_HIGH_COEFFICIENTS:
                this.filterItemsClass = Double.class;
                break;
            case YIELD_TYPE:
                yieldFilterFunction = (filterItems != null ? ((YieldType) filterItems[0]).getFunction() : YieldFunction::weightedAverage);
                break;
            default:
                this.filterItemsClass = null;
                break;
        }
    }

    public void setFilterItems(Object[] filterItems) {
        this.filterItems = filterItems;
        this.filterItemsCapacity = (filterItems != null) ? filterItems.length : 0;
    }

    public Object[] getFilterItems() {
        return this.filterItems;
    }

    public FilterCategory getFilterCategory() {
        return filterCategory;
    }

    public int getFilterItemsCapacity() {
        return this.filterItemsCapacity;
    }

    public Class getFilterItemsClass() {
        return this.filterItemsClass;
    }

    public static void setYieldFunction(Function<Fork, Double> function) {
        yieldFilterFunction = function;
    }

    public static Function<Fork, Double> getYieldFunction() {
        return yieldFilterFunction;
    }

    public void accept(Set<Fork> filteredForks) {
        switch (filterCategory) {
            case REQUIRED_BOOKMAKERS:
                applyRequiredBookmakersFilter(filteredForks);
                break;
            case HIDDEN_BOOKMAKERS:
                applyHiddenBookmakersFilter(filteredForks);
                break;
            case HIDE_FORKS_WITH_RETURN:
                applyHideForksWithReturnFilter(filteredForks);
                break;
            case DIFFERENT_BOOKMAKERS:
                applyDifferentBookmakers(filteredForks);
                break;
            case OUTCOMES_NUMBER:
                applyOutcomesNumber(filteredForks);
                break;
            case TIME:
                applyTime(filteredForks);
                break;
            case HIDE_FORKS_WITH_HIGH_COEFFICIENTS:
                applyHideForksWithHighCoefficients(filteredForks);
                break;
            case YIELD_TYPE:
                applyYieldType();
                break;
            default:
                break;
        }
    }

    private void applyRequiredBookmakersFilter(Set<Fork> filteredForks) {
        if (filterItemsCapacity != 0) {
            HashSet<Fork> copyFilteredForks = new HashSet<>();
            copyFilteredForks.addAll(filteredForks);

            ArrayList<Bookmaker> requiredBookmakers = new ArrayList<>();
            Collections.addAll(requiredBookmakers, (Bookmaker[]) filterItems);
            copyFilteredForks.stream().filter(f -> !f.getBookmakers().containsAll(requiredBookmakers))
                    .forEach(filteredForks::remove);
        }
    }

    private void applyHiddenBookmakersFilter(Set<Fork> filteredForks) {
        if (filterItemsCapacity != 0) {
            HashSet<Fork> copyFilteredForks = new HashSet<>();
            copyFilteredForks.addAll(filteredForks);

            ArrayList<Bookmaker> hiddenBookmakers = new ArrayList<>();
            Collections.addAll(hiddenBookmakers, (Bookmaker[]) filterItems);

            for (Fork f : copyFilteredForks) {
                for (Bookmaker b : hiddenBookmakers) {
                    if (f.getBookmakers().contains(b)) {
                        filteredForks.remove(f);
                        break;
                    }
                }
            }
        }
    }

    private void applyHideForksWithReturnFilter(Set<Fork> filteredForks) {
        HashSet<Fork> copyFilteredForks = new HashSet<>();
        copyFilteredForks.addAll(filteredForks);
        copyFilteredForks.stream().filter(f -> yieldFilterFunction.apply(f) <= 0)
                .forEach(filteredForks::remove);
    }

    private void applyDifferentBookmakers(Set<Fork> filteredForks) {
        HashSet<Fork> copyFilteredForks = new HashSet<>();
        copyFilteredForks.addAll(filteredForks);
        for (Fork f : copyFilteredForks) {
            Set<Bookmaker> bookmakers = new HashSet<>();
            for (Bookmaker b : f.getBookmakers()) {
                if (bookmakers.contains(b)) {
                    filteredForks.remove(f);
                    break;
                }
                bookmakers.add(b);
            }
        }
    }

    private void applyOutcomesNumber(Set<Fork> filteredForks) {
        if (filterItemsCapacity != 0) {
            HashSet<Fork> copyFilteredForks = new HashSet<>();
            copyFilteredForks.addAll(filteredForks);

            ArrayList<Integer> outcomes = new ArrayList<>();
            Collections.addAll(outcomes, (Integer[]) filterItems);

            copyFilteredForks.stream().filter(f -> !outcomes.contains(f.getOutcomes())).forEach(filteredForks::remove);
        }
    }

    private void applyTime(Set<Fork> filteredForks) {
        if (filterItemsCapacity == 3) {
            HashSet<Fork> copyFilteredForks = new HashSet<>();
            copyFilteredForks.addAll(filteredForks);

            Long days = (Long) filterItems[0];
            Long hours = (Long) filterItems[1];
            Long minutes = (Long) filterItems[2];
            Long milliseconds = 1000L * (days * 24 * 60 * 60 + hours * 60 * 60 + minutes * 60);
            Date tillDate = new Date(new Date().getTime() + milliseconds);

            copyFilteredForks.stream().filter(f -> f.getDate().getTime() > tillDate.getTime()).forEach(filteredForks::remove);
        } else {
            throw new RuntimeException("DefaultFilter: FilterCategory.TIME: number of filterItems != 3.");
        }
    }

    private void applyHideForksWithHighCoefficients(Set<Fork> filteredForks) {
        if (filterItemsCapacity == 1) {
            HashSet<Fork> copyFilteredForks = new HashSet<>();
            copyFilteredForks.addAll(filteredForks);

            double coeff = (double) filterItems[0];

            for (Fork f : copyFilteredForks) {
                for (Double c : f.getRates()) {
                    if (c > coeff) {
                        filteredForks.remove(f);
                        break;
                    }
                }
            }
        } else {
            throw new RuntimeException("DefaultFilter: FilterCategory.HIDE_FORKS_WITH_HIGH_COEFFICIENTS: number of filterItems != 1.");
        }
    }

    private void applyYieldType() {
        if (filterItemsCapacity != 0) {
            yieldFilterFunction = ((YieldType)filterItems[0]).getFunction();
        } else {
            yieldFilterFunction = YieldFunction::weightedAverage;
        }
    }
}
