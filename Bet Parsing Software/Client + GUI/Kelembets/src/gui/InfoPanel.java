package gui;

import client.enums.YieldType;
import client.impl.DefaultFork;
import client.impl.DefaultManager;
import client.interfaces.Fork;
import client.interfaces.Manager;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import javax.swing.table.TableModel;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.io.IOException;

/**
 * Created by aoool on 17.01.2015.
 */
public class InfoPanel extends JPanel {
    private JTable table;
    private static final String[] columnNames = {"Bookmakers", "Event Type", "Rate"};
    private JPanel infoPanelElement;
    public JScrollPane scrollPaneInfo;
    private JLabel labelDate;
    private JLabel labelFirstTeam;
    private JLabel labelSecondTeam;
    private JCheckBox checkBoxMarkAsDone;
    private JButton moveToStorageButton;
    private JLabel labelPossibleYields;
    private JSplitPane splitPanePossibleYields;
    private JLabel labelAvg;
    private JLabel labelAvgVariance;
    private JButton buttonCalculator;
    private JLabel labelWAvg;
    private JLabel labelMin;
    private JTextField textFieldComment;
    private JCheckBox markAsHiddenCheckBox;
    private JButton buttonHide;
    private JLabel labelWAvgVariance;
    private JButton hideThisMatchButton;
    private JCheckBox checkBoxHideThisMath;
    private final Manager manager;
    private final Fork fork;
    private final ControlPanel controlPanel;


    public InfoPanel(Manager m, Fork panelFork, ControlPanel parentControlPanel) {
        manager = m;
        fork = panelFork;
        controlPanel = parentControlPanel;

        //infoPanelElement.setBorder(BorderFactory.createRaisedBevelBorder());
        infoPanelElement.setBorder(BorderFactory.createLineBorder(Color.BLACK));
        splitPanePossibleYields.setResizeWeight(0.5);

        initTable(fork);
        initLabels(fork);

        checkBoxMarkAsDone.addItemListener(e -> moveToStorageButton.setEnabled(!moveToStorageButton.isEnabled()));

        markAsHiddenCheckBox.addItemListener(e -> buttonHide.setEnabled(!buttonHide.isEnabled()));

        moveToStorageButton.addActionListener(e -> {
            manager.markForkAsDone(fork);
            infoPanelElement.setVisible(false);
        });

        buttonCalculator.addActionListener(e -> {
            String fileName = manager.storeForkInFile(fork);
            String command = "gnome-terminal -x ./call_calc.sh " + fileName;
            try {
                Runtime.getRuntime().exec(command);
            } catch (IOException ioe) {
                ioe.printStackTrace();
            }
        });

        buttonHide.addActionListener(e -> {
            manager.hideFork(fork);
            infoPanelElement.setVisible(false);
        });

        checkBoxHideThisMath.addItemListener(e -> hideThisMatchButton.setEnabled(!hideThisMatchButton.isEnabled()));

        hideThisMatchButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                manager.hideMatch(fork.getFirstTeam(),
                        fork.getSecondTeam(),
                        fork.getDate());
                controlPanel.updatePanelInfo();
            }
        });
    }

    public JComponent getInfoPanelElement() {
        return infoPanelElement;
    }

    private void initLabels(Fork fork) {
        labelDate.setText(fork.getDate().toString());
        labelFirstTeam.setText(fork.getFirstTeam());
        labelSecondTeam.setText(fork.getSecondTeam());

        StringBuilder yields = new StringBuilder();
        for (Double d : fork.getYields()) {
            yields.append(String.format("%.2f", d * 100));
            yields.append("% | ");
        }
        yields.delete(yields.lastIndexOf("|") - 1, yields.lastIndexOf("|") + 1);
        labelPossibleYields.setText(yields.toString());

        // setting yield functions values
        labelAvg.setText(labelAvg.getText() +
                String.format("%.2f", manager.getYieldFunction(YieldType.AVERAGE).apply(fork) * 100) + "%");
        labelAvgVariance.setText(labelAvgVariance.getText() +
                String.format("%.2f", manager.getYieldFunction(YieldType.AVERAGE_VARIANCE).apply(fork) * 100) + "%");
        labelWAvg.setText(labelWAvg.getText() +
                String.format("%.2f", manager.getYieldFunction(YieldType.WEIGHTED_AVERAGE).apply(fork) * 100) + "%");
        labelWAvgVariance.setText(labelWAvgVariance.getText() +
                String.format("%.2f", manager.getYieldFunction(YieldType.WEIGHTED_AVERAGE_VARIANCE).apply(fork) * 100) + "%");
        labelMin.setText(labelMin.getText() +
                String.format("%.2f", manager.getYieldFunction(YieldType.MINIMUM).apply(fork) * 100) + "%");
    }

    private void initTable(Fork fork) {
        TableModel model = new DefaultTableModel(createForkInfoTable(fork), columnNames);
        table.setModel(model);
        table.updateUI();
    }

    private static Object[][] createForkInfoTable(Fork fork) {
        String[][] tab = new String[fork.getOutcomes()][columnNames.length];
        for (int i = 0; i < fork.getOutcomes(); i++) {
            tab[i][0] = fork.getBookmakers().get(i).toString();
            tab[i][1] = fork.getEvents().get(i).toString();
            tab[i][2] = fork.getRates().get(i).toString();
        }
        return tab;
    }

    public static void main(String[] args) {
        /* Setting LookAndFeel styles */
        try {
            // Set System L&F
            UIManager.setLookAndFeel(
                    UIManager.getSystemLookAndFeelClassName());
        } catch (UnsupportedLookAndFeelException e) {
            e.printStackTrace();
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        } catch (InstantiationException e) {
            e.printStackTrace();
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        }
        JFrame frame = new JFrame("InfoPanel");
        try {
            frame.setContentPane(new InfoPanel(DefaultManager.getInstance(),
                    new DefaultFork("3|firstTeam3|secondTeam3|3,33,63,93|3.3,3.6,6.3,4.2|3,0,1,2|3.3,3.6,3.9"), null).infoPanelElement);
        } catch (InstantiationException e) {
            e.printStackTrace();
            return;
        }
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.pack();
        frame.setVisible(true);
    }

}
