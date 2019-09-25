package client.impl;

import client.interfaces.Fork;
import client.interfaces.WritableStorage;
import client.util.Constants;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.*;
import java.util.HashSet;
import java.util.Set;

import static java.nio.file.StandardOpenOption.APPEND;
import static java.nio.file.StandardOpenOption.CREATE;

/**
 * Implementation of WritableStorage interface which stores info in a file.
 */
public class FileDoneForksStorage implements WritableStorage<Fork> {
    private HashSet<Fork> forkSet;
    private final Path path;

    public FileDoneForksStorage() {
        this.path = Paths.get(Constants.getDoneForksStorageFileName());
        forkSet = new HashSet<>();
        if (Files.notExists(path)) { //assume that there is no problems with access rights
            try {
                Files.createFile(path);
            } catch (IOException ioe) {
                System.err.format("Can't create a file %s which stores done forks.%n", path.toString());
                ioe.printStackTrace();
            }
        } else {
            try (BufferedReader reader = Files.newBufferedReader(path)) {
                String line;
                while ((line = reader.readLine()) != null) {
                    forkSet.add(new DefaultFork(line));
                }
            } catch (IOException ioe) {
                ioe.printStackTrace();
            }
        }
    }

    public Set<Fork> getAll() {
        return forkSet;
    }

    public void write(Set<Fork> forks) {
        forkSet.addAll(forks);
        try (BufferedWriter writer = Files.newBufferedWriter(path, CREATE, APPEND)) {
            for (Fork b : forks) {
                writer.write(b.toString() + "\n");
            }
            writer.flush();
            writer.close();
        } catch (IOException ioe) {
            ioe.printStackTrace();
        }
    }

    public void write(Fork fork) {
        forkSet.add(fork);
        try (BufferedWriter writer = Files.newBufferedWriter(path, CREATE, APPEND)) {
            writer.write(fork.toString() + "\n");
            writer.flush();
            writer.close();
        } catch (IOException ioe) {
            ioe.printStackTrace();
        }
    }

    public void removeAll() {
        forkSet.clear();
        try {
            Files.delete(path);
        } catch (NoSuchFileException x) {
            x.printStackTrace();
        } catch (DirectoryNotEmptyException x) {
            x.printStackTrace();
        } catch (IOException x) {
            x.printStackTrace();
        }
    }
}
