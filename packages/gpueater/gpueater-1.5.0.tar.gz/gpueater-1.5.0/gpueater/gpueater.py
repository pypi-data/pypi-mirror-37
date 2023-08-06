import tempfile
import os
import requests
import json
import hashlib

G_GPUEATER_URL = "https://www.gpueater.com"

if 'GPUEATER_URL' in os.environ:
    G_GPUEATER_URL = os.environ['GPUEATER_URL']


G_HOMEDIR       = os.path.expanduser("~")
G_TMPDIR        = tempfile.gettempdir()
G_COOKIE        = os.path.join(G_TMPDIR,"gpueater_cookie.txt")
G_LOGIN_HASH    = os.path.join(G_TMPDIR,"gpueater_login_hash.txt")
G_CONFIG        = None



try:
    G_CONFIG = json.loads(open(".eater").read())
except:
    try:
        G_CONFIG = json.loads(open(os.path.join(G_HOMEDIR,".eater")).read())
    except:
        fp = open(os.path.join(G_HOMEDIR,".eater"),"w")
        fp.write('{"gpueater":{"email":"[Your email address]","password":"[Your password]"}}')
        fp.close
        raise Exception("\n\n Error: You must define config to "+os.path.join(G_HOMEDIR,".eater")+" json file.")

if G_CONFIG['gpueater']['email'] == "[Your email address]":
    raise Exception("\n\n Error: Invalid email\n  You must define config to "+os.path.join(G_HOMEDIR,".eater")+" json file.")

if G_CONFIG['gpueater']['password'] == "[Your password]":
    raise Exception("\n\n Error: Invalid password\n  You must define config to "+os.path.join(G_HOMEDIR,".eater")+" json file.")


G_HEADERS = {'User-Agent': 'PythonAPI'}




try:
    G_HEADERS['cookie'] = None
    try:
        cached_hash = open(G_LOGIN_HASH).read()

        hash = hashlib.sha256(json.dumps(G_CONFIG).encode('UTF-8')).hexdigest()
        if hash == cached_hash:
            G_HEADERS['cookie'] = open(G_COOKIE).read()
    except:
        pass
except:
    print(G_HEADERS)

def func_get(api,required_fields=[],query={}, e=None, try_cnt=2):
    if try_cnt <= 0: raise e
    for v in required_fields:
        if v not in query:
            print("Required field => \"" + v + "\"")
            raise "Required field"
    j = None
    try:
        res = requests.get(G_GPUEATER_URL+api,headers=G_HEADERS,params=query)
        j = json.loads(res.text)
    except Exception as e:
        #print(res.text)
        if "session_timeout" in res.url:
            relogin()
        return func_get(api, required_fields, query, e, try_cnt-1)

    if 'error' in j and j['error'] is not None:
        print(j)
        raise j['error']
    return j['data']

def func_post(api,required_fields=[],form={}, e=None, try_cnt=2):
    if try_cnt <= 0: raise e
    for v in required_fields:
        if v not in form:
            print("Required field => \"" + v + "\"")
            raise "Required field"
    j = None
    try:
        res = requests.post(G_GPUEATER_URL+api,headers=G_HEADERS,data=form)
        j = json.loads(res.text)
    except Exception as e:
        #print(form)
        #print(res.text)
        if "session_timeout" in res.url:
            relogin()

        return func_post(api, required_fields, form, e, try_cnt-1)

    if 'error' in j and j['error'] is not None:
        print(j)
        raise j['error']
    return j['data']

def relogin():
    print("relogin")
    res = requests.post(G_GPUEATER_URL+"/api_login",headers=G_HEADERS,data={'email':G_CONFIG['gpueater']['email'],'password':G_CONFIG['gpueater']['password']})
    j = json.loads(res.text)
    if 'set-cookie' in res.headers:
        G_HEADERS['cookie'] = res.headers['set-cookie']
        with open(G_COOKIE,"w") as f:
            f.write(G_HEADERS['cookie'])
        with open(G_LOGIN_HASH,"w") as f:
            f.write(hashlib.sha256(json.dumps(G_CONFIG).encode('UTF-8')).hexdigest())
    return j


class ProductsResnpose:
    def __init__(self,res):
        self.images = res['images']
        self.ssh_keys = res['ssh_keys']
        self.products = res['products']

    def find_image(self,name):
        data = self.images
        for k in data:
            if data[k]['name'] == name:
                return data[k]
        return None

    def find_product(self,name):
        data = self.products
        for d in data:
            if d['name'] == name:
                return d
        return None

    def find_ssh_key(self,name):
        data = self.ssh_keys
        for d in data:
            if d['name'] == name:
                return d
        return None

def ___________image___________(): pass
def image_list(): return func_get("/console/servers/images",[],{})
def registered_image_list(): return func_get("/console/servers/registered_image_list",[],{})  #@
def create_image(form): return func_post("/console/servers/create_user_defined_image",['instance_id','image_name'],form)  #@
def delete_image(form): return func_post("/console/servers/delete_user_defined_image",['fingerprint'],form)  #@
def snapshot_instance(form): raise "Not implemented yet"
def delete_snapshot(form): raise "Not implemented yet"
def test_image():
    print(image_list())

def ___________ssh_key___________(): pass
def ssh_key_list(): return func_get("/console/servers/ssh_keys",[],{})
def generate_ssh_key(): return func_get("/console/servers/ssh_key_gen",[],{})
def register_ssh_key(form): return func_post("/console/servers/register_ssh_key",['name','public_key'],form)
def delete_ssh_key(form): return func_post("/console/servers/delete_ssh_key",['id'],form)

def test_ssh_key():
    ssh_key_name = "my_ssh_key2_for_python"

    keys = ssh_key_list()
    for key in keys:
        if key["name"] == ssh_key_name:
            delete_ssh_key(key)

    k = generate_ssh_key()
    print(register_ssh_key({"name":ssh_key_name,"public_key":k["public_key"]}))

    fp = open(os.path.join(G_HOMEDIR,".ssh",ssh_key_name+".pem"),"w")
    fp.write(k["private_key"])
    fp.close()
    print(ssh_key_list())

    pass

def ___________instance___________(): pass
def ondemand_list(): return ProductsResnpose(func_get("/console/servers/ondemand_launch_list",[],{})) #@
def subscription_list(): raise "Not implemented yet"
def launch_ondemand_instance(form): return func_post("/console/servers/launch_ondemand_instance",['product_id','image','ssh_key_id','tag'],form)  #@
def launch_subcription_instance(form): raise "Not implemented yet"
def instance_list(): return func_get("/console/servers/instance_list",[],{})  #@
def change_instance_tag(form): return func_post("/console/servers/force_terminate",['instance_id','machine_resource_id'],form)  #@
def start_instance(form): return func_post("/console/servers/start",['instance_id','machine_resource_id'],form)  #@
def stop_instance(form): return func_post("/console/servers/stop",['instance_id','machine_resource_id'],form)  #@
def restart_instance(form): stop_instance(form); return start_instance(form);  #@
def terminate_instance(form): return func_post("/console/servers/force_terminate",['instance_id','machine_resource_id'],form)  #@
def emergency_restart_instance(form): return func_post("/console/servers/emergency_restart",['instance_id','machine_resource_id'],form)  #@

def test_instance():
    ssh_key_name = "my_ssh_key2_for_python"

    instances = instance_list()
    for instance in instances:
        print(instance)
        terminate_instance(instance)

    pd      = ondemand_list()
    key     = pd.find_ssh_key(ssh_key_name)
    image   = pd.find_image("Ubuntu16.04 x64")
    product = pd.find_product("n1.p400")

    print(launch_ondemand_instance({"tag":"TestTag","ssh_key_id":key["id"], "image":image["alias"],"product_id":product["id"]}))
    instances = instance_list()
    for instance in instances:
        print(instance)
        print(stop_instance(instance))
        print(start_instance(instance))
        print(restart_instance(instance))
    pass


def __________network__________(): pass
def port_list(form): return func_get("/console/servers/port_list",['instance_id'],form)  #@
def open_port(form): return func_post("/console/servers/add_port",['instance_id','connection_id','port'],form) #@
def close_port(form): return func_post("/console/servers/delete_port",['instance_id','connection_id','port'],form) #@
def renew_ipv4(form): return func_post("/console/servers/renew_ipv4",['instance_id'],form) #@
def refresh_ipv4(form): return func_post("/console/servers/refresh_ipv4",['instance_id'],form) #@
def network_description(form): return func_get("/console/servers/instance_info",['instance_id'],form) #@

def test_network():
    instance = instance_list()[0]
    print(port_list(instance))
    instance['port'] = 9999;
    print(open_port(instance))
    print(port_list(instance))
    print(close_port(instance))
    print(port_list(instance))
    print(network_description(instance))

    pass

def __________storage__________(): pass
def create_volume(form):   raise "Not implemented yet"
def delete_volume(form):   raise "Not implemented yet"
def transfer_volume(form):   raise "Not implemented yet"

def _________subscription__________(): pass
def subscribe_instance_list():   raise "Not implemented yet"
def subscribe_storage_list():   raise "Not implemented yet"
def subscribe_network_list():   raise "Not implemented yet"
def subscribe_instance(form):   raise "Not implemented yet"
def unsubscribe_instance(form):   raise "Not implemented yet"
def subscribe_storage(form):   raise "Not implemented yet"
def unsubscribe_storage(form):   raise "Not implemented yet"
def subscribe_network(form):   raise "Not implemented yet"
def unsubscribe_network(form):   raise "Not implemented yet"


def _________special__________(): pass
def live_migration(form):   raise "Not implemented yet"
def cancel_transaction(form):   raise "Not implemented yet"

def _________payment__________(): pass
def invoice_list(): return func_get("/console/servers/charge_list",[],{}) #@
def subscription_invoice_list():  raise "Not implemented yet"
def make_invoice(form):  raise "Not implemented yet"
def test_payment():
    print(invoice_list())
    pass

if __name__ == '__main__':
    st = open(__file__).read().split("\n")
    ret = []
    ret2 = []
    cnt = 0
    for line in st:
        ret += [line]
        if "#@" in line:
            if "def" in line:
                s = line.replace("def ","")
                s = s.split(":")[0]
                s = s.strip()
                ret2 += [s]
        if "##@@ GEN @@##" in line:
            cnt += 1
            if cnt == 2:
                break;

    fp = open(__file__,"w")
    fp.write("\n".join(ret))
    fp.write("\n")
    fnc = "def flist():\n"
    fnc += "    return [\n"
    for f in ret2:
        fnc += "        \"" +f+ "\",\n"
    fnc += "    ]\n"
    fp.write(fnc)
    fp.close()
    print(ret)
    print(ret2)

##@@ GEN @@##
def flist():
    return [
        "registered_image_list()",
        "create_image(form)",
        "delete_image(form)",
        "ondemand_list()",
        "launch_ondemand_instance(form)",
        "instance_list()",
        "change_instance_tag(form)",
        "start_instance(form)",
        "stop_instance(form)",
        "restart_instance(form)",
        "terminate_instance(form)",
        "emergency_restart_instance(form)",
        "port_list(form)",
        "open_port(form)",
        "close_port(form)",
        "renew_ipv4(form)",
        "refresh_ipv4(form)",
        "network_description(form)",
        "invoice_list()",
    ]
