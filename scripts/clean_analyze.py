"""Clean the included raw snapshot without modifying source data."""
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
import hashlib, json, sys, platform
import numpy as np
import pandas as pd

def save_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, default=lambda x: x.item() if hasattr(x, 'item') else str(x)) + '\n')

def export(df, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, float_format='%.6f', date_format='%Y-%m-%d', lineterminator='\n')

def profile(df):
    return [{'column': c, 'dtype': str(df[c].dtype), 'missing': int(df[c].isna().sum()), 'distinct': int(df[c].nunique(dropna=True))} for c in df]

def date_dimension(start, end):
    d = pd.DataFrame({'Date': pd.date_range(start, end, freq='D')})
    d['DateKey'] = d.Date.dt.strftime('%Y%m%d').astype(int)
    d['Year'] = d.Date.dt.year
    d['MonthNumber'] = d.Date.dt.month
    d['MonthName'] = d.Date.dt.strftime('%b')
    d['YearMonth'] = d.Date.dt.strftime('%Y-%m')
    d['YearMonthSort'] = d.Date.dt.year * 100 + d.Date.dt.month
    d['Weekday'] = d.Date.dt.day_name()
    d['WeekdayNumber'] = d.Date.dt.dayofweek + 1
    d['IsWeekend'] = (d.Date.dt.dayofweek >= 5).astype(int)
    return d

def bank():
    p = ROOT
    raw = pd.read_csv(p / 'data/raw/bank-additional-full.csv', sep=';')
    d = raw.copy()
    d.insert(0, 'ContactRowKey', np.arange(len(d)) + 2)
    duplicate = raw.duplicated()
    unknown = raw.eq('unknown').sum()
    fields = {'age': 'Age', 'job': 'Job', 'marital': 'MaritalStatus', 'education': 'Education', 'default': 'CreditDefault', 'housing': 'HousingLoan', 'loan': 'PersonalLoan', 'contact': 'ContactChannel', 'month': 'Month', 'day_of_week': 'Weekday', 'duration': 'DurationSeconds', 'campaign': 'CampaignContacts', 'pdays': 'DaysSincePrevious', 'previous': 'PreviousContacts', 'poutcome': 'PreviousOutcome', 'emp.var.rate': 'EmploymentVariationRate', 'cons.price.idx': 'ConsumerPriceIndex', 'cons.conf.idx': 'ConsumerConfidenceIndex', 'euribor3m': 'Euribor3M', 'nr.employed': 'EmploymentCount', 'y': 'SubscriptionOutcome'}
    d = d.rename(columns=fields)
    d['ExactDuplicateFlag'] = duplicate.astype(int)
    for c in d.select_dtypes('object'):
        d[c] = d[c].str.strip().str.replace('\\s+', ' ', regex=True).replace('unknown', 'Not recorded')
    d['PreviouslyContacted'] = d.DaysSincePrevious.ne(999).astype(int)
    d.loc[d.DaysSincePrevious.eq(999), 'DaysSincePrevious'] = np.nan
    d['Subscribed'] = d.SubscriptionOutcome.eq('yes').astype(int)
    d['AgeBand'] = pd.cut(d.Age, [-np.inf, 29, 39, 49, 59, np.inf], labels=['Under 30', '30–39', '40–49', '50–59', '60+']).astype(str)
    months = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6, 'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}
    d['MonthNumber'] = d.Month.map(months)
    d['Month'] = d.Month.str.title()
    d['WeekdayOrder'] = d.Weekday.map({'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5})
    d['Weekday'] = d.Weekday.str.title()
    d['ContactIntensity'] = pd.cut(d.CampaignContacts, [0, 1, 3, 6, np.inf], labels=['1 contact', '2–3 contacts', '4–6 contacts', '7+ contacts']).astype(str)
    d['UnknownFieldCount'] = raw.eq('unknown').sum(axis=1)
    d['HasUnknown'] = d.UnknownFieldCount.gt(0).astype(int)
    export(d, p / 'data/clean/FactCampaign.csv')
    for name, col in [('DimJob', 'Job'), ('DimEducation', 'Education'), ('DimContact', 'ContactChannel'), ('DimAgeBand', 'AgeBand')]:
        dim = pd.DataFrame({col: sorted(d[col].unique())})
        if col == 'AgeBand':
            dim['AgeBandOrder'] = dim.AgeBand.map({'Under 30': 1, '30–39': 2, '40–49': 3, '50–59': 4, '60+': 5})
        export(dim, p / 'data/clean' / f'{name}.csv')
    export(d[['Month', 'MonthNumber']].drop_duplicates().sort_values('MonthNumber'), p / 'data/clean/DimMonth.csv')
    for col in ['Job', 'Education', 'ContactChannel', 'AgeBand', 'Month', 'ContactIntensity', 'PreviousOutcome']:
        g = d.groupby(col, observed=True).agg(ContactRecords=('Subscribed', 'size'), Subscriptions=('Subscribed', 'sum'), ConversionRate=('Subscribed', 'mean'), MeanDurationSeconds=('DurationSeconds', 'mean')).reset_index()
        if col == 'Month':
            g = g.merge(d[['Month', 'MonthNumber']].drop_duplicates(), on='Month').sort_values('MonthNumber')
        export(g, p / 'analysis' / f'{col}.csv')
    export(d.loc[duplicate], p / 'data/audit/duplicate_signatures.csv')
    summary = {'source_rows': len(raw), 'clean_rows': len(d), 'duplicate_signatures_retained': int(duplicate.sum()), 'subscriptions': int(d.Subscribed.sum()), 'conversion_rate': float(d.Subscribed.mean()), 'average_duration_seconds': float(d.DurationSeconds.mean()), 'average_campaign_contacts': float(d.CampaignContacts.mean()), 'never_previously_contacted': int(d.PreviouslyContacted.eq(0).sum()), 'unknown_values_source': unknown.loc[unknown.gt(0)].to_dict(), 'contact_records_with_unknown_fields': int(d.HasUnknown.sum()), 'cleaning_policy': 'Preserve all records. No customer identifier exists; exact signatures could be different customers, so flag the 12 repeated signatures rather than delete them.', 'pdays_policy': '999 is a structural never-contacted sentinel, converted to null DaysSincePrevious with an explicit PreviouslyContacted indicator. Not median-imputed.', 'time_scope': 'Month and weekday are categories across the source period. No year or exact contact date exists; no fabricated calendar trend.', 'interpretation': 'Conversion is observational, not causal campaign uplift. Duration is known after the call; it is not a valid pre-call predictor.'}
    assert d.ContactRowKey.is_unique and len(d) == len(raw) and (d.Subscribed.sum() == raw.y.eq('yes').sum())
    save_json(p / 'analysis/summary.json', summary)
    save_json(p / 'analysis/cleaning_audit.json', {'before': profile(raw), 'after': profile(d), 'unknown_labels_explicit': True, 'duplicate_signatures_flagged': int(duplicate.sum()), 'rows_removed': 0})
    return summary

ROOT = Path(__file__).resolve().parents[1]
if __name__ == "__main__":
    print(json.dumps(bank(), indent=2, default=str))
