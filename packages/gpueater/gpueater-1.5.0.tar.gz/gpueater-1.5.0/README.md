# GPUEater API Console

## Getting Started
GPUEater is a cloud computing service focusing on Machine Learning and Deep Learning. Now, AMD Radeon GPUs and NVIDIA Quadro GPUs are available.

This document is intended to describe how to set up this API and how to control your instances through this API.

Before getting started, register your account on GPUEater.
https://www.gpueater.com/


----------------------------------------


### AMD RadeonGPU ROCm-TensorFlow information (https://github.com/aieater/rocm_tensorflow_info)
<br>
This README is intended to provide helpful information for Deep Learning developers with AMD ROCm.<br>
<br>
Unfortunately, AMD's official repository for ROCm sometimes includes old or missing information. Therefore, on this readme, we will endeavor to describe accurate information based on the knowledge gained by GPUEater infrastructure development and operation.<br>
<br>
<br>

- How to setup Radeon GPU Driver (ROCm) on Ubuntu16.04/18.04
- How to setup ROCm-Tensorflow on Ubuntu16.04/18.04
  + ROCm(AMDGPU)-TensorFlow 1.8 Python2.7/Python3.5 + UbuntuOS
  + ROCm(AMDGPU)-TensorFlow 1.1x Python2.7/Python3.5/Python3.6 + UbuntuOS
  + CPU-TensorFlow 1.10.1 Python3.7 + MacOSX
- Lightweight ROCm-TensorFlow docker
  + ROCm-TensorFlow on GPUEater
  + ROCm-TensorFlow1.11 docker

ROCm information URL : https://github.com/aieater/rocm_tensorflow_info
<br>
<br>
<br>

----------------------------------------




### Prerequisites
1. Python 3.x is required to run GPUEater API console.
2. Create a JSON file in accordance with the following instruction.

At first, open your account page(https://www.gpueater.com/console/account) and copy your access_token. The next, create a JSON file on ~/.eater

```
{
        "gpueater": {
                "access_token":"[YourAccessToken]",
                "secret_token":"[YourSecretToken]"
        }
}
```

or

```
{
        "gpueater": {
                "email":"[YourEmail]",
                "password":"[YourPassword]"
        }
}
```
* At this time, permission control for each token is not available. Still in development.

## Installation

Add this line to your application's Gemfile:

```python
pip3 install gpueater
```

## Run GPUEater API

Before launching an instance, you need to decide product, ssh key, OS image. Get each info with the following APIs.

#### Get available on-demand product list

This API returns current available on-demand products.
```
import gpueater

res = gpueater.ondemand_list()
print(res)
```
#### Get registered ssh key list

This API returns your registered ssh keys.
```
import gpueater

res = gpueater.ssh_key_list()
print(res)
```

#### Get OS image list

This API returns available OS images.
```
import gpueater

res = gpueater.image_list()
print(res)
```

#### Instance launch

Specify product, OS image, and ssh_key for instance launching.

```
import gpueater

res = gpueater.ondemand_list()

image = res.find_image('Ubuntu16.04 x64')
ssh_key = res.find_ssh_key('[Your ssh key]')
product = res.find_product('a1.rx580')

param = {
    'product_id' : product['id'],
    'image' : image['alias'],
    'ssh_key_id' : ssh_key['id'],
    'tag' : 'HappyGPUProgramming'
}

res = gpueater.launch_ondemand_instance(param)
print(res)
```
In the event, the request has succeeded, then the API returns the following empty data.
{data:null, error:null}

In the event, errors occurred during the instance instantiation process, then the API returns details about the error.

#### Launched instance list

This API returns your launched instance info.
```
import gpueater

res = gpueater.instance_list()
```
#### Terminate instance

Before terminating an instance, get instance info through instance list API. Your instance_id and machine_resource_id are needed to terminate.

```
import gpueater

res = gpueater.instance_list()
for ins in res:
	if ins['tag'] == 'HappyGPUProgramming':
		print(gpueater.terminate_instance(ins))
```



-----


#### API list

##### Image
|  Version  |  Function  | Required | Description  |
| ---- | ---- | ---- | ---- |
|  v0.8  |  image_list()  |  | Listing all OS images |
|  v1.7  |  snapshot_instance(form)  | instance_id, machine_resource_id |  Creating a snapshot |
|  v1.7  |  delete_snapshot(form)  | instance_id, machine_resource_id |  Deleting a snapshot |
|  v1.5  |  registered_image_list()  |  | Listing all user defined OS images |
|  v1.5  |  create_image(form)  | instance_id, image_name |  Adding an user defined OS image |
|  v2.0  |  import_image(form)  | url, image_name |  Registering an user defined OS image on the internet |
|  v1.5  |  delete_image(form)  | fingerprint |  Deleting an OS image |


##### SSH Key
|  Version  |  Function  | Required | Description  |
| ---- | ---- | ---- | ---- |
|  v0.8  |  ssh_key_list()  |  |  Listing all ssh keys |
|  v1.0  |  generate_ssh_key()  |  |  Generating Key Pair |
|  v1.0  |  register_ssh_key(form)  | name, public_key |  Registering an SSH key |
|  v1.0  |  delete_ssh_key(form)  | id |  Deleting an SSH key |

```
import gpueater
import os


ssh_key_name = "my_ssh_key2_for_python"

keys = gpueater.ssh_key_list()
for key in keys:
    if key["name"] == ssh_key_name:
        gpueater.delete_ssh_key(key)

k = gpueater.generate_ssh_key()
print(gpueater.register_ssh_key({"name":ssh_key_name,"public_key":k["public_key"]}))

HOMEDIR = os.path.expanduser("~")
fp = open(os.path.join(HOMEDIR,".ssh",ssh_key_name+".pem"),"w")
fp.write(k["private_key"])
fp.close()
print(gpueater.ssh_key_list())

```

##### Instance
|  Version  |  Function  | Required | Description  |
| ---- | ---- | ---- | ---- |
|  v0.8  |  ondemand_list()  |  |  Listing all on-demand instances |
|  v2.0  |  subscription_list()  |  |  Listing all subscription instances |
|  v0.8  |  launch_ondemand_instance(form)  | product_id, image, ssh_key_id |  Launch an on-demand instance |
|  v2.0  |  launch_subcription_instance(form)  | subscription_id, image, ssh_key_id |  Launch a subscription instance |
|  v0.8  |  instance_list()  |  |  Listing all launched instances |
|  v1.0  |  change_instance_tag(form)  | instance_id, tag |  Changing an instance tag |
|  v1.0  |  start_instance(form)  | instance_id, machine_resource_id |  Starting an instance. If the instance is already RUNNING, nothing is going to happen |
|  v1.0  |  ~~stop_instance(form)~~[Deprecated]  | instance_id, machine_resource_id |  Stopping an instance. If the instance is already STOPPED, nothing is going to happen |
|  v1.0  |  restart_instance(form)  | instance_id, machine_resource_id |  Restarting an instance |
|  v0.8  |  terminate_instance(form)  | instance_id, machine_resource_id |  Terminating an instance |
|  v1.0  |  emergency_restart_instance(form)  | instance_id, machine_resource_id |  Restarting an instance emergently when an instance is hung up |

The "machine_resource_id" is including an instance object.  See the following sample code.

Example:
```

instance = gpueater.instance_list()[0]
# instance object has instance_id, and machine_resource_id.

gpueater.terminate_instance(instance)

```

##### Network
|  Version  |  Function  | Required | Description  |
| ---- | ---- | ---- | ---- |
|  v1.0  |  port_list(form)  | instance_id |  Listing all ports |
|  v1.0  |  open_port(form)  | instance_id, connection_id, port |  Opening a port for inbound traffic |
|  v1.0  |  close_port(form)  | instance_id, connection_id, port |  Closing a port for inbound traffic |
|  v1.0  |  renew_ipv4(form)  | instance_id |  Getting a new IPv4 address |
|  v1.0  |  network_description(form)  | instance_id |  This API reports current network status |

##### Storage
|  Version  |  Function  | Required | Description  |
| ---- | ---- | ---- | ---- |
|  v2.0  |  create_volume(form)  | size |  Creating an extended volume |
|  v2.0  |  attach_volume(form)  | volume_id, instance_id |  Attaching an extended volume to an instance |
|  v2.0  |  delete_volume(form)  | volume_id |  Deleting an extended volume |
|  v2.0  |  transfer_volume(form)  | volume_id,region_id |  Transfering an extended volume to another region |

##### Subscription
|  Version  |  Function  | Required | Description  |
| ---- | ---- | ---- | ---- |
|  v2.0  |  subscription_instance_list()  |  |  Listing all subscription instances |
|  v2.0  |  subscription_storage_list()  |  |  Listing all storage volumes |
|  v2.0  |  subscription_network_list()  |  |  Listing all subscription networks |
|  v2.0  |  subscribe_instance(form)  | subscription_id |  Subscribing a subscription instance |
|  v2.0  |  unsubscribe_instance(form)  | subscription_id |  Canceling a subscription instance |
|  v2.0  |  subscribe_storage(form)  | subscription_id |  Subscribing a storage volume |
|  v2.0  |  unsubscribe_storage(form)  | subscription_id |  Canceling a storage volume |
|  v2.0  |  subscribe_network(form)  | subscription_id |  Subscribing a network product |
|  v2.0  |  unsubscribe_network(form)  | subscription_id |  Canceling a network product |

##### Special
|  Version  |  Function  | Required | Description  |
| ---- | ---- | ---- | ---- |
|  v2.5  |  live_migration(form)  | product_id, region_id, connection_id |  Moving a running instance to another physical machine without termination |
|  v2.5  |  cancel_transaction(form)  | transaction_id |  Canceling a transaction |
|  v2.5  |  peak_transaction(form)  | transaction_id |  checking a current transaction status |

##### Payment
|  Version  |  Function  | Required | Description  |
| ---- | ---- | ---- | ---- |
|  v1.0  |  invoice_list()  |  |  Listing invoices for on-demand instances |
|  v2.0  |  subscription_invoice_list()  |  |  Listing invoices for subscription instances |
|  v2.5  |  make_invoice(form)  | invoice_id |  Obtain a pdf invoice |

##### Extensions
|  Version  |  Function  | Required | Description  |
| ---- | ---- | ---- | ---- |
|  v1.7  |  copy_file(form)  | action("get"or"put"), src, dst |  Copying a file. "get" obtains a file from a remote host to your local host, and "put" is the opposite. "src" is a source file path, and "dst" is a destination file path |
|  v1.7  |  delete_file(form)  | src, recursive |  Deleting a remote file |
|  v1.7  |  move_file(form)  | action("get"or"put"), src, dst |  Moving a file. "get" obtains a file from a remote host to your local host, and "put" is the opposite. "src" is a source file path, and "dst" is a destination file path |
|  v1.7  |  make_directory(form)  | dst |  Making a directory in a remote host |
|  v1.7  |  file_list(form)  | src |  Listing all files in a remote host |
|  v1.7  |  synchronize_files(form)  | action, src, dst |  This API is similar to the "rsync" |
|  v1.7  |  login_instance(form)  | instance_id | Logging in a specific instance through the SSH |
|  v1.7  |  tunnel(form)  | instance_id, port |  This API enables a port tunneling between your local and a remote host |

##### Class API
|  Version  |  Function  | Required | Description  |
| ---- | ---- | ---- | ---- |
|  v1.7  |  api_list()  |  |  Listing all available APIs. |


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
