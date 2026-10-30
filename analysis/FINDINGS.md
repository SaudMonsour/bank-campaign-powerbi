# Analysis findings

The full additional bank-marketing table has 41,188 contact records and 4,640 positive outcomes: 11.27% observed conversion.

## Observed patterns

- Cellular contacts: 3,853 subscriptions / 26,144 records = 14.74%.
- Telephone contacts: 787 / 15,044 = 5.23%.
- One campaign contact: 2,300 / 17,642 = 13.04%.
- Seven or more contacts: 111 / 2,406 = 4.61%.
- A recorded prior successful campaign outcome: 894 / 1,373 = 65.11%.

These differences can reflect audience selection, previous relationships, channel availability, economic conditions and contact scheduling. They do not estimate the causal effect of changing a channel or adding a call. Group counts and Wilson intervals accompany conversion rates.

## Cleaning judgment

Keep all records. The twelve exact signatures are flagged because a customer ID is absent; deleting them could remove distinct customers. Records are contacts, not verified unique customers. Unknown strings become explicit Not recorded categories, and 10,700 records retain a missing-field flag.

The pdays value 999 indicates no previous contact. It becomes a structural null with a separate contact flag. Average prior-gap days excludes those structural nulls rather than turning 999 into a real interval. A small inconsistency remains between the previous-contact and previous-outcome variables; the dashboard preserves original categories rather than forcing them to agree.

Month and weekday are categories, not exact dates. No year, chronological monthly revenue trend, or year-over-year metric has been invented. Call duration is observed after the call and would leak the outcome context in a pre-call prediction use case.
