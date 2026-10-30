# Measure definitions

All measures are stored in the fact table and recalculate under active report filters.

## Contact Records

```dax
COUNTROWS(FactCampaign)
```

Display format: `#,0`.

## Subscriptions

```dax
SUM(FactCampaign[Subscribed])
```

Display format: `#,0`.

## Conversion Rate

```dax
DIVIDE([Subscriptions], [Contact Records])
```

Display format: `0.0%`.

## Average Call Seconds

```dax
AVERAGE(FactCampaign[DurationSeconds])
```

Display format: `#,0.0`.

## Average Campaign Contacts

```dax
AVERAGE(FactCampaign[CampaignContacts])
```

Display format: `0.00`.

## Previously Contacted Records

```dax
SUM(FactCampaign[PreviouslyContacted])
```

Display format: `#,0`.

## Previously Contacted Share

```dax
DIVIDE([Previously Contacted Records], [Contact Records])
```

Display format: `0.0%`.

## Not Recorded Records

```dax
SUM(FactCampaign[HasUnknown])
```

Display format: `#,0`.

## Not Recorded Share

```dax
DIVIDE([Not Recorded Records], [Contact Records])
```

Display format: `0.0%`.

## Duplicate Signatures

```dax
SUM(FactCampaign[ExactDuplicateFlag])
```

Display format: `#,0`.

## Average Prior Gap Days

```dax
AVERAGE(FactCampaign[DaysSincePrevious])
```

Display format: `0.0`.

## Conversion CI Lower

```dax
VAR N = [Contact Records] VAR P = [Conversion Rate] VAR Z = 1.96 RETURN IF(N > 0, DIVIDE(P + Z*Z/(2*N) - Z*SQRT(DIVIDE(P*(1-P),N) + Z*Z/(4*N*N)), 1+Z*Z/N))
```

Display format: `0.0%`.

## Conversion CI Upper

```dax
VAR N = [Contact Records] VAR P = [Conversion Rate] VAR Z = 1.96 RETURN IF(N > 0, DIVIDE(P + Z*Z/(2*N) + Z*SQRT(DIVIDE(P*(1-P),N) + Z*Z/(4*N*N)), 1+Z*Z/N))
```

Display format: `0.0%`.

