from jinja2 import Template
import requests
from os.path import basename
import urllib

url_template = """http://go/vpxhw-quality?{{jobIds}}

{% if encoder %}
  Choose {% for e in encoder %}
  {{ e }}{% endfor %}
  in encoder selection box (top one on the left)
{% endif %}
{% if model_name %}
  Pick '{{model_name}}' in tags filter (second one from the top)
{% endif %}
"""


class DashboardUrl(object):

  def __init__(self):
    super(DashboardUrl, self).__init__()

    self._encoder = []
    self._model_name = None
    self._jobIds = []

  def add_single_job(self, commit, encoder, usecase, test_suite, model_name):
    self._encoder.append(' '.join((
        encoder,
        usecase,
    )))
    self._model_name = model_name

    r = requests.post(
        'http://35.241.37.91/be/locate/single',
        data={
            'commit': commit,
            'encoder': encoder,
            'usecase': usecase,
            'test_suite': basename(test_suite),
            'model_name': model_name,
            'FPGA': '0',
        })

    if r.status_code == requests.codes.ok:
      self._jobIds.append(r.text)

  def add_latest_job(self, encoder, usecase, test_suite, model_name=None):
    self._encoder.append(' '.join((
        encoder,
        usecase,
    )))

    data = {
        'encoder': encoder,
        'usecase': usecase,
        'test_suite': basename(test_suite),
        'FPGA': '0',
    }

    if model_name:
      data['model_name'] = model_name

    r = requests.post('http://35.241.37.91/be/locate/latest', data=data)

    if r.status_code == requests.codes.ok:
      self._jobIds.append(r.text)

  def get_dashboard_url(self):
    template = Template(url_template)

    jobIdsString = '&'.join(
        ['job=' + urllib.quote_plus(id) for id in self._jobIds])
    return template.render({
        'jobIds': jobIdsString,
        'encoder': self._encoder,
        'model_name': self._model_name
    })
