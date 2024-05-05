import requests, yaml, json

class cluster:
    def __init__(self):
        self.cfg = self.load_cfg()

    def update_nodes(self):
        res = self.request(method="GET",path='/nodes')
        self.nodes = json.loads(res.text)

    def update_state(self):
        self.update_nodes()

    def load_cfg(self):
        with open('proxmox-config.yaml', 'r') as file:
            return yaml.safe_load(file)
    def print_cfg(self):
        print(yaml.dump(self.cfg))

    def request(self, method, path):
        url = f"https://{self.cfg['api-url']}:{self.cfg['port']}/api2/json{path}"
        headers = {'Authorization': 'PVEAPIToken='+self.cfg['user']+'@pam!'+ self.cfg['apiToken']['name'] +'=' + self.cfg['apiToken']['value']}
        payload = ""
        print(url)
        print(headers)
        res=requests.request("GET", url, data=payload, verify=self.cfg['ssl'], headers=headers)
        print("status:" + str(res.status_code))
        print(res.text)
        return res

    def create_vm(self, definitionFile):
        return self.nodes[node]

homelab = cluster()
homelab.request(method="GET",path='/nodes')