import datetime
import requests
import os
import json
import urllib.parse


class LoggerApi:
    def __init__(self, url, estado):

        mode = os.environ['MODE']

        self.url = url
        self.estado = estado
        self.APIURL = os.getenv("APIURL")

        if mode != 'TEST':
            self.routes = self.obtener_indices_pasos()

    def informar(self, msg):
        data = {'nombre': self.estado,
                'fecha': datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                'observaciones': msg}

        requests.post(self.url,
                      headers={"Content-Type": "application/json",
                               "Authorization": self.obtener_credenciales_pipelines()},
                      json=data)

    def cancel_job(self, urld):
        urld = urld.rstrip('pasosEjecucion/')

        # build url endpoint with the ID of the step and the process
        data = {'estado': 'Erroneo'}

        mode = os.environ['MODE']

        if mode not in ['TEST']:
            # POST data
            r = requests.delete(urld, headers={"Authorization": self.obtener_credenciales_pipelines()}, data=data)
            print(r)

    def iniciar_paso(self, name, analysis, log):
        if name in ['TagVariants', 'Gender_check', 'Report_client', 'report_client',
                    'FindAlu', 'AnnotatePGx', 'MapAlu', 'CleanBamAlu', 'Homopolymer']:
            return
        # build data
        data = {'fecha': datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

        # build url endpoint with the ID of the step and the process
        url = urllib.parse.urljoin(self.url, self.routes[analysis][name] + '/inicio')

        # POST data
        r = requests.post(url, headers={"Content-Type": "application/json",
                                        "Authorization": self.obtener_credenciales_pipelines()},
                          json=data)

        # log.debug(f"POST [{name}]: data -> {data}")
        log.debug(f"#[START]: API-POST [{name}]: status -> {r.status_code}; url -> {url}")

    def finalizar_paso(self, name, analysis, log):
        if name in ['TagVariants', 'Gender_check', 'Report_client', 'report_client',
                    'FindAlu', 'AnnotatePGx', 'MapAlu', 'CleanBamAlu', 'Homopolymer']:
            return
        # build data
        data = {'fecha': datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

        # build url endpoint with the ID of the step and the process
        url = urllib.parse.urljoin(self.url, self.routes[analysis][name] + '/finalizacion')

        # POST data
        r = requests.post(url,
                          headers={"Content-Type": "application/json",
                                   "Authorization": self.obtener_credenciales_pipelines()},
                          json=data)

        # log.debug(f"POST [{name}]: data -> {data}")
        log.debug(f"#[END]: API-POST [{name}]: status -> {r.status_code}; url -> {url}")

    def obtener_indices_pasos(self):
        # Select the endpoint direction from which get the data

        api_url = f'{self.APIURL}/pipelineapi/v1/pipelines'

        # Process the get request to the API
        r = requests.get(api_url, headers={
                                           "Content-Type": "application/json",
                                           "Authorization": self.obtener_credenciales_pipelines()
                                           })

        data = json.loads(r.text)

        # Filter out inactive pipelines
        active_pipelines = []

        for pipeline in data:
            if pipeline['estado'] != 'activa':
                continue

            # Add the active pipeline to the list
            active_pipelines.append(pipeline)

        routes = {}

        # For each of the pipelines, get the data of each step, and create a
        # dictionary with it
        for pipeline in active_pipelines:
            pipeline_id = str(pipeline['id'])

            r = requests.get(api_url + '/' + pipeline_id,
                             headers={
                                      "Content-Type": "application/json",
                                      "Authorization": self.obtener_credenciales_pipelines()
                                      })

            data = json.loads(r.text)

            routes[pipeline['nombre']] = {step['nombre']: str(step['id']) for step in data['pasos']}

        return routes

    def mandar_path_resultados(self, config):
        # Build data
        data = config['results']

        # build url endpoint
        url = self.url.rstrip('pasosEjecucion/') + '/resultados'

        # POST data
        r = requests.post(url, headers={"Content-Type": "application/json",
                                        "Authorization": self.obtener_credenciales_pipelines()}, json=data)

    def obtener_credenciales_pipelines(self):

        api_url = f'{self.APIURL}/seguridadapi/v1/login'

        data = {
                "usuario": "pipelineuser",
                "password": "pipelinepassword",
                "dominio": "pipelineapi"
                }

        r = requests.post(api_url, headers={"Content-Type": "application/json"}, json = data)
        auth = r.content.decode('utf-8')
        return "Bearer " + auth

    def empty_cache(self, mode):
        # print('#[LOG]: emptying cache')
        if mode != 'TEST':
            try:
                os.popen("sh -c 'echo 3 > /proc/sys/vm/drop_caches'", 'w')
            except:
                print("#[WARN]: Could not clean the cache (do python have root privileges?)")
