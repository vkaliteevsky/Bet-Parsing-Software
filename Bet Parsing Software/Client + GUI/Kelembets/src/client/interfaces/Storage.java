package client.interfaces;

import java.util.Set;

/**
 * Reads bets from file.
 */
public interface Storage<T> {
    /**
     * Reads Bet objects from storage (file).
     * @return Bet
     */
    Set<T> getAll();

    /**
     * Removes all forks from storage
     */
    void removeAll();
}
