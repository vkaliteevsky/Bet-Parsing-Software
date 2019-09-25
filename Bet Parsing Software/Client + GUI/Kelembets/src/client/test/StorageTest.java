package client.test;

import client.enums.Bookmaker;
import client.enums.Event;
import client.impl.DefaultFork;
import client.impl.FileDoneForksStorage;
import client.interfaces.Fork;
import client.interfaces.WritableStorage;
import org.junit.Assert;
import org.junit.Test;

import java.util.ArrayList;
import java.util.Date;
import java.util.Set;


/**
 * Tests for all Storage implementations
 */
public class StorageTest {


    @Test
    public static void testDoneForksStorageImpl(){
        ArrayList<Fork> forksTestSet = new ArrayList<>();
        WritableStorage<Fork> doneForksStorage = new FileDoneForksStorage();

        for (int i = 0; i < 5; i++) {
            //initializing date
            Date date = new Date(i * 1000L);

            //initializing events
            Event[] events = new Event[4];
            events[0] = Event.values()[i];
            events[1] = Event.values()[i + i * 10];
            events[2] = Event.values()[i + i * 20];
            events[3] = Event.values()[i + i * 30];

            //initializing rates
            Double[] rates = new Double[4];
            rates[0] = i + 0.1 * i;
            rates[1] = i + 0.2 * i;
            rates[2] = i + 0.3 + i;
            rates[3] = i + 0.4 * i;

            //initializing bookmakers
            Bookmaker[] bookmakers = new Bookmaker[4];
            bookmakers[0] = Bookmaker.values()[i % Bookmaker.values().length];
            bookmakers[1] = Bookmaker.values()[(i + 1) % Bookmaker.values().length];
            bookmakers[2] = Bookmaker.values()[(i + 2) % Bookmaker.values().length];
            bookmakers[3] = Bookmaker.values()[(i + 3) % Bookmaker.values().length];

            //initializing yields
            Double[] yields = new Double[3];
            yields[0] = i + 0.1 * i;
            yields[1] = i + 0.2 * i;
            yields[2] = i + 0.3 * i;

            Double[] probabilities = new Double[3];
            probabilities[0] = 0.1;
            probabilities[1] = 0.7;
            probabilities[2] = 0.2;

            Fork fork = new DefaultFork(date, "firstTeam" + i, "secondTeam" + i,
                    events, rates, bookmakers, yields, probabilities);

            forksTestSet.add(fork);
            doneForksStorage.write(fork);
        }
        //receiving elements from computers memory
        Set<Fork> receivedForks = doneForksStorage.getAll();
        Assert.assertTrue(receivedForks.containsAll(forksTestSet));
    }
}
