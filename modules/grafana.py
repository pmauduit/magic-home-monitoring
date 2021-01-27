import time
import logging
import requests
from grafana_api.grafana_face import GrafanaFace


class grafana:
    def __init__(self, host, token, datasources, probes, ok_value):
        self._host = host
        self._token = token
        ds = datasources.split(",")
        self._datasource_id = []
        self._grafana_api = GrafanaFace(auth=self._token, host=self._host)
        for i in ds:
            dsource = self._grafana_api.datasource.get_datasource_by_name(i)
            self._datasource_id.append(dsource['id'])
        self._probes = probes.split(",")
        self._ok_value = int(ok_value)

    def _get_current_status(self, datasource_id, probe):
        ts = time.time()
        ts_1min_ago = ts - 60
        http_headers = {'Authorization': "Bearer {}".format(self._token)}
        query = "https://{}/api/datasources/proxy/{}/api/v1/query_range?query=sum({})&start={}&end={}&step={}" \
            .format(self._host, datasource_id, probe, ts_1min_ago, ts, 30)
        resp = requests.get(query, headers=http_headers)
        resp_json = resp.json()
        ret = 0
        for value in resp_json['data']['result'][0]['values']:
            cur_ts, val = value
            val = int(val)
            ret += val
        return ret

    # Ideally we should have a separate JIRA module, but since the info
    # is already present in the grafana dashboard, I'd prefer to get the
    # info from there.
    def check_jira_issues(self):
        ts = int(time.time()) - 60
        http_headers = {'Authorization': "Bearer {}".format(self._token)}
        query = "https://{}/api/datasources/proxy/82/api/v1/query?query=high_prio_jira_tickets&time={}" \
            .format(self._host, ts)
        resp = requests.get(query, headers=http_headers)
        resp_json = resp.json()
        # It normally returns only one value
        return int(resp_json['data']['result'][0]['value'][1]) == 0

    def compute_status(self):
        try:
            result = 0
            for ds in self._datasource_id:
                for p in self._probes:
                    result += self._get_current_status(ds, p)
            return result == self._ok_value and self.check_jira_issues()
        except Exception as e:
            logging.error("Unable to connect to Grafana", exc_info=True)
            return True
