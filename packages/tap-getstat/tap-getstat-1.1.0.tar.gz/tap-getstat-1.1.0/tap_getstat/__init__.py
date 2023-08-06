#!/usr/bin/env python3

import datetime
import sys
import os
import time
import requests
import singer
from singer import Transformer, utils

import pytz
import backoff

PER_PAGE = 100

def yesterday():
    return datetime.datetime.today() - datetime.timedelta(1)

CONFIG = {
    'api_url': "https://{}.getstat.com/api/v2/{}",
    'api_key': None,
    'start_date': None,
    'subdomain': None,
    "end_date": yesterday(),
    'stream_url': "https://{}.getstat.com/bulk_reports/stream_report/{}"
}

STATE = {}

class TimeoutException(Exception):
    pass

def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)

def load_schema(entity):
    return utils.load_json(get_abs_path("schemas/{}.json".format(entity)))

def daterange(start_date, end_date):
    """ Yield and iterable of dates from start to end, inclusive, represented as "%Y-%m-%d" strings.
    Arguments:
    start_date: a string or datetime representing the first date to yield
    end_date: a string or datetime representing the last date to yield
    """
    if isinstance(start_date, str):
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    if isinstance(end_date, str):
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    for n in range(int ((end_date - start_date).days + 1)):
        yield (start_date + datetime.timedelta(n)).strftime('%Y-%m-%d')

RESOURCES = {
    'projects': {
        'endpoint': '/projects/list',
        'schema': load_schema('projects'),
        'key_properties': ['Id'],
    },
    'sites': {
        'endpoint': '/sites/list?project_id={}',
        'schema': load_schema('sites'),
        'key_properties': ['Id'],
    },
    'tags': {
        'endpoint': '/tags/list?site_id={}',
        'schema': load_schema('tags'),
        'key_properties': ['site_id','Id'],
    },
    'keywords': {
        'endpoint': '/keywords/list?site_id={}',
        'schema': load_schema('keywords'),
        'key_properties': ['site_id','Id'],
    },
    'rankings': {
        'endpoint': '/bulk/ranks?site_id={}',
        'schema': load_schema('rankings'),
        'key_properties': ['site_id','Id'],
    },
		'sov': {
				'endpoint': '/sites/sov?id={}',
				'schema': load_schema('sov'),
				'key_properties': ['date'],
		},
    'status': {
        'endpoint': '/bulk/status?id={}'
    },
    'job_stream': {
        'endpoint': 'bulk_report/stream_report/{}'
    }
}


LOGGER = singer.get_logger()
SESSION = requests.Session()

def get_url(entity, pid):
    return CONFIG['api_url'].format(CONFIG['subdomain'], CONFIG['api_key']) + RESOURCES[entity]['endpoint'].format(pid)


def get_start(entity):
    if entity not in STATE:
        STATE[entity] = CONFIG['start_date']

    return STATE[entity]


@backoff.on_exception(backoff.expo,
                      (requests.exceptions.RequestException),
                      max_tries=5,
                      giveup=lambda e: e.response is not None and 400 <= e.response.status_code < 500, # pylint: disable=line-too-long
                      factor=2)
def request(url, params=None):
    params = params or {}

    headers = {}
    if 'user_agent' in CONFIG:
        headers['User-Agent'] = CONFIG['user_agent']

    req = requests.Request('GET', url, params=params, headers=headers).prepare()
    LOGGER.info("GET {}".format(req.url))
    resp = SESSION.send(req)

    if resp.status_code >= 400:
        LOGGER.critical(
            "Error making request to getstat.com API: GET {} [{} - {}]".format(
                req.url, resp.status_code, resp.content))
        sys.exit(1)

    return resp


def gen_request(url, params):
    resp = request(url, params)

    result = resp.json()

    result = result['Response']['Result']

    if not isinstance(result, list):
        result = [result]

    if 'nextpage' in resp.json()['Response'].keys():
        nextPageUrl = CONFIG['api_url'].format(CONFIG['subdomain'], CONFIG['api_key']) + resp.json()['Response']['nextpage']
        for rec in list(gen_request(nextPageUrl, None)):
            result.append(rec)

    for res in result:
        yield res

def gen_sov_request(url, params):
		resp = request(url, params)

		result = resp.json()

		result = result['Response']['ShareOfVoice']

		if not isinstance(result, list):
				result = [result]

		if 'nextpage' in resp.json()['Response'].keys():
				nextPageUrl = CONFIG['api_url'].format(CONFIG['subdomain'], CONFIG['api_key']) + resp.json()['Response']['nextpage']
				for rec in list(gen_sov_request(nextPageUrl, None)):
						result.append(rec)

		for res in result:
				yield res

def gen_bulk_request(url, params):
    resp = request(url, params)

    result = resp.json()

    result = result['Response']['Result']['Id']

    return result

def is_job_done(job_id):
    url = get_url('status', job_id)

    tries = 0
    while True:
        if tries == 5:
            raise TimeoutException
        time.sleep(30)
        
        resp = request(url, {'format': 'json'})
        result = resp.json()['Response']['Result']

        if result['Status'] == 'Completed':
            return True
        tries += 1

def get_job_result(job_id):
    stream_url = CONFIG['stream_url'].format(CONFIG['subdomain'], job_id)

    resp = request(stream_url, {'key': CONFIG['api_key']})

    result = resp.json()
    result = result['Response']['Project']['Site']['Keyword']

    if not isinstance(result, list):
        result = [result]

    for res in result:
        yield res


def format_timestamp_make_null(data, typ, schema):
    result = data
    if typ == 'string' and schema.get('format') == 'date-time':
        result = datetime.datetime.strptime(data, "%Y-%m-%d")
    if typ == 'null' and data in ('N/A', 'none', '-', '-1'):
        result = ''
    if typ == 'array' and not isinstance(data, list):
        result = [data]

    return result

def sync_projects():
    url = get_url("projects", None)
    with Transformer(pre_hook=format_timestamp_make_null) as transformer:
        for row in gen_request(url,  {"format": "json"}):
            transformed_row = transformer.transform(row, RESOURCES["projects"]["schema"])
            singer.write_record("projects", transformed_row, time_extracted=utils.now())


def sync_sites(project_id):
    url = get_url("sites", project_id)
    with Transformer(pre_hook=format_timestamp_make_null) as transformer:
        for row in gen_request(url, {"format": "json"}):
            transformed_row = transformer.transform(row, RESOURCES["sites"]["schema"])
            singer.write_record("sites", transformed_row, time_extracted=utils.now())


def sync_tags(project_id, site_id):
    url = get_url("tags", site_id)
    with Transformer(pre_hook=format_timestamp_make_null) as transformer:
        for row in gen_request(url, {"format": "json", "results":"5000"}):
            if row["Keywords"] == 'none':
              row["Keywords"] = {"Id": []}
            row = dict(Id = row["Id"], Tag = row["Tag"], Type = row["Type"], Keywords = row['Keywords'])
            transformed_row = transformer.transform(row, RESOURCES["tags"]["schema"])

            singer.write_record("tags", transformed_row, time_extracted=utils.now())

def sync_keywords(project_id, site_id):
    url = get_url("keywords", site_id)
    with Transformer(pre_hook=format_timestamp_make_null) as transformer:
        for row in gen_request(url, {"format": "json", "results":"5000"}):
            transformed_row = transformer.transform(row, RESOURCES["keywords"]["schema"])

            singer.write_record("keywords", transformed_row, time_extracted=utils.now())

def sync_rankings(project_id, site_id):
    url = get_url("rankings", site_id)
    with Transformer(pre_hook=format_timestamp_make_null) as transformer:
        jobs = []
        for date in daterange(CONFIG['start_date'], CONFIG['end_date']):
            jobs.append(gen_bulk_request(url, {"format": "json", "date": date}))

        for job in jobs:
            if is_job_done(job):
                for row in get_job_result(job):
                    transformed_row = transformer.transform(row, RESOURCES["rankings"]["schema"])
                    singer.write_record("rankings", transformed_row, time_extracted=utils.now())

def sync_sov(project_id, site_id):
		url = get_url("sov", site_id)
		with Transformer(pre_hook=format_timestamp_make_null) as transformer:
			for row in gen_sov_request(url, {"format": "json", "from_date": CONFIG['start_date'], "to_date": CONFIG['end_date'], "results": "365"}):
				transformed_row = transformer.transform(row, RESOURCES["sov"]["schema"])

				singer.write_record("sov", transformed_row, time_extracted=utils.now())

def sync_project(project_id, site_id):
		time_extracted = utils.now()

		state_key = "project_id"


		# sync_projects()
		# sync_sites(project_id)
		# sync_tags(project_id, site_id)
		# sync_keywords(project_id, site_id)
		# sync_rankings(project_id, site_id)
		sync_sov(project_id, site_id)

		utils.update_state(STATE, state_key, time_extracted)
		singer.write_state(STATE)


def do_sync(project_id, site_id):
    LOGGER.info("Starting sync")

    for resource, config in RESOURCES.items():
        if config.get('schema'):
            singer.write_schema(resource, config['schema'], config['key_properties'])

    sync_project(project_id, site_id)

    LOGGER.info("Sync complete")


def main_impl():
    args = utils.parse_args(["api_key", "subdomain", "project_id", "site_id", "start_date", "end_date"])

    CONFIG.update(args.config)

    if args.state:
        STATE.update(args.state)

    do_sync(CONFIG['project_id'], CONFIG['site_id'])


def main():
    try:
        main_impl()
    except Exception as exc:
        LOGGER.critical(exc)
        raise exc


if __name__ == '__main__':
    main()
