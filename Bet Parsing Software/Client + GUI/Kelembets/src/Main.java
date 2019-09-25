import client.impl.DefaultManager;
import gui.ControlPanel;

/**
 * The execution of the program starts here.
 */
public class Main {

    public static void main(String[] args) {
        try {
            ControlPanel.start(DefaultManager.getInstance());
        } catch(InstantiationException e) {
            e.printStackTrace();
        }
    }

}
