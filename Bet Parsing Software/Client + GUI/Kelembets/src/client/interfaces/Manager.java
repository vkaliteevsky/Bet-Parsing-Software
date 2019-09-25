package client.interfaces;

import client.enums.YieldType;

import java.util.Date;
import java.util.List;
import java.util.Set;
import java.util.SortedSet;
import java.util.function.Function;

/**
 * Manages work process. Works with storages, filters
 */
public interface Manager {
    /**
     * @return Array of currently applied filters
     */
    SortedSet<Fork> getFilteredForks();

    /**
     * @return Array of forks with filters applied
     */
    Set<Fork> getAllForks();

    /**
     * Setting all filters.
     * @param allFilters
     */
    void setFilters(List<Filter<Object[]>> allFilters);


    /**
     * Resetting all filters.
     */
    void resetFilters();

    /**
     * Place a fork to done forks storage.
     */
    void markForkAsDone(Fork fork);

    /**
     * Hides given fork.
     * @param fork
     */
    void hideFork(Fork fork);

    /**
     * Hides given match.
     * @param firstTeam
     * @param secondTeam
     * @param date
     */
    void hideMatch(String firstTeam, String secondTeam, Date date);

    /**
     * Restores all hidden forks.
     */
    void restoreHiddenForks();

    /**
     * @param yieldType
     * @return functions which corresponds to the given yield type
     */
    Function<Fork, Double> getYieldFunction(YieldType yieldType);

    /**
     * @param fork
     * @return file name with one fork stored.
     */
    String storeForkInFile(Fork fork);

    /**
     * Removes all forks from storage.
     */
    void clearForksStorage();
}
