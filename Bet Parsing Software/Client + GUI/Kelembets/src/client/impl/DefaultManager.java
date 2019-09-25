package client.impl;

import client.enums.FilterCategory;
import client.enums.YieldType;
import client.interfaces.*;
import client.util.YieldFunction;

import java.util.*;
import java.util.function.Function;

/**
 * Default implementation for Manager interface.
 */
public class DefaultManager implements Manager {
    private static final DefaultManager manager = new DefaultManager();
    private final Storage<Fork> allForksStorage;
    private final WritableStorage<Fork> doneForksStorage;
    private final GenerousFileStorage oneForkStorage;
    private static boolean instantiated = false;
    private Set<Fork> filteredForks;
    private Set<Fork> hiddenForks;
    private List<Filter<Object[]>> filters;

    private DefaultManager() {
        allForksStorage = new FileAllForksStorage();
        doneForksStorage = new FileDoneForksStorage();
        oneForkStorage = new GenerousFileStorage();
        DefaultFilter.setYieldFunction(YieldFunction::weightedAverage);

        // default filtered set is all current forks which have not been done
        filteredForks = new HashSet<>();
        filteredForks.addAll(allForksStorage.getAll());
        filteredForks.removeAll(doneForksStorage.getAll());

        // yield function is a special kind of filter and processes separately
        filters = new ArrayList<>(FilterCategory.values().length);

        //by default there are no hidden forks
        hiddenForks = new HashSet<>();
    }

    public static DefaultManager getInstance() throws InstantiationException {
        if (instantiated) {
            throw new InstantiationError("DefaultManager has already been instantiated.");
        }
        instantiated = true;
        return manager;
    }

    public String storeForkInFile(Fork fork) {
        return oneForkStorage.write(fork);
    }

    public Function<Fork, Double> getYieldFunction(YieldType yieldType) {
        return yieldType.getFunction();
    }

    public void hideFork(Fork fork) {
        filteredForks.remove(fork);
        hiddenForks.add(fork);
    }

    public void hideMatch(String firstTeam, String secondTeam, Date date) {
        HashSet<Fork> copyFilteredSet = new HashSet<>();
        copyFilteredSet.addAll(filteredForks);

        for (Fork f : copyFilteredSet) {
            if (f.getFirstTeam().equals(firstTeam)
                    && f.getSecondTeam().equals(secondTeam)
                    && f.getDate().equals(date)) {
                filteredForks.remove(f);
                hiddenForks.add(f);
            }
        }
    }

    public void restoreHiddenForks() {
        hiddenForks.clear();
        applyAllFilters();
    }

    public void clearForksStorage() {
        allForksStorage.removeAll();
        resetFilters();
    }

    public SortedSet<Fork> getFilteredForks() {
        TreeSet<Fork> sortedFilteredForks = new TreeSet<>((Fork f1, Fork f2) -> f1.compareTo(f2));

        sortedFilteredForks.addAll(filteredForks);
        return sortedFilteredForks;
    }

    public Set<Fork> getAllForks() {
        Set<Fork> allForks = new HashSet<>();
        allForks.addAll(allForksStorage.getAll());
        allForks.removeAll(doneForksStorage.getAll());
        return allForks;
    }

    public void setFilters(List<Filter<Object[]>> allFilters) {
        filters = allFilters;
        applyAllFilters();
    }

    public void resetFilters() {
        // default yield function is weightedAverage yield
        DefaultFilter.setYieldFunction(YieldFunction::weightedAverage);

        // default filtered set is all current forks which have not been done
        filteredForks = new HashSet<>();
        filteredForks.addAll(allForksStorage.getAll());
        filteredForks.removeAll(doneForksStorage.getAll());
        if (hiddenForks.size() > 0) {
            filteredForks.removeAll(hiddenForks);
        }
        filters.clear();
    }

    public void markForkAsDone(Fork fork) {
        if (filteredForks.contains(fork)) {
            filteredForks.remove(fork);
        }
        doneForksStorage.write(fork);
    }

    private void applyAllFilters() {
        filteredForks = new HashSet<>();
        filteredForks.addAll(allForksStorage.getAll());
        filteredForks.removeAll(doneForksStorage.getAll());
        if (hiddenForks.size() > 0) {
            filteredForks.removeAll(hiddenForks);
        }

        for (int i = 0; i < filters.size(); i++) {
            Filter<Object[]> filter = filters.get(i);
            if (filter != null) {
                filter.accept(filteredForks);
            }
        }
    }


}
