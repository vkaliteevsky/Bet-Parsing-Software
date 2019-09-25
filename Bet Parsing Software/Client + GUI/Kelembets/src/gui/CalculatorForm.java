package gui;

import javax.swing.*;

/**
 * Created by admin on 20/01/15.
 */
public class CalculatorForm {
    private JTable Yields;
    private JTextField whillCoef;
    private JTextField sbobetCoef;
    private JTextField bet365BET;
    private JTextField marathonBET;
    private JTextField whillBET;
    private JTextField sbobetBET;
    private JTextField bet365Coef;
    private JTextField marathonCoef;
    private JLabel avgFuncLabel;
    private JLabel weightedAvgFuncLabel;
    private JLabel dispertionFuncLabel;
    private JTextField sumTextField;
    private JPanel calculatorPanel;

    public static void main(String[] args) {
        JFrame frame = new JFrame("CalculatorForm");
        frame.setContentPane(new CalculatorForm().calculatorPanel);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.pack();
        frame.setVisible(true);
    }
}
