package gui;

import com.jidesoft.swing.MultilineLabel;

import javax.swing.*;
import java.awt.event.*;
import java.io.IOException;

public class Dispatcher extends JDialog {
    private JPanel contentPane;
    private JButton buttonOK;
    private JButton buttonCancel;
    private MultilineLabel labelTutorial;
    private JTextArea textAreaCommand;

    public Dispatcher() {
        setContentPane(contentPane);
        setModal(true);
        getRootPane().setDefaultButton(buttonOK);

        labelTutorial.setText("Описание функциональности модуля dispetcher.\n" +
                "\n" +
                "1. ./dispetcher get <min_minutes> <max_minutes> <amount> <main_bookmakers> <all_bookmakers> <auto|manual>\n" +
                "Парсит информацию с букмекеров и управляет анализом. На выходе несколько файлов, имеющих формат файла info.txt. Файлы хранятся в некотором катологе, перезаписи оказаться не может.\n" +
                "    1.1. <min_minutes> - минимальное количество минут, через которое должен начаться матч\n" +
                "    1.2. <max_minutes> - максимальное количество минут, через которое должен начаться матч; вместе 1.1. - 1.2. образуют фильтр матчей по времени\n" +
                "    1.3. <amount> - количество матчей, которые необходимо распарсить и проанализировать\n" +
                "    1.4. <main_bookmakers> - целое число, кодирующее список всех \"обязательных\" букмекеров\n" +
                "    1.5. <all_bookmakers> - целое число, кодирующее список всех \"необязательных\" букмекеров\n" +
                "    1.6. <auto|manual> - строковая константа. Если auto - парс + анализ проходит без вмешательства пользователя. Если manual - возможно ручное сопоставление названий команд пользователем.\n" +
                "    Кодирование <main_bookmakers>, <all_bookmakers>:\n" +
                "    У каждого букмекера имеется свой id: id(bet365) = 0; id(sbobet) = 1; id(marathonbet) = 2; id(whill) = 3\n" +
                "    Формирование кода: представляется одним целым числом в диапозоне от 0 до 15. Преобразование из вдоичного вида в десятичный.\n" +
                "    Пример: пусть в <main_bookmakers> должны попасть bet365, marathonbet, whill. Сформируем битовую маску: 1101, где крайний правый (нулевой) бит соответствует наличию/отсутствию букмекера bet365, первый бит - sbobet, второй - marathonbet, третий - whill. Далее переводим число 1101 в десятичную систему: 1101 -> 13. Это и есть код.\n" +
                "    \n" +
                "    Пример вызова dispetcher:\n" +
                "    ./dispetcher get 200 300 5 8 15 auto - получить вилки с 5 матчей, начинающихся не ранее чем через 200 минут и не позднее чем через 300 минут, 8 - кодировка \"необязательных\" букмекеров (только whill, т.к. 8 = 1000), 15 - кодировка \"обязательных\" букмекеров (все букмекеры, т.к. 15 = 1111), auto - парс без участия пользователя\n" +
                "    \n" +
                "2. ./dispetcher initSome <code_bookmakers> - вызов инициализации букмекеров, удовлетворяющих кодировке\n" +
                "    Пример: ./dispetcher initSome 12 - инициализировать whill + sbobet, т.к. 12 = 8 + 4 = 1010\n" +
                "3. ./dispetcher initAll - инициализация всех букмекеров (равносильно вызову ./dispetcher initSome 15)\n" +
                "4. ./dispetcher resetSome <code_bookmakers> - вызов сброса файла-состояния каждого букмекера\n" +
                "    Пример: ./dispetcher resetSome 1 - сбросить файл-состояние только у bet365\n" +
                "5. ./dispetcher resetAll - аналогично ./dispetcher resetSome 15");

        buttonOK.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                onOK();
            }
        });

        buttonCancel.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                onCancel();
            }
        });

// call onCancel() when cross is clicked
        setDefaultCloseOperation(DO_NOTHING_ON_CLOSE);
        addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent e) {
                onCancel();
            }
        });

// call onCancel() on ESCAPE
        contentPane.registerKeyboardAction(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                onCancel();
            }
        }, KeyStroke.getKeyStroke(KeyEvent.VK_ESCAPE, 0), JComponent.WHEN_ANCESTOR_OF_FOCUSED_COMPONENT);
    }

    private void onOK() {
// add your code here
        //TODO: Call dispatcher from here
        try {
            Runtime.getRuntime().exec(textAreaCommand.getText());
        } catch (IOException e) {
            e.printStackTrace();
        }
        dispose();
    }

    private void onCancel() {
// add your code here if necessary
        textAreaCommand.setText("");
        dispose();
    }

    public static void main(String[] args) {
        Dispatcher dialog = new Dispatcher();
        dialog.pack();
        dialog.setVisible(true);
        System.exit(0);
    }
}
