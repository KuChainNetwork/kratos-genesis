# Kratos Boot Script

We can use this script to init and boot node for kratos.

## Usage

Before use script, should install some dependencies:

OS X:

```bash
brew install curl
```

Ubuntu:

```bash
sudo apt-get install curl -y
```

Use this script to create a node:

```bash
mkdir kratos-node
cd kratos-node
curl https://raw.githubusercontent.com/KuChainNetwork/kratos-genesis/master/scripts/boot-node.sh | bash 
```

this will create a node in path kratos-node/, and boot it auto.

In this script, it will download the bin and configs from github, then boot the node in background.

you can show logs:

```bash
tail -n 10 ./log/node.log
```

**Warnning** : The script will init the privKeys to node/priv_validator_key.json, you should to backup this data.