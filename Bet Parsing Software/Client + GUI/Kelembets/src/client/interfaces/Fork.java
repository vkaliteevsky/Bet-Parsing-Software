package client.interfaces;

import client.enums.Bookmaker;
import client.enums.Event;

import java.util.Date;
import java.util.List;

/**
 * Fork interface.
 */
public interface Fork extends Comparable<Fork> {
    /**
     * @return The Number of fork's outcomes
     */
    int getOutcomes();

    /**
     * Current yield of the fork.
     * @return Array of yields
     */
    List<Double> getYields();

    /**
     * Changes the rate of the corresponding event.
     * @param event
     * @param rate
     */
    void changeOdd(int event, double rate);

    /**
     * @return The first team name.
     */
    String getFirstTeam();

    /**
     * @return The second team name.
     */
    String getSecondTeam();

    /**
     * @return The match date and time.
     */
    Date getDate();

    /**
     * @return The array of fork events.
     */
    List<Event> getEvents();

    /**
     * @return The array of fork rates.
     */
    List<Double> getRates();

    /**
     * @return The array of fork bookmakers.
     */
    List<Bookmaker> getBookmakers();

    /**
     * @return The array of probabilities.
     */
    List<Double> getProbabilities();
}
