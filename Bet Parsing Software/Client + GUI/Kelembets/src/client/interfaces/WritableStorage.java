package client.interfaces;

import java.util.Set;

/**
 * Reads and Writes bets from file.
 */
public interface WritableStorage<T> extends Storage {
    /**
     * Writes many Bet objects into the storage (file).
     * @param bets Set of new bets
     */
    void write(Set<T> bets);

    /**
     * Writes Bet object into the storage (file).
     * @param elem Set of new elems
     */
    void write(T elem);
}
