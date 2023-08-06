import sys
from functools import wraps
import json
import requests
from glom import glom, T
import itertools
import tempfile
import secrets
from time import sleep

from yattag import Doc
from IPython.display import HTML,display
import ipywidgets as widgets

from demyst.common.config import load_config
from demyst.common.connectors import Connectors, DemystConnectorError
from demyst.common.track import track_function
from demyst.analytics.shiny import progressbar
from demyst.analytics.shiny import generatehandlerbutton

import os
import pandas as pd
from pandas.api.types import is_string_dtype

from pandas_schema import Column, Schema
from pandas_schema.validation import MatchesPatternValidation, IsDtypeValidation, InListValidation, CanCallValidation

from urllib.parse import urlparse

import warnings
warnings.filterwarnings("ignore", 'This pattern has match groups')

non_empty_validation = MatchesPatternValidation(r'.+')
decimal_number_validation = MatchesPatternValidation(r'^[+-]?\d*(\.\d+)?$')

percentage_validation = non_empty_validation & MatchesPatternValidation(r'^\d*(\.\d+)?%?$')
number_validation = non_empty_validation & decimal_number_validation
first_name_validation = non_empty_validation
last_name_validation = non_empty_validation
middle_name_validation = non_empty_validation
city_validation = non_empty_validation
business_name_validation = non_empty_validation
marital_status_validation = non_empty_validation & InListValidation([
        "A", "ANNULLED",
        "D", "DIVORCED",
        "I", "INTERLOCUTORY",
        "L", "LEGALLY SEPARATED",
        "M", "MARRIED",
        "P", "POLYGAMOUS",
        "S", "NEVER MARRIED", "SINGLE",
        "T", "DOMESTIC PARTNER",
        "U", "UNMARRIED",
        "W", "WIDOWED"
        ], case_sensitive=False)
email_address_validation = non_empty_validation & MatchesPatternValidation(r'^[^@]+@[^@]+\.[^@]+$')
ip4_validation = non_empty_validation & MatchesPatternValidation(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
latitude_validation = non_empty_validation & MatchesPatternValidation(r'^(\+|-)?(?:90(?:(?:\.0{1,6})?)|(?:[0-9]|[1-8][0-9])(?:(?:\.[0-9]{1,6})?))$') # https://jex.im/regulex/#!embed=true&flags=&re=%5E(%5C%2B%7C-)%3F(%3F%3A90(%3F%3A(%3F%3A%5C.0%7B1%2C6%7D)%3F)%7C(%3F%3A%5B0-9%5D%7C%5B1-8%5D%5B0-9%5D)(%3F%3A(%3F%3A%5C.%5B0-9%5D%7B1%2C6%7D)%3F))%24
longitude_validation = non_empty_validation & MatchesPatternValidation(r'^(\+|-)?(?:180(?:(?:\.0{1,6})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\.[0-9]{1,6})?))$') # https://jex.im/regulex/#!cmd=export&flags=&re=%5E(%5C%2B%7C-)%3F(%3F%3A180(%3F%3A(%3F%3A%5C.0%7B1%2C6%7D)%3F)%7C(%3F%3A%5B0-9%5D%7C%5B1-9%5D%5B0-9%5D%7C1%5B0-7%5D%5B0-9%5D)(%3F%3A(%3F%3A%5C.%5B0-9%5D%7B1%2C6%7D)%3F))%24
full_name_validation = non_empty_validation
domain_validation = non_empty_validation & MatchesPatternValidation(r'^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$')
year_month_validation = non_empty_validation & MatchesPatternValidation(r'^\d{4}-\d{2}$')
year_validation = non_empty_validation & MatchesPatternValidation(r'^\d{4}$')
string_validation = non_empty_validation
country_validation = non_empty_validation & MatchesPatternValidation(r'(?i)^(AF|AX|AL|DZ|AS|AD|AO|AI|AQ|AG|AR|AM|AW|AU|AT|AZ|BS|BH|BD|BB|BY|BE|BZ|BJ|BM|BT|BO|BQ|BA|BW|BV|BR|IO|BN|BG|BF|BI|KH|CM|CA|CV|KY|CF|TD|CL|CN|CX|CC|CO|KM|CG|CD|CK|CR|CI|HR|CU|CW|CY|CZ|DK|DJ|DM|DO|EC|EG|SV|GQ|ER|EE|ET|FK|FO|FJ|FI|FR|GF|PF|TF|GA|GM|GE|DE|GH|GI|GR|GL|GD|GP|GU|GT|GG|GN|GW|GY|HT|HM|VA|HN|HK|HU|IS|IN|ID|IR|IQ|IE|IM|IL|IT|JM|JP|JE|JO|KZ|KE|KI|KP|KR|KW|KG|LA|LV|LB|LS|LR|LY|LI|LT|LU|MO|MK|MG|MW|MY|MV|ML|MT|MH|MQ|MR|MU|YT|MX|FM|MD|MC|MN|ME|MS|MA|MZ|MM|NA|NR|NP|NL|NC|NZ|NI|NE|NG|NU|NF|MP|NO|OM|PK|PW|PS|PA|PG|PY|PE|PH|PN|PL|PT|PR|QA|RE|RO|RU|RW|BL|SH|KN|LC|MF|PM|VC|WS|SM|ST|SA|SN|RS|SC|SL|SG|SX|SK|SI|SB|SO|ZA|GS|SS|ES|LK|SD|SR|SJ|SZ|SE|CH|SY|TW|TJ|TZ|TH|TL|TG|TK|TO|TT|TN|TR|TM|TC|TV|UG|UA|AE|GB|US|UM|UY|UZ|VU|VE|VN|VG|VI|WF|EH|YE|ZM|ZW)$')
us_ein_validation = non_empty_validation & MatchesPatternValidation(r'^\d\d-?\d\d\d\d\d\d\d$')
us_ssn_validation = non_empty_validation & MatchesPatternValidation(r'^\d\d\d-?\d\d-?\d\d\d\d$')
us_ssn4_validation = non_empty_validation & MatchesPatternValidation(r'^\d\d\d\d$')
sic_code_validation = non_empty_validation & MatchesPatternValidation(r'^\d\d\d\d$')
gender_validation = non_empty_validation & MatchesPatternValidation(r'(?i)^m(ale)?$|^f(emale)?$')
post_code_validation = non_empty_validation & MatchesPatternValidation(r'^[0-9A-Z -]{3,}$')
# XXX The following are simply passed through to BKF without any checking:
state_validation = non_empty_validation & InListValidation([
        "AL", "Alabama",
        "AK", "Alaska",
        "AZ", "Arizona",
        "AR", "Arkansas",
        "AE", "Armed Forces in Europe, the Middle East, Africa, and Canada",
        "AA", "Armed Forces in the Americas",
        "AP", "Armed Forces in the Pacific",
        "CA", "California",
        "CO", "Colorado",
        "CT", "Connecticut",
        "DE", "Delaware",
        "DC", "District Of Columbia",
        "FL", "Florida",
        "GA", "Georgia",
        "HI", "Hawaii",
        "ID", "Idaho",
        "IL", "Illinois",
        "IN", "Indiana",
        "IA", "Iowa",
        "KS", "Kansas",
        "KY", "Kentucky",
        "LA", "Louisiana",
        "ME", "Maine",
        "MD", "Maryland",
        "MA", "Massachusetts",
        "MI", "Michigan",
        "MN", "Minnesota",
        "MS", "Mississippi",
        "MO", "Missouri",
        "MT", "Montana",
        "NE", "Nebraska",
        "NV", "Nevada",
        "NH", "New Hampshire",
        "NJ", "New Jersey",
        "NM", "New Mexico",
        "NY", "New York",
        "NC", "North Carolina",
        "ND", "North Dakota",
        "OH", "Ohio",
        "OK", "Oklahoma",
        "OR", "Oregon",
        "PA", "Pennsylvania",
        "PR", "Puerto Rico",
        "RI", "Rhode Island",
        "SC", "South Carolina",
        "SD", "South Dakota",
        "TN", "Tennessee",
        "TX", "Texas",
        "UT", "Utah",
        "VT", "Vermont",
        "VA", "Virginia",
        "WA", "Washington",
        "WV", "West Virginia",
        "WI", "Wisconsin",
        "WY", "Wyoming",
        # Canada
        "09", "Quebec",
        "17", "Saskatchewan",
        "AB", "Alberta",
        "BC", "British Columbia",
        "MB", "Manitoba",
        "NB", "New Brunswick",
        "NL", "Newfoundland and Labrador",
        "NS", "Nova Scotia",
        "NT", "Northwest Territories",
        "NU", "Nunavut",
        "ON", "Ontario",
        "PE", "Prince Edward Island",
        "YT", "Yukon",
        # Mexico
        "AGU", "Aguascalientes",
        "BCN", "Baja California",
        "BCS", "Baja California Sur",
        "CAM", "Campeche",
        "CHH", "Chihuahua",
        "CHP", "Chiapas",
        "CMX", "Mexican Federal District",
        "COA", "Coahuila",
        "COL", "Colima",
        "DUR", "Durango",
        "GRO", "Guerrero",
        "GUA", "Guanajuato",
        "HID", "Hidalgo",
        "JAL", "Jalisco",
        "MEX", "México",
        "MIC", "Michoacán",
        "MOR", "Morelos",
        "NAY", "Nayarit",
        "NLE", "Nuevo León",
        "OAX", "Oaxaca",
        "PUE", "Puebla",
        "QUE", "Querétaro",
        "ROO", "Quintana Roo",
        "SIN", "Sinaloa",
        "SLP", "San Luis Potosí",
        "SON", "Sonora",
        "TAB", "Tabasco",
        "TAM", "Tamaulipas",
        "TLA", "Tlaxcala",
        "VER", "Veracruz",
        "YUC", "Yucatán",
        "ZAC", "Zacatecas"
        ], case_sensitive=False)
street_validation = non_empty_validation
blob_validation = non_empty_validation
phone_validation = non_empty_validation
# XXX urlparse allows basically anything, maybe check for existence of netloc (i.e. host) part?
url_validation = non_empty_validation & CanCallValidation(urlparse)

# Type specs are used to associate type names with validations (in the
# type_specs dictionary, below), and also to note whether to use a
# type to create suggestions (types which match any non-empty string
# make poor suggestions).  The specificity value is used to rank type
# specs: if two type specs have the same error rate for a column, the
# one with the higher specificity comes earlier in the list of
# suggestions.
class TypeSpec(object):
    def __init__(self, name, validation, specificity=50, suggest=True):
        self.name = name
        self.validation = validation
        self.specificity = specificity
        self.suggest = suggest

type_specs = {
    'percentage': TypeSpec('Percentage', percentage_validation),
    'email_address': TypeSpec('EmailAddress', email_address_validation),
    # Make plain number less specific than percentages etc
    'number': TypeSpec('Number', number_validation, specificity=30),
    'string': TypeSpec('String', string_validation, suggest=False),
    'first_name': TypeSpec('FirstName', first_name_validation, suggest=False),
    'last_name': TypeSpec('LastName', last_name_validation, suggest=False),
    'full_name': TypeSpec('FullName', full_name_validation, suggest=False),
    'middle_name': TypeSpec('MiddleName', middle_name_validation, suggest=False),
    'city': TypeSpec('City', city_validation, suggest=False),
    'business_name': TypeSpec('BusinessName', business_name_validation, suggest=False),
    'marital_status': TypeSpec('MaritalStatus', marital_status_validation),
    'ip4': TypeSpec('Ip4', ip4_validation),
    'latitude': TypeSpec('Latitude', latitude_validation),
    'longitude': TypeSpec('Longitude', longitude_validation),
    'domain': TypeSpec('Domain', domain_validation),
    'year_month': TypeSpec('YearMonth', year_month_validation),
    'year': TypeSpec('Year', year_validation),
    'country': TypeSpec('Country', country_validation),
    # Make these codes more specific than numbers, percentages, etc.
    'us_ein': TypeSpec('UsEin', us_ein_validation, specificity=70),
    'us_ssn': TypeSpec('UsSsn', us_ssn_validation, specificity=70),
    'us_ssn4': TypeSpec('UsSsn4', us_ssn4_validation, specificity=70),
    'sic_code': TypeSpec('SicCode', sic_code_validation, specificity=70),
    'gender': TypeSpec('Gender', gender_validation),
    # Make post code even more specific
    'post_code': TypeSpec('PostCode', post_code_validation, specificity=90),
    'state': TypeSpec('State', state_validation, specificity=90),
    'street': TypeSpec('Street', street_validation, suggest=False),
    'blob': TypeSpec('Blob', blob_validation, suggest=False),
    'phone': TypeSpec('Phone', phone_validation, suggest=False),
    'url': TypeSpec('Url', url_validation, suggest=False)
}

# Type suggestions are generated for each column whose name doesn't
# match one of our predefined column names.  Each suggestion points to
# a potential type spec and has an error rate (float, percentage) that
# says how many rows of that column didn't pass that type spec's
# validation.
class TypeSuggestion(object):
    def __init__(self, type_spec, error_rate):
        self.type_spec = type_spec
        self.error_rate = error_rate
    def __repr__(self):
        return self.type_spec.name + " (hit rate: {:.1f}%)".format(100 - self.error_rate)

# A message suggestion is used to tell the user something about a
# column if we can't create or find a type suggestion.
class MessageSuggestion(object):
    def __init__(self, message):
        self.message = message
    def __repr__(self):
        return self.message

class Validation(object):
    def __init__(self, df):
        self.columns = {
            c : Column(c, [type_specs[c].validation]) for c in list(type_specs)
        }
        schema_list = []
        column_list = []
        unknown_column_list = []
        for col in list(df.columns):
            if self.columns.get(col) and is_string_dtype(df[col]):
                column_list.append(col)
                schema_list.append(self.columns.get(col))
            else:
                unknown_column_list.append(col)
        self.df = df[column_list]
        self.unknown_df = df[unknown_column_list]
        # Only create a Schema if we have any columns we want to validate.
        # (Schema raises an error if you create it with an empty list.)
        if (len(schema_list)) > 0:
            schema = Schema(schema_list)
            self.errors = schema.validate(self.df)
        else:
            self.errors = []
        self.suggestions = {
            c : self.generate_suggestions(c) for c in unknown_column_list
        }

    def generate_suggestions(self, column_name):
        if is_string_dtype(self.unknown_df[column_name]):
            suggestions = []
            for name, type_spec in type_specs.items():
                if type_spec.suggest:
                    s = self.generate_suggestion(type_spec, column_name)
                    if (s.error_rate < 50.0):
                        suggestions.append(s)
            return sorted(suggestions, key=lambda s: [s.error_rate, -s.type_spec.specificity])[:5]
        else:
            return [MessageSuggestion('This column should be of type string')]

    def generate_suggestion(self, type_spec, column_name):
        total_ct = self.unknown_df.shape[0]
        results = type_spec.validation.validate(self.unknown_df[column_name])
        error_ct = results[results == False].shape[0]
        p = 100 * float(error_ct) / float(total_ct)
        return TypeSuggestion(type_spec, p)

    def valid(self):
        if self.errors == []:
            return True
        else:
            return False

    def report(self):
        row_count = self.df.shape[0]
        report = {
            c : {
                'row_count': row_count,
                'error_count': 0,
                'row_indexes': [],
                'type_name': type_specs[c].name
            } for c in list(self.df.columns)
        }
        for e in self.errors:
            report[e.column]['error_count'] += 1
            report.get(e.column).get('row_indexes').append(e.row)

        return report

class Analytics(object):

    def __init__(self, inputs={}, config_file=None, region=None, env=None, key=None, username=None, password=None):
        self.C = load_config(config_file=config_file, region=region, env=env, key=key, username=username, password=password)
        self.key = self.C.get("API_KEY")
        self.prefix = True
        self.inputs = inputs
        self.sample_mode = False # Anchovy does not support sample mode

        # This is only used for validate and batch, so force sample_mode
        self.connectors = Connectors(config=self.C,
                                     inputs=self.inputs,
                                     sample_mode=True)

    def get(self, provider_name, query, default=None, inputs=None):
        return self.connectors.get(provider_name, query, default,
                                   inputs=inputs,
                                   shape="table", prefix=self.prefix)

    def data_function_append(self, name, inputs_dframe):
        return track_function(lambda: self.do_data_function_append(name, inputs_dframe),
                              self.C, "API : Python : Data Function Append",
                              { "name": name })

    def do_data_function_append(self, name, inputs_dframe):
        output = [None] * len(inputs_dframe)
        for idx, row in progressbar(inputs_dframe.iterrows()):
            inputs = dict([(key, row[key]) for key in row.keys()])
            output[idx] = inputs
            post = {
                "api_key": self.key,
                "inputs": inputs,
                "providers": [],
                "data_function_id": name
            }
            channel_url = self.C.get("BLACKFIN_URL") + "v2/execute"
            resp = requests.post(channel_url,
                                 data = json.dumps(post),
                                 headers={'Content-Type':'application/json'})
            body = resp.json()

            result = body['pipes']['data_function']['result']
            output[idx] = {**output[idx], **result}

        appended_dframe = pd.DataFrame.from_dict(output)
        sorted_columns = list(inputs_dframe.columns) + [x for x in appended_dframe.columns if x not in list(inputs_dframe.columns)]
        return appended_dframe[sorted_columns]

    def batch(self, *args, **kwargs):
        print("batch() is deprecated. Please use enrich() instead.", file=sys.stderr)

    # XXX Not available until Blackfin supports JWTs.
    def _sample(self, provider_names, inputs_dframe, validate=True):
        return track_function(lambda: self.do_batch(provider_names, inputs_dframe, validate=validate),
                              self.C, "API : Python : Sample",
                              { "provider_names": provider_names })

    def do_batch(self, provider_names, inputs_dframe, validate=True):
        print("Sample will only use the first 5 records of your dataframe", file=sys.stderr)
        inputs_dframe = inputs_dframe.head(5)

        if (validate):
            if (not self.validate_providers(provider_names, inputs_dframe)):
                return None

        for idx, row in progressbar(inputs_dframe.iterrows()):
            inputs = dict([(key, row[key]) for key in row.keys()])
            no_failues = True
            try:
                no_failures = self.connectors.fetch(provider_names, inputs)
            except DemystConnectorError as e:
                d = e.args[0]
                print("Failed to run batch %s because of %s. Contact support@demystdata.com for help."%(d['transaction_id'], d['message']), file=sys.stderr)
                return False

            if not no_failures:
                for provider_name in provider_names:
                    provider_error = self.connectors.cache_get_error(provider_name, inputs)
                    if provider_error:
                        print("Transaction with %s failed because of %s: %s. "%(provider_name, provider_error['type'], provider_error['message']), file=sys.stderr)

        output = [None] * len(inputs_dframe)
        for i, row in inputs_dframe.iterrows():
            inputs = dict([(key, row[key]) for key in row.keys()])
            output[i] = inputs # Initial dictionary
            for provider_name in provider_names:
                provider_data = self.connectors.get(provider_name, '', inputs=inputs, shape="table", prefix=True)
                if provider_data:
                    output[i] = {**output[i], **provider_data}

        appended_dframe = pd.DataFrame.from_dict(output)
        # Move inputs_dframe columns to the front of the dataframe
        sorted_columns = list(inputs_dframe.columns) + [x for x in appended_dframe.columns if x not in list(inputs_dframe.columns)]
        return appended_dframe[sorted_columns]

    # If preflight is True, will not actually run the batch, just
    # print info about credits.
    def enrich(self, provider_names, inputs_dframe, validate=True, preflight=False):
        return track_function(lambda: self.do_enrich(provider_names, inputs_dframe, validate=validate, preflight=preflight),
                              self.C, "API : Python : Enrich",
                              { "provider_names": provider_names })

    def enrich_credits(self, provider_names, inputs_dframe, validate=True):
        return self.enrich(provider_names, inputs_dframe, validate=validate, preflight=True)

    def do_enrich(self, provider_names, inputs_dframe, validate=True, preflight=False):
        print("Starting enrichment...")
        if (validate):
            if (not self.validate_providers(provider_names, inputs_dframe)):
                return None
        fd, temp_path = tempfile.mkstemp()
        try:
            inputs_dframe.to_csv(temp_path, index=False, header=False)
            return self.enrich_csv(provider_names, temp_path, list(inputs_dframe), preflight=preflight)
        finally:
            os.close(fd)

    def enrich_csv(self, provider_names, csv_file, columns, preflight=False):
        dict = self.get_presigned_url_and_s3_object_key()
        url = dict["presigned_url"]
        s3_key = dict["s3_object_key"]
        self.upload_file_to_presigned_url(csv_file, url)
        region_id = self.find_region_id(self.C.get("REGION"))
        input_id = self.create_batch(csv_file, s3_key, columns, region_id)
        run_batch_id = self.run_batch(provider_names, input_id, region_id, preflight=preflight)
        print("Enrich Job ID: " + str(run_batch_id))
        return run_batch_id

    def upload_file_to_presigned_url(self, csv_file, url):
        print("Uploading data...")
        with open(csv_file, "rb") as f:
            res = requests.put(url, data=f)
            if (res.status_code != 200):
                raise RuntimeError("Error while trying to upload file: " + res.text)

    def get_presigned_url_and_s3_object_key(self):
        res = self.C.auth_get(self.C.get("MANTA_URL") + "presigned_batch_upload_url")
        return res.json()

    def create_batch(self, csv_file, s3_key, columns, region_id):
        num_rows = self.count_lines_in_file(csv_file)
        input = {
            "aegean_batch_input": {
                "name": csv_file,
                "num_rows": num_rows,
                "region_id": region_id,
                "s3_object_key": s3_key,
                "headers": columns
            }
        }
        res = self.C.auth_post(self.C.get("MANTA_URL") + "aegean_batch_inputs", json=input)
        return res.json()["id"]

    def find_region_id(self, region_code):
        region_json = self.C.auth_get(self.C.get("MANTA_URL") + "list_regions").json()
        for region in region_json:
            if region["code"] == region_code:
                return region["id"]
        raise RuntimeError("Region not found: " + region_code)

    def run_batch(self, provider_names, input_id, region_id, preflight=False):
        provider_ids = [self.C.provider_name_to_id(name) for name in provider_names]
        # Send draft request to get credits info
        draft_input = {
            "aegean_batch_run": {
                "aegean_batch_input_id": input_id,
                "provider_version_ids": provider_ids,
                "region_id": region_id,
                "name": secrets.token_hex(32),
                "draft": True
            }
        }
        draft_res = self.C.auth_post(self.C.get("MANTA_URL") + "aegean_batch_runs",
                                     json=draft_input).json()
        org_credits = draft_res["organization"]["credit_balance"]
        run_credits = draft_res["estimated_credit_cost"]
        self.print_credits(draft_res)
        if preflight:
            # If we should only check credits, we are done now
            return draft_res["id"]
        else:
            # Send real request
            if (org_credits < run_credits):
                raise RuntimeError("Aborting due to insufficient credits.")
            else:
                input = {
                    "aegean_batch_run": {
                        "aegean_batch_input_id": input_id,
                        "provider_version_ids": provider_ids,
                        "region_id": region_id,
                        "name": secrets.token_hex(32)
                    }
                }
                res = self.C.auth_post(self.C.get("MANTA_URL") + "aegean_batch_runs",
                                       json=input).json()
                return res["id"]

    def print_credits(self, batch_run_resp):
        if self.sample_mode:
            print("This enrichment will cost 0 credits because you are using sample data.",
                  file=sys.stderr)
            print("To switch to live mode, please set sample_mode=False in the Analytics class.",
                  file=sys.stderr)
        else:
            org_credits = "{:n}".format(batch_run_resp["organization"]["credit_balance"])
            run_credits = "{:n}".format(batch_run_resp["estimated_credit_cost"])
            print("This enrichment will use " + run_credits + " credits.", file=sys.stderr)
            print("Your organization currently has " + org_credits + " credits.", file=sys.stderr)

    def count_lines_in_file(self, fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1

    # Return true if all providers are done, false otherwise.
    def enrich_status(self, id, notebook=True):
        resp_json = self.fetch_enrich_status(id)
        if notebook:
            print(self.enrich_status_message(resp_json))
        return self.enrich_status_finished(resp_json)

    def enrich_wait(self, id):
        # This progress bar is fake, but still an effective UI
        # element.  It starts at 50% and stays there until finished,
        # then we set it to 100%.
        bar = widgets.IntProgress(value=1,min=0,max=2)
        label = widgets.Label("Checking status...")
        display(bar)
        display(label)
        while True:
            resp_json = self.fetch_enrich_status(id)
            if self.enrich_status_finished(resp_json):
                label.value = "Done."
                bar.value = 2
                return
            else:
                label.value = self.enrich_status_message(resp_json)
                sleep(5)

    def fetch_enrich_status(self, id):
        return self.C.auth_get(self.C.get("MANTA_URL") + "aegean_batch_runs/" + str(id)).json()

    # Check that all export links are available
    def enrich_status_finished(self, resp_json):
        for provider in resp_json["batch_run_provider_versions"]:
            if not provider["most_recent_export_link"]:
                return False
        return True

    # For each provider X, create a message like "X (55%)" or "X
    # (exporting)" or "X (done)".
    def enrich_status_message(self, resp_json):
        num_rows = resp_json["num_rows"]
        messages = []
        for provider in resp_json["batch_run_provider_versions"]:
            name = provider["table_provider"]["name"]
            rows_completed = provider["rows_completed"] or 0
            status = "done"
            if rows_completed < num_rows:
                status = "{:.1f}%".format(100 * float(rows_completed) / float(num_rows))
            elif not provider["most_recent_export_link"]:
                status = "exporting"
            messages.append(name + " (" + status + ")")
        return ", ".join(messages)

    def enrich_download(self, id, block_until_complete=True):
        if (block_until_complete):
            self.enrich_wait(id)

        resp_json = self.C.auth_get(self.C.get("MANTA_URL") + "aegean_batch_runs/" + str(id)).json()
        provider_results = resp_json["batch_run_provider_versions"]
        df = pd.DataFrame()
        returned_inputs = None
        for r in provider_results:
            export_link = r["most_recent_export_link"]
            provider_name = r["table_provider"]["name"]
            if export_link:
                provider_df = pd.read_csv(export_link, na_filter=False)
                input_cols = [c for c in provider_df.columns if c.startswith("inputs.")]
                # Extract inputs passed through by provider
                if returned_inputs is None:
                    returned_inputs = provider_df[input_cols]
                # Drop the inputs from the dataframe
                provider_df = provider_df.drop(input_cols, axis="columns")
                # Prefix all remaining columns with provider name
                provider_df = provider_df.rename(lambda col: provider_name + "." + col,
                                                 axis="columns")
                df = pd.concat([df, provider_df], axis="columns")
            else:
                print("Provider " +provider_name+ " has not finished enrichment and will not be included." , file=sys.stderr)
        if df.empty:
            print("No results were returned from this enrichment", file=sys.stderr)
        # Add inputs to final dataframe
        df = pd.concat([returned_inputs, df], axis="columns")
        return df

    def search(self, inputs=None, tags=None, notebook=True, strict=False):
        if isinstance(inputs, pd.DataFrame):
            inputs = list(inputs)
        return track_function(lambda: self.do_search(inputs=inputs, tags=tags, notebook=notebook, strict=strict),
                              self.C, "API : Python : Search",
                              { "tags": tags, "notebook": notebook, "inputs": inputs })

    def do_search(self, inputs=None, tags=None, notebook=True, strict=False):
        params = {
            'inputs[]': inputs,
            'tags[]': tags
        }
        murl = "%stable_providers/match_given_input.json" % self.C.get("MANTA_URL")
        response = self.C.auth_get(murl, params=params)
        connectors = response.json()

        if strict:
            connectors = self.filter_connectors_strictly(connectors, inputs)
        if (notebook):
            doc, tag, text, line = Doc().ttl()
            table ={}
            if connectors == []:
                line('p', "Sorry, we couldn't find any Data Products that matched this input.", style='font-style: italic;')
            else:
                for connector in connectors:
                    connector_inputs = list(set(list(itertools.chain(*connector['required_input']))))
                    with tag('div', style=''):
                        with tag('div', style="pading:10px;"):
                            with tag('div',style='padding:5px'):
                                with tag('h1'):
                                    doc.stag('img', height=30, width=30, src=connector['data_source_logo_url'], style="display:inline-block")
                                    text(" " + connector['data_source_name'])
                                line('pre', connector['name'], style='')
                                with tag('p'):
                                    if connector['description']:
                                        line('em', connector['description'])
                            with tag('div', style='padding: 5px;'):
                                with tag('table'):
                                    with tag('tr'):
                                        with tag('th'):
                                            text(" ")
                                        for i in range(len(connector_inputs)):
                                            with tag('th'):
                                                text(connector_inputs[i])
                                    for ri_idx, required_inputs in enumerate(connector['required_input']):

                                        with tag('tr'):
                                            with tag('td'):
                                                text(f'Option {ri_idx+1}')
                                            for i in range(len(connector_inputs)):
                                                with tag('td'):
                                                    with tag('span', style="font-size: 20px;"):
                                                        if connector_inputs[i] in required_inputs:
                                                            if connector_inputs[i] in inputs:
                                                                text("☒")
                                                            else:
                                                                text("☐")
                                                        else:
                                                            text(" ")

            return HTML(doc.getvalue())
        else:
            return connectors

    def filter_connectors_strictly(self, connectors, inputs):
        input_set = set(inputs)
        def any_required_input_matches(connector):
            return len([r for r in connector["required_input"] if set(r).issubset(input_set)]) > 0
        return [c for c in connectors if any_required_input_matches(c)]

    def load_demo_csv(self):
        return pd.read_csv(os.path.join(os.path.dirname(__file__), "sample/website.csv"))

    def validate_providers(self, provider_names, inputs_dframe, return_errors=False):
        inputs_one_dframe = inputs_dframe[:1]
        inputs = inputs_one_dframe.to_dict('records')[0]

        try:
            success = self.connectors.fetch(provider_names, inputs, sample_mode=True)
        except DemystConnectorError as e:
            d = e.args[0]
            print("Failed to run %s because of %s. Contact support@demystdata.com for help."%(d['transaction_id'], d['message']), file=sys.stderr)
            return False

        errors=[]
        if (not success):
            for provider_name in provider_names:
                if self.connectors.cache_get_error(provider_name, inputs):
                    error = self.connectors.cache_get_error(provider_name, inputs)
                    error['provider_name'] = provider_name
                    if (return_errors):
                        errors.append(error)
                    else:
                        print('%s: %s'% (provider_name, error['message']), file=sys.stderr)

        if (return_errors):
            return errors
        else:
            return success

    def validate(self, df, providers=None, report=True, verbose=False):
        v = Validation(df)

        providers_validate = True
        provider_errors = []
        if (providers):
            provider_errors = self.validate_providers(providers, df, return_errors=True)
            if provider_errors:
                providers_validate = False

        # XXX The boolean  return for v.validate doesn't make too much senseself.
        # XXX An input file will rarely have 100% detection
        if not report:
            return v.valid() and providers_validate
        else:
            report = v.report()
            doc, tag, text, line = Doc().ttl()
            if (df.shape[0] == 0):
                line('p', 'The DataFrame you passed in is empty.')
            else:
                line('h4', 'Input Types Detected')
                with tag('table'):
                    with tag('tr'):
                        with tag('th'):
                            text('Column')
                        with tag('th'):
                            text('Type')
                        with tag('th'):
                            text('Error %')
                        #with tag('th'):
                        #    text('Rows')
                    for column_name in report.keys():
                        with tag('tr'):
                            with tag('td'):
                                text(column_name)
                            with tag('td'):
                                text(report.get(column_name).get('type_name'))
                            with tag('td'):
                                p = 100 * float(report.get(column_name).get('error_count')) / float(report.get(column_name).get('row_count'))
                                text("{:.1f}".format(p))
                            #with tag('td'):
                            #    text(",".join(map(str, report.get(column_name).get('row_indexes'))))
                if len(v.suggestions) > 0:
                    line('h4', 'Input Types Suggested')
                    with tag('table'):
                        with tag('tr'):
                            with tag('th'):
                                text('Column')
                            with tag('th'):
                                text('Suggestions')
                        for column_name, suggestions in v.suggestions.items():
                            with tag('tr'):
                                with tag('td'):
                                    text(column_name)
                                with tag('td'):
                                    if (len(suggestions) > 0):
                                        text(", ".join(map(str, suggestions)))
                                    else:
                                        with tag('em'):
                                            text('No suggestions found for this column')
                if providers:
                    line('h4', 'Providers')
                    with tag('table'):
                        with tag('tr'):
                            with tag('th'):
                                text('Provider')
                            with tag('th'):
                                text('Validate?')
                            with tag('th'):
                                text('Errors')
                        for p in providers:
                            match = next((l for l in provider_errors if l['provider_name'] == p), None)
                            with tag('tr'):
                                with tag('td'):
                                    text(p)
                                if match:
                                    with tag('td'):
                                        text('False')
                                    with tag('td'):
                                        text(match['message'])
                                else:
                                    with tag('td'):
                                        text('True')
                                    with tag('td'):
                                        text('')

            return HTML(doc.getvalue())

    def credits(self):
        headers = { "Accept": "application/json" }
        resp_json = self.C.auth_get(self.C.get("MANTA_URL") + "organization", headers=headers).json()
        return resp_json["credit_balance"]
