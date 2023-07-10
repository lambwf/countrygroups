# UNFCCC signatures and ratification

import re
import sys
import pandas as pd

from shortcountrynames import to_name
from util import to_code, root

url = ("https://treaties.un.org/Pages/ViewDetailsIII.aspx"
       "?src=IND&mtdsg_no=XXVII-7&chapter=27&Temp=mtdsg3&clang=_en")

# Ratification and Signature status from the UN treaty collection.
try:
    print(url)
    df = pd.read_html(url, match="Belgium", encoding="UTF-8")[1]
except ValueError as e:
    print(e)
    print("Maybe {} is down?".format(url))
    sys.exit()


def get_kind(datestring):
    if datestring.endswith(" A"):
        return "Acceptance"
    elif datestring.endswith(" a"):
        return "Accession"
    elif datestring.endswith(" AA"):
        return "Approval"
    elif datestring.endswith(" d"):
        return "Succession"
    else:
        return "Ratification"


def get_date_only(datestring):
    if pd.isnull(datestring):
        return None
    datestring = datestring.strip()
    if datestring.endswith(" AA"):
        return datestring[:-3]
    elif datestring[-1] in ["a", "A", "d"]:
        return datestring[:-2]
    else:
        return datestring

df.columns = df.loc[0]
df = df.reindex(df.index.drop(0))

def remove_subscripts(participant):
    return re.sub('[\d,]', '', participant).strip()

df.Participant = df.Participant.apply(remove_subscripts)

df.index = df.Participant.apply(to_code)
df.index.name = "Code"

df.columns = [
    "Name",
    "Signature",
    "Ratification-Acceptance-Accession-Approval-Succession"
]

df["Kind"] = df.iloc[:, -1].apply(get_kind)

df.iloc[:, 1] = df.iloc[:, 1].apply(get_date_only)
df.iloc[:, 1] = pd.to_datetime(df.iloc[:, 1], dayfirst=True)
df.iloc[:, -2] = df.iloc[:, -2].apply(get_date_only)
df.iloc[:, -2] = pd.to_datetime(df.iloc[:, -2], dayfirst=True)

df.Signature = df.Signature.apply(lambda x: x.to_pydatetime())
df["Ratification-Acceptance-Accession-Approval-Succession"] = df["Ratification-Acceptance-Accession-Approval-Succession"].apply(lambda x: x.to_pydatetime())

df.Name = [to_name(code) for code in df.index]


assert len(df) == 198
assert sum(~df.Signature.isnull()) == 165
assert len(df.Name.unique()) == len(df)

df.to_csv(root / "data/unfccc.csv")
