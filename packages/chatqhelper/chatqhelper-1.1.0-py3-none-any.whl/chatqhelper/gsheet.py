"""
The module suppporting getting records from google sheet and perform filter and projection.
To use google sheet api 2 main steps must be done:
    - enable google sheet api and get the service account credentials
    - share the sheet with the associated email in service account credentials
"""
import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os, copy

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
SERVICE_SECRET_FILE =  os.environ['GOOGLE_APPLICATION_CREDENTIALS']


BOOL_TRUE = 'TRUE'
BOOL_FALSE = 'FALSE'


def get_client():
    """
    get a new google sheet client and login
    require service file containg google service credentials
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_SECRET_FILE, SCOPES)
    client = gspread.Client(credentials)
    client.login()
    return client

class Record():
    def __init__(self, records=[], spreadsheet=None, worksheet=None, client=None):
        self._records = records
        self._record_keys = records[0].keys() if records else []
        self._spreadsheet = spreadsheet
        self._worksheet = worksheet
        self._client = client
    
    def filter(self, filt={}):
        """
        filter should be 1 level dictionary.
        to do nested filter operation, perform 2 separated filter, one after another
        sample filter:
        filter = {
            "Index": {
                LTE: 50
            }
        }
        """
        if not self._records or not filt:
            return self._records

        rec_keys = self._record_keys
        filt_keys = filt.keys()

        # validate filter keys. warn if filter keys not in record keys
        missing_keys = list(set(filt_keys) - set(rec_keys))
        if missing_keys:
            raise Exception('could not filter. Missing key in record {}'.format(missing_keys))

        results = []
        for record in self._records:
            results.append(record)
            for key in filt_keys:
                opt_code, param = get_operator_param(filt[key])
                if not operator_filter[opt_code](record[key], param):
                    results.pop()
                    break
        
        self._records = results
        return self

    def project(self, proj):
        """
        The main purpose of projection is to reduce memory foodprint when it deletes fields/keys not needed by applications
        Projection should be a dictionary with keys as the fields to be projected and values is true/false or 0/1
        Projection can be a list of desired fields
        """
        if not self._records or not proj:
            return self._records
        
        # if it's a list, then map to key:True
        if isinstance(proj, list):
            proj = {k:True for k in proj}

        rec_keys = self._record_keys
        yes_keys = [k for k in proj.keys() if proj[k]]
        yes_keys = yes_keys if yes_keys else copy.deepcopy(list(rec_keys))
        no_keys = [k for k in proj.keys() if not proj[k]]
        yes_keys = list(set(yes_keys) - set(no_keys))

        if not yes_keys:
            raise Exception('invalid projection, nothing left to show')
        
        results = [
            {
                k:record[k] for k in yes_keys
            } for record in self._records
        ]

        self._records = results
        self._record_keys = results[0].keys()
    
    def to_json(self):
        return copy.deepcopy(self._records)

    def reload(self):
        records = self._worksheet.get_all_records()
        self._records = records

    @classmethod
    def get_all_records_from_sheet(cls, spreadsheet_id, worksheet_name, client=None):
        if not client:
            client = get_client()
        spreadsheet = client.open_by_key(spreadsheet_id)
        worksheet = spreadsheet.worksheet(worksheet_name)
        records = worksheet.get_all_records()
        records = Record(records, spreadsheet, worksheet, client)
        return records

# ------------------------------------------------------

# operators
EQ = '$EQ'
NE = '$NE'
NOT = '$NOT'
IN = '$IN'
NOTIN = '$NOTIN'
HAS = '$HAS'
NOTHAS = '$NOTHAS'
GT = '$GT'
GTE = '$GTE'
LT = '$LT'
LTE = '$LTE'

# operator functions
def eq_filt(value, param):
    return value == param

def ne_filt(value, param):
    return value != param

def in_filt(value, param):
    return value in param

def notin_filt(value, param):
    return value not in param

def has_filt(value, param):
    return param in value

def nothas_filt(value, param):
    return param not in value

def gt_filt(value, param):
    return type(param)(value) > param

def gte_filt(value, param):
    return type(param)(value) >= param

def lt_filt(value, param):
    return type(param)(value) < param

def lte_filt(value, param):
    return type(param)(value) <= param

def get_operator_param(filt):
    operator, param = EQ, filt
    if isinstance(filt, dict):
        operator = list(filt)[0]
        param = filt[operator]
    return operator, param

# a map of operator name to operator function
operator_filter = {
    EQ: eq_filt,
    NE: ne_filt,
    IN: in_filt,
    NOTIN: notin_filt,
    HAS: has_filt,
    NOTHAS: nothas_filt,
    GT: gt_filt,
    GTE: gte_filt,
    LT: lt_filt,
    LTE: lte_filt,
}

#----------------------------------------------------------

if __name__ == "__main__":
    pass
#     # print(opt_parm({NOT:{ISIN:['a','b','c']}}))
#     print(get_records({USER_FN:{NOT:{ISIN:["Khoa", "Ilya"]}}},{USER_FN:1, USER_ID:0}))