package client.util;

/**
 * Class containing all Platform dependent constants
 */
public class Constants {

    public static enum OS {
        WINDOWS("C:\\Kelembets\\all_forks_storage.txt",
                "C:\\Kelembets\\done_bets.txt",
                "C:\\Kelembets\\"),
        LINUX("/opt/kelembets/all_forks_storage",
              "/opt/kelembets/done_bets",
              "/opt/kelembets/");

        public final String allForksStorageFileName;
        public final String doneForksStorageFileName;
        public final String generousFileStorage;

        private OS(String allForksStorageFileName,
                   String doneForksStorageFileName,
                   String generousFileStorage) {
            this.allForksStorageFileName = allForksStorageFileName;
            this.doneForksStorageFileName = doneForksStorageFileName;
            this.generousFileStorage = generousFileStorage;
        }
    }

    public static String getAllForksStorageFileName() {
        for (OS os : OS.values()) {
            if (System.getProperty("os.name").toUpperCase().contains(os.toString())) {
                return os.allForksStorageFileName;
            }
        }
        return "";
    }

    public static String getDoneForksStorageFileName() {
        for (OS os : OS.values()) {
            if (System.getProperty("os.name").toUpperCase().contains(os.toString())) {
                return os.doneForksStorageFileName;
            }
        }
        return "";
    }

    public static String getGenerousFileStorageDirectoryName() {
        for (OS os : OS.values()) {
            if (System.getProperty("os.name").toUpperCase().contains(os.toString())) {
                return os.generousFileStorage;
            }
        }
        return "";
    }
}
