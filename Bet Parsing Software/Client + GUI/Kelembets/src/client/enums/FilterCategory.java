package client.enums;


/**
 * Filters head categories.
 */
public enum FilterCategory {
    REQUIRED_BOOKMAKERS("Required bookmakers"),
    HIDDEN_BOOKMAKERS("Hidden bookmakers"),
    HIDE_FORKS_WITH_RETURN("Hide forks with return"),
    DIFFERENT_BOOKMAKERS("Different bookmakers"),
    OUTCOMES_NUMBER("Outcomes number"),
    TIME("Time"),
    HIDE_FORKS_WITH_HIGH_COEFFICIENTS("Coefficient"),
    YIELD_TYPE("Yield type");

    private final String humanName;

    private FilterCategory(String humanName) {
        this.humanName = humanName;
    }

    @Override
    public String toString() {
        return humanName;
    }
}
