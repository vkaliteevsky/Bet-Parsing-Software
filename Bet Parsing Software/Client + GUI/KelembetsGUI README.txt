Код тестировал только на windows, так что, возможно, на Linux что-то не влезет в экран.

Чтобы скомпилировать нужна java 8 + IntelliJ 14.

Есть скомпилированный jar файл. Его запускать из ...\Kelembets\out\artifacts\Kelembets.
Как его собрать заново - обращаться ко мне.

По вопросам по коду - тоже ко мне.

запуск java -jar Kelembets.jar

Я быстро проверил. На линуксе действительно все скверно. Чтобы было приемлемо запускайте командой
java -jar -Dswing.defaultlaf=com.sun.java.swing.plaf.gtk.GTKLookAndFeel Kelembets.jar