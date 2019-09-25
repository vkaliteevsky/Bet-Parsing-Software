package client.impl;

import client.enums.Bookmaker;
import client.enums.Event;
import client.interfaces.Fork;

import java.util.*;

/**
 * Implementation of the Fork interface.
 */
public class DefaultFork implements Fork {
    private final Date date;
    private final String firstTeam;
    private final String secondTeam;
    private final List<Event> events;
    private final List<Bookmaker> bookmakers;
    private final int outcomes;
    private List<Double> rates;
    private List<Double> yields;
    private List<Double> probabilities;

    public DefaultFork(Date date, String firstTeam, String secondTeam,
                       Event[] events, Double[] rates, Bookmaker[] bookmakers,
                       Double[] yields, Double[] probabilities) throws RuntimeException {
        this.date = date;
        this.firstTeam = firstTeam;
        this.secondTeam = secondTeam;
        this.yields = new ArrayList<>();
        Collections.addAll(this.yields, yields);
        this.probabilities = new ArrayList<>();
        Collections.addAll(this.probabilities, probabilities);
        if (check(events.length, rates.length, bookmakers.length)
                && yields.length == probabilities.length) {
            this.events = new ArrayList<>();
            Collections.addAll(this.events, events);
            this.rates = new ArrayList<>();
            Collections.addAll(this.rates, rates);
            this.bookmakers = new ArrayList<>();
            Collections.addAll(this.bookmakers, bookmakers);
            this.outcomes = events.length;
        } else {
            throw new RuntimeException(
                    "The problem is in the Dispatcher's output file: events, rates, bookmakers sizes are not equal.");
        }
    }

    public DefaultFork(String args) throws RuntimeException {
        Scanner scanner = new Scanner(args);
        scanner.useDelimiter("\\|");
        this.date = new Date(Long.parseLong(scanner.next()) * 1000L);
        this.firstTeam = scanner.next();
        this.secondTeam = scanner.next();
        this.events = importEvents(scanner.next());
        this.rates = importRates(scanner.next());
        this.bookmakers = importBookmakers(scanner.next());
        this.yields = importYields(scanner.next());
        this.probabilities = importProbabilities(scanner.next());
        this.outcomes = this.events.size();
        if (!check(events.size(), rates.size(), bookmakers.size())
                || yields.size() != probabilities.size()) {
            throw new RuntimeException(
                    "The problem is in the Dispatcher's output file: events, rates, bookmakers sizes are not equal.");
        }
    }

    public int getOutcomes() {
        return outcomes;
    }

    public List<Double> getYields() {
        return yields;
    }

    public List<Double> getProbabilities() {
        return probabilities;
    }

    public void changeOdd(int event, double rate) {
        this.rates.set(event, rate);
    }

    public String getFirstTeam() {
        return firstTeam;
    }

    public String getSecondTeam() {
        return secondTeam;
    }

    public Date getDate() {
        return this.date;
    }

    public List<Event> getEvents() {
        return events;
    }

    public List<Double> getRates() {
        return rates;
    }

    public List<Bookmaker> getBookmakers() {
        return bookmakers;
    }

    //public ForkBase serialize() {}

    @Override
    public String toString() {
        return String.format(Locale.US, "%d|%s|%s|%s|%s|%s|%s|%s", (date.getTime() / 1000L), firstTeam, secondTeam,
                eventsToString(), ratesToString(), bookmakersToString(), yieldsToString(), probabilitiesToString());
    }

    @Override
    public boolean equals(Object obj) {
        DefaultFork fork = (DefaultFork)obj;
        return fork.hashCode() == this.hashCode();
    }

    @Override
    public int hashCode() {
        int eventsHash = 0;
        int bookmakersHash = 0;

        if (outcomes == 4) {
            eventsHash = 7 * events.get(0).ordinal()
                    + 3 * events.get(1).ordinal()
                    + 13 * events.get(2).ordinal()
                    + 5 * events.get(3).ordinal();
            bookmakersHash = 23 * bookmakers.get(0).ordinal()
                    + 3 * bookmakers.get(1).ordinal()
                    + 29 * bookmakers.get(2).ordinal()
                    + 5 * bookmakers.get(3).ordinal();
        } else if (outcomes == 5) {
            eventsHash = 7 * events.get(0).ordinal()
                    + 3 * events.get(1).ordinal()
                    + 13 * events.get(2).ordinal()
                    + 5 * events.get(3).ordinal()
                    + 31 * events.get(4).ordinal();
            bookmakersHash = 23 * bookmakers.get(0).ordinal()
                    + 3 * bookmakers.get(1).ordinal()
                    + 29 * bookmakers.get(2).ordinal()
                    + 5 * bookmakers.get(3).ordinal()
                    + 7 * bookmakers.get(3).ordinal();
        }

        return 13 * date.hashCode() + 7 * firstTeam.hashCode() + 17 * secondTeam.hashCode()
                + 23 * eventsHash + 5 * bookmakersHash;
    }

    @Override
    public int compareTo(Fork f) {
        DefaultFork fork = (DefaultFork)f;
        int res;
        double difference = -1 * (DefaultFilter.getYieldFunction().apply(this) - DefaultFilter.getYieldFunction().apply(fork));
        if (difference < 0.001) {
            res = -1;
        } else {
            res = (int) Math.signum(-1 * (DefaultFilter.getYieldFunction().apply(this) - DefaultFilter.getYieldFunction().apply(fork)));
        }
        return res;
    }

    private String eventsToString() {
        StringBuilder str = new StringBuilder();
        for (Event e : events) {
            str.append(e.ordinal());
            str.append(",");
        }
        return str.deleteCharAt(str.lastIndexOf(",")).toString();
    }

    private String ratesToString() {
        StringBuilder str = new StringBuilder();
        for (double d : rates) {
            str.append(d);
            str.append(",");
        }
        return str.deleteCharAt(str.lastIndexOf(",")).toString();
    }

    private String bookmakersToString() {
        StringBuilder str = new StringBuilder();
        for (Bookmaker b : bookmakers) {
            str.append(b.ordinal());
            str.append(",");
        }
        return str.deleteCharAt(str.lastIndexOf(",")).toString();
    }

    private String yieldsToString() {
        StringBuilder str = new StringBuilder();
        for (double d : yields) {
            str.append(d);
            str.append(",");
        }
        return str.deleteCharAt(str.lastIndexOf(",")).toString();
    }

    private String probabilitiesToString() {
        StringBuilder str = new StringBuilder();
        for (double d : probabilities) {
            str.append(d);
            str.append(",");
        }
        return str.deleteCharAt(str.lastIndexOf(",")).toString();
    }

    /**
     * Checks if all input arrays has the same length.
     * @param len1 first length
     * @param len2 second length
     * @param len3 third length
     * @return boolean
     */
    private static boolean check(int len1, int len2, int len3) {
        return (len1 == len2) && (len2 == len3);
    }

    /**
     * Parses string with events' identifiers.
     * @param str input string
     * @return ArrayList<Event> of events
     */
    private ArrayList<Event> importEvents(String str) {
        Scanner scanner = new Scanner(str);
        scanner.useDelimiter(",");
        ArrayList<Event> events = new ArrayList<>();
        while (scanner.hasNext()) {
            events.add(Event.values()[Integer.parseInt(scanner.next())]);
        }
        return events;
    }

    /**
     * Parses string with rates.
     * @param str input string
     * @return ArrayList<Double> of rates
     */
    private ArrayList<Double> importRates(String str) {
        Scanner scanner = new Scanner(str);
        scanner.useDelimiter(",");
        ArrayList<Double> rates = new ArrayList<>();
        while (scanner.hasNext()) {
            rates.add(Double.parseDouble(scanner.next()));
        }
        return rates;
    }

    /**
     * Parses string with bookmakers' identifiers.
     * @param str input string
     * @return ArrayList<Bookmaker> of bookmakers
     */
    private ArrayList<Bookmaker> importBookmakers(String str) {
        Scanner scanner = new Scanner(str);
        scanner.useDelimiter(",");
        ArrayList<Bookmaker> bookmakers = new ArrayList<>();
        while (scanner.hasNext()) {
            bookmakers.add(Bookmaker.values()[Integer.parseInt(scanner.next())]);
        }
        return bookmakers;
    }

    /**
     * Parses string with yields.
     * @param str input string
     * @return ArrayList<Double> of yields
     */
    private ArrayList<Double> importYields(String str) {
        Scanner scanner = new Scanner(str);
        scanner.useDelimiter(",");
        ArrayList<Double> yields = new ArrayList<>();
        while (scanner.hasNext()) {
            yields.add(Double.parseDouble(scanner.next()));
        }
        return yields;
    }

    /**
     * Parses string with probabilities.
     * @param str input string
     * @return ArrayList<Double> of probabilities
     */
    private ArrayList<Double> importProbabilities(String str) {
        Scanner scanner = new Scanner(str);
        scanner.useDelimiter(",");
        ArrayList<Double> probabilities = new ArrayList<>();
        while (scanner.hasNext()) {
            probabilities.add(Double.parseDouble(scanner.next()));
        }
        return probabilities;
    }
}
