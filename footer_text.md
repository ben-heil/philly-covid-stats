## Philly COVID Response Levels (Feb 16):
> The Response Levels are triggered by meeting the following thresholds (the lowest level for which the city meets metrics will apply):
>
>  **Extreme Caution [Red]**
>  - Two or more of the following are true:
>  - - Average new cases per day is 500 or more
>  - - Hospitalizations are 500 or more
>  - - Percent positivity is 10% or more
>  - - Cases have risen by more than 50% in the previous 10 days
>  **Caution [Orange]**
>  - Three or more of the following are true:
>  - - Average new cases per day is less than 500
>  - - Hospitalizations are under 500
>  - - Percent positivity is under 10%
>  - - Cases have not risen by more than 50% in the previous 10 days
>  **Mask Precautions [Yellow]**
>  - Three or more of the following are true:
>  - - Average new cases per day is less than 225 (This is approximately the cut-off >between CDC’s “high” and “substantial” levels of transmission)
>  - - Hospitalizations are under 100
>  - - Percent positivity is under 5%
>  - - Cases have not risen by more than 50% in the previous 10 days
>  **All Clear [Green]**
>  - Three or more of the following are true:
>  - - Average new cases per day is less than 100 (This is approximately the cut-off >between CDC’s “substantial” and “moderate” levels of transmission)
>  - - Hospitalizations are under 50
>  - - Percent positivity is under 2%
>  - - Cases have not risen by more than 50% in the previous 10 days
## Notes:

- Data for a given day is based on the day a test is received, not when the result comes in. As a result, the most recent data is likely to consitently undercount both positive and negative tests. The based on [these graphs](https://www.phila.gov/programs/coronavirus-disease-2019-covid-19/data/testing/), data that's at least a week old can be considered rougly accurate.
- Days with fewer than six entries for cases/negative tests/etc are masked for privacy. To avoid undercounting those days I set the value to five. This may lead to overcounting in some cases.
- The city doesn't define "average", so I used a 7-day right-aligned rolling window. Their definition is likely different.
- The hospitalization figure is based on confirmed cases, it's unclear whether the city uses suspected cases for their decisionmaking (or all hospitalizations).
