package gui;

import client.enums.Bookmaker;
import client.enums.FilterCategory;
import client.enums.YieldType;
import client.impl.DefaultFilter;
import client.interfaces.Filter;
import client.interfaces.Fork;
import client.interfaces.Manager;
import com.jidesoft.plaf.LookAndFeelFactory;
import com.jidesoft.swing.CheckBoxTree;

import javax.swing.*;
import javax.swing.event.TreeModelEvent;
import javax.swing.event.TreeModelListener;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.DefaultTreeModel;
import javax.swing.tree.TreePath;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.List;
import java.util.SortedSet;

import static client.enums.FilterCategory.*;
import static client.enums.YieldType.WEIGHTED_AVERAGE;

/**
 * Control panel.
 */
public class ControlPanel {
    private JPanel controlPanel;
    private CheckBoxTree filtersTree;
    private JButton buttonApplyFilters;
    private JPanel panelInfo;
    private JButton buttonRestoreHiddenForks;
    private JButton buttonDispatcher;
    private JButton buttonClearForksStorage;
    private final Manager manager;

    private void createUIComponents() {
        // creating tree with filters
        LookAndFeelFactory.installJideExtension();
        DefaultMutableTreeNode root = new DefaultMutableTreeNode("Filters");
        DefaultTreeModel defaultTreeModel = new DefaultTreeModel(root);
        filtersTree = new CheckBoxTree(defaultTreeModel) {
            @Override
            public boolean isCheckBoxVisible(TreePath path) {
                return ((DefaultMutableTreeNode) path.getLastPathComponent()).isLeaf();
            }
        };

        initFiltersTree();

        filtersTree.getModel().addTreeModelListener(new TreeModelListener() {
            @Override
            public void treeNodesChanged(TreeModelEvent e) {
                DefaultMutableTreeNode node;
                node = (DefaultMutableTreeNode)
                        (e.getTreePath().getLastPathComponent());
                if (node.getUserObject().toString().equals("Time")) {
                    try {
                        int index = e.getChildIndices()[0];
                        node = (DefaultMutableTreeNode)
                                (node.getChildAt(index));
                        Time.parseTime(node.getUserObject().toString());
                    } catch (NullPointerException exc) {
                    }
                }
            }

            @Override
            public void treeNodesInserted(TreeModelEvent e) {
            }

            @Override
            public void treeNodesRemoved(TreeModelEvent e) {
            }

            @Override
            public void treeStructureChanged(TreeModelEvent e) {
            }
        });
    }


    // there is no need to have more than one time instance
    private static class Time {
        public static long days = 0;
        public static long hours = 0;
        public static long minutes = 0;

        public static void parseTime(String str) {
            int dayInd = str.indexOf('d');
            int hourInd = str.indexOf('h', dayInd);
            int minuteInd = str.indexOf('m', hourInd);

            days = Long.parseLong(str.substring(0, dayInd));
            hours = Long.parseLong(str.substring(dayInd + 2, hourInd));
            minutes = Long.parseLong(str.substring(hourInd + 2, minuteInd));
        }
    }

    private ControlPanel(Manager defaultManager) {
        this.manager = defaultManager;

        buttonApplyFilters.addActionListener(e -> {
            processSelectedFilters();
            updatePanelInfo();
        });
        buttonRestoreHiddenForks.addActionListener(e -> {
            manager.restoreHiddenForks();
            updatePanelInfo();
        });
        buttonDispatcher.addActionListener(e -> {
            //TODO: call dispatcher from here
            Dispatcher dialog = new Dispatcher();
            dialog.pack();
            dialog.setVisible(true);
        });
        buttonClearForksStorage.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                manager.clearForksStorage();
                updatePanelInfo();
            }
        });
    }

    public static void start(Manager manager) {
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

        /* Initializing control panel */
        ControlPanel panel = new ControlPanel(manager);

        /* Initializing frame */
        JFrame frame = new JFrame("Control Panel");
        frame.setContentPane(panel.controlPanel);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.pack();
        frame.setVisible(true);
    }

    private void initFiltersTree() {
        DefaultTreeModel defaultTreeModel = (DefaultTreeModel)filtersTree.getModel();
        DefaultMutableTreeNode root = (DefaultMutableTreeNode)filtersTree.getModel().getRoot();
        filtersTree.setShowsRootHandles(true);

        for (FilterCategory filter : FilterCategory.values()) {
            DefaultMutableTreeNode node;
            node = new DefaultMutableTreeNode(filter.toString());
            switch (filter) {
                case REQUIRED_BOOKMAKERS:
                case HIDDEN_BOOKMAKERS:
                    for (Bookmaker b : Bookmaker.values()) {
                        defaultTreeModel.insertNodeInto(new DefaultMutableTreeNode(b.toString()), node, b.ordinal());
                    }
                    break;
                case OUTCOMES_NUMBER:
                    defaultTreeModel.insertNodeInto(new DefaultMutableTreeNode("4"), node, 0);
                    defaultTreeModel.insertNodeInto(new DefaultMutableTreeNode("5"), node, 1);
                    break;
                case TIME:
                    defaultTreeModel.insertNodeInto(new DefaultMutableTreeNode("0d 0h 0m"), node, 0);
                    break;
                case HIDE_FORKS_WITH_HIGH_COEFFICIENTS:
                    defaultTreeModel.insertNodeInto(new DefaultMutableTreeNode("< 0"), node, 0);
                    break;
                case YIELD_TYPE:
                    for (YieldType y : YieldType.values()) {
                        DefaultMutableTreeNode subNode = new DefaultMutableTreeNode(y.toString());
                        defaultTreeModel.insertNodeInto(subNode, node, y.ordinal());
                    }
                    break;
                default:
                    break;
            }
            defaultTreeModel.insertNodeInto(node, root, filter.ordinal());
        }

        //Expand all rows by default
        for (int i = 0; i < filtersTree.getRowCount(); i++) {
            filtersTree.expandRow(i);
        }
    }

    public void updatePanelInfo() {
        panelInfo.removeAll();
        panelInfo.validate();
        SortedSet<Fork> forks = manager.getFilteredForks();
        panelInfo.setLayout(new BoxLayout(panelInfo, BoxLayout.PAGE_AXIS));
        for (Fork f : forks) {
            InfoPanel infoPanel = new InfoPanel(manager, f, this);
            panelInfo.add(infoPanel.getInfoPanelElement());
        }
        panelInfo.updateUI();
    }

    private void processSelectedFilters() {
        TreePath[] selectedFilters = filtersTree.getCheckBoxTreeSelectionModel().getSelectionPaths();
        List<Filter<Object[]>> filters = new ArrayList<>();

        // arrays that might be chosen as a filters
        ArrayList<Bookmaker> requiredBookmakers = new ArrayList<>();
        ArrayList<Bookmaker> hiddenBookmakers = new ArrayList<>();
        ArrayList<Integer> outcomesNumber = new ArrayList<>();
        ArrayList<Long> time = new ArrayList<>();
        ArrayList<Double> coefficient = new ArrayList<>();
        ArrayList<YieldType> yieldType = new ArrayList<>();

        for (TreePath path : selectedFilters) {
            if (path.getPathCount() == 2) {
                // check first level filters (HIDE_FORKS_WITH_RETURN and DIFFERENT_BOOKMAKERS)
                String nodeHumanName = ((DefaultMutableTreeNode)path.getPathComponent(1)).getUserObject().toString();

                if (HIDE_FORKS_WITH_RETURN.toString().equals(nodeHumanName)) {
                    filters.add(new DefaultFilter(HIDE_FORKS_WITH_RETURN, null));
                }

                if (DIFFERENT_BOOKMAKERS.toString().equals(nodeHumanName)) {
                    filters.add(new DefaultFilter(DIFFERENT_BOOKMAKERS, null));
                }

                if (TIME.toString().equals(nodeHumanName)) {
                    time.add(Time.days);
                    time.add(Time.hours);
                    time.add(Time.minutes);
                }

                if (HIDE_FORKS_WITH_HIGH_COEFFICIENTS.toString().equals(nodeHumanName)) {
                    String childNodeHumanName = ((DefaultMutableTreeNode)((DefaultMutableTreeNode) path.getPathComponent(1))
                            .getChildAt(0)).getUserObject().toString();
                    childNodeHumanName = childNodeHumanName.substring(1);
                    coefficient.add(Double.parseDouble(childNodeHumanName));
                }

            } else { //path.getPathCount() == 3
                // check second level filters (all other)
                String nodeCategoryHumanName = ((DefaultMutableTreeNode)path.getPathComponent(1)).getUserObject().toString();
                String nodeHumanName = ((DefaultMutableTreeNode)path.getPathComponent(2)).getUserObject().toString();

                if (REQUIRED_BOOKMAKERS.toString().equals(nodeCategoryHumanName)) {
                    for (Bookmaker b : Bookmaker.values()) {
                        if (b.toString().equals(nodeHumanName)) {
                            requiredBookmakers.add(b);
                        }
                    }
                }

                if (HIDDEN_BOOKMAKERS.toString().equals(nodeCategoryHumanName)) {
                    for (Bookmaker b : Bookmaker.values()) {
                        if (b.toString().equals(nodeHumanName)) {
                            hiddenBookmakers.add(b);
                        }
                    }
                }

                if (OUTCOMES_NUMBER.toString().equals(nodeCategoryHumanName)) {
                    outcomesNumber.add(Integer.parseInt(nodeHumanName));
                }

                if (YIELD_TYPE.toString().equals(nodeCategoryHumanName)) {
                    for (YieldType yt : YieldType.values()) {
                        if (yt.toString().equals(nodeHumanName)) {
                            yieldType.add(yt);
                            break;
                        }
                    }
                }
            }
        }

        // Adding filters that were selected
        if (requiredBookmakers.size() > 0) {
            filters.add(new DefaultFilter(REQUIRED_BOOKMAKERS,
                    requiredBookmakers.toArray(new Bookmaker[requiredBookmakers.size()])));
        }

        if (hiddenBookmakers.size() > 0) {
            filters.add(new DefaultFilter(HIDDEN_BOOKMAKERS,
                    hiddenBookmakers.toArray(new Bookmaker[hiddenBookmakers.size()])));
        }

        if (outcomesNumber.size() > 0) {
            filters.add(new DefaultFilter(OUTCOMES_NUMBER,
                    outcomesNumber.toArray(new Integer[outcomesNumber.size()])));
        }

        if (time.size() == 3) {
            filters.add(new DefaultFilter(TIME, time.toArray(new Long[3])));
        }

        if (coefficient.size() == 1) {
            filters.add(new DefaultFilter(HIDE_FORKS_WITH_HIGH_COEFFICIENTS, coefficient.toArray(new Double[1])));
        }

        if (yieldType.size() == 1) {
            filters.add(new DefaultFilter(YIELD_TYPE, yieldType.toArray(new YieldType[1])));
        } else if (yieldType.size() == 0) {
            Object[] arr = { WEIGHTED_AVERAGE };
            filters.add(new DefaultFilter(YIELD_TYPE, arr));
        }


        manager.setFilters(filters);
    }
}
