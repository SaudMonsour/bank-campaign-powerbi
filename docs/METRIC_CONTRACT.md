# Metric contract

Contact Records counts rows, not distinct people. Subscriptions sums the binary outcome. Conversion Rate divides subscriptions by retained records under active filters. Conversion CI Lower and Upper are descriptive Wilson 95% binomial intervals with z=1.96; repeated contacts and observational sampling can violate independence, so these are not causal uncertainty estimates. DaysSincePrevious converts the 999 never-contacted sentinel to null. Average Prior Gap Days excludes those nulls; Previously Contacted Share exposes the structural coverage.

## Filter context

Dimension slicers propagate through active one-to-many, single-direction relationships to the fact table. KPI and chart measures are evaluated in the selected context. A chart selection can further narrow other visuals, subject to native Desktop interaction defaults. Blank ratios mean no valid denominator; they must not be interpreted as an observed zero. Tooltips expose record counts and, for campaign conversion, descriptive interval bounds.

## Snapshot caveats

There is no customer identifier, exact contact date or year in this selected file. Month is a category, not a chronological sequence. Keep the 12 repeated signatures because they may represent different people. Do not turn segment associations into creditworthiness decisions or claim campaign uplift.
