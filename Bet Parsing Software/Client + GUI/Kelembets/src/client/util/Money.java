package client.util;

import org.junit.Assert;

import java.io.Serializable;
import java.util.Currency;
import java.util.Locale;

/**
 * Money.
 */
public class Money implements Serializable {
    private long amount;
    private final Currency currency = Currency.getInstance(Locale.US);

    /**
     * @return Amount of money in human view.
     */
    public double getAmount() {
        return (double)amount / centFactor();
    }

    public Money(long amount)
    {
        this.amount = amount * centFactor();
    }

    public Money(double amount)
    {
        this.amount = Math.round( amount * centFactor() );
    }

    private Money()
    {
    }

    public static Money dollars(double amount)
    {

        return new Money(amount);
    }

    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        Money money = (Money) o;

        if (amount != money.amount) return false;
        if (currency != null? !currency.equals(money.currency): money.currency != null) return false;

        return true;
    }

    public int hashCode() {
        int result;
        result = (int) (amount ^ (amount >>> 32));
        result = 31 * result + (currency != null? currency.hashCode(): 0);
        return result;
    }

    /**
     * Функция складывает деньги.
     * @param other с чем сложить.
     * @return Результат сложения.
     */
    public Money add(Money other)
    {
        assertSameCurrencyAs(other);
        return newMoney(amount + other.amount);
    }

    /**
     * Функция вычитает деньги.
     * @param other вычистаемое.
     * @return Результат вычитания.
     */
    public Money subtract(Money other)
    {
        assertSameCurrencyAs(other);
        return newMoney(amount - other.amount);
    }

    /**
     * Функция умнажает деньги на коэффициент.
     * @param arg вычистаемое.
     * @return Результат умножения.
     */
    public Money multiply(double arg)
    {
        return new Money(getAmount() * arg);
    }

    public int compareTo(Object other)
    {
        return compareTo((Money)other);
    }

    /**
     * Фунция сравнения денег.
     * @param other с чем сравнить
     * @return
     * -1 меньше<br>
     * 0 равно<br>
     * 1 больше<br>
     */
    public int compareTo(Money other)
    {
        assertSameCurrencyAs(other);
        if(amount < other.amount)
            return -1;
        if(amount == other.amount)
            return 0;

        return 1;
    }

    /**
     * Больше ли деньги.
     * @param other с чем сравнивать.
     * @return True, если больше.
     */
    public boolean greaterThan(Money other)
    {
        return (compareTo(other) > 0);
    }

    /**
     * Разделить деньги на несколько частей.
     * @param n количество частей.
     * @return Массив разделенных денег.
     */
    public Money[] allocate(int n)
    {
        Money lowResult = newMoney(amount/n);
        Money highResult = newMoney(lowResult.amount + 1);
        Money[] results = new Money[n];
        int remainder = (int)amount % n;

        for (int i = 0; i < remainder; i++)
            results[i] = highResult;
        for (int i = remainder; i < n; i++)
            results[i] = lowResult;
        return results;
    }

    /**
     * Разделяет деньги на неравный части.
     * @param ratios пропорция для разделения.
     * @return Массив разделенных денег.
     */
    public Money[] allocate(long[] ratios) {
        long total = 0;
        for (int i = 0; i < ratios.length; i++)
            total += ratios[i];
        long remainder = amount;
        Money[] results = new Money[ratios.length];

        for (int i = 0; i < results.length; i++)
        {
            results [i] = newMoney(amount * ratios[i] / total);
            remainder -= results[i].amount;
        }
        for (int i = 0; i < remainder; i++) {
            results[i].amount++;
        }

        return results;
    }

    private static final int [ ] cents = new int[] { 1, 10, 100, 1000 };
    private int centFactor()
    {
        return cents[currency.getDefaultFractionDigits()];
    }

    private void assertSameCurrencyAs(Money arg)
    {
        Assert.assertEquals("money math mismatch", currency, arg.currency);
    }

    private Money newMoney(long amount)
    {
        Money money = new Money();
        money.amount = amount;
        return money;
    }
}