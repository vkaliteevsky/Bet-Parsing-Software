package client.interfaces;

import client.enums.FilterCategory;

import java.util.Set;
import java.util.function.Consumer;

/**
 * Interface represents filter.
 */
public interface Filter<T> extends Consumer<Set<Fork>> {

    /**
     * Sets subfilters.
     * @param filterItems
     */
    void setFilterItems(T filterItems);

    /**
     * @return filterItems
     */
    T getFilterItems();

    /**
     * @return FilterCategory
     */
    FilterCategory getFilterCategory();

    /**
     * @return capacity of filter items
     */
    int getFilterItemsCapacity();
}
