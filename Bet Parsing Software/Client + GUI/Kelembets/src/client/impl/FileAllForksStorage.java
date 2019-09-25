package client.impl;

import client.interfaces.Fork;
import client.interfaces.Storage;
import client.util.Constants;

import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.*;
import java.nio.file.attribute.BasicFileAttributes;
import java.nio.file.attribute.FileTime;
import java.util.HashSet;
import java.util.Set;

import static java.nio.file.StandardOpenOption.CREATE;
import static java.nio.file.StandardOpenOption.TRUNCATE_EXISTING;

/**
 * Implementation of Storage interface for all folks, which come from the dispatcher.
 */
public class FileAllForksStorage implements Storage<Fork> {
    private Set<Fork> forkSet;
    private FileTime lastModifiedTime;
    private final Path path;

    public FileAllForksStorage() {
        this.forkSet = new HashSet<>();
        this.path = Paths.get(Constants.getAllForksStorageFileName());
        if (Files.exists(path)) {
            try {
                this.lastModifiedTime = Files.readAttributes(path, BasicFileAttributes.class).lastModifiedTime();
            } catch (IOException ioe) {
                ioe.printStackTrace();
            }
            readForksFromFile();
        } else {
            this.lastModifiedTime = FileTime.fromMillis(0);
        }
    }

    public Set<Fork> getAll() {
        try {
            FileTime fileLastModificationTime = Files.readAttributes(path, BasicFileAttributes.class).lastModifiedTime();
            if (!lastModifiedTime.equals(fileLastModificationTime)) {
                lastModifiedTime = fileLastModificationTime;
                readForksFromFile();
            }
        } catch (NoSuchFileException e) {
            // if NoSuchFileException thrown return empty set
        } catch (IOException ioe) {
            ioe.printStackTrace();
        }
        return forkSet;
    }

    private void readForksFromFile() {
        forkSet.clear();
        try (BufferedReader reader = Files.newBufferedReader(path)) {
            String line;
            while (((line = reader.readLine()) != null)) {
                forkSet.add(new DefaultFork(line));
            }
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
