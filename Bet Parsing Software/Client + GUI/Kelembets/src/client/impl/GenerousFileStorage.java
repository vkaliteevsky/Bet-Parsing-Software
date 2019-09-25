package client.impl;

import client.interfaces.Fork;
import client.interfaces.WritableStorage;
import client.util.Constants;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashSet;
import java.util.Set;

import static java.nio.file.StandardOpenOption.APPEND;
import static java.nio.file.StandardOpenOption.CREATE;
import static java.nio.file.StandardOpenOption.TRUNCATE_EXISTING;

/**
 * Created by aoool on 1/29/15.
 */
public class GenerousFileStorage  {
    private final String directoryName;
    private static int counter = 0;

    public GenerousFileStorage() {
        this.directoryName = Constants.getGenerousFileStorageDirectoryName();
    }

    /**
     * @param fork
     * @return full name of the created file
     */
    public String write(Fork fork) throws RuntimeException {
        String filename = directoryName + counter;
        try (BufferedWriter writer = Files.newBufferedWriter(Paths.get(filename), CREATE, TRUNCATE_EXISTING)) {
            writer.write(fork.toString() + "\n");
            writer.flush();
            writer.close();
            return filename;
        } catch (IOException ioe) {
            ioe.printStackTrace();
            throw new RuntimeException(String.format("GenerousFileStorage: could not create file %s", filename));
        }
    }

}
