#!/bin/bash

echo $1

VERSION="0.5.1"

MAIN_SYMBOL='kratos'
CORE_SYMBOL='kts'

MAINNET_CHAIN_ID="kratos"

NODE_ID="nodeid"
ROOTPATH="."

if [ -z $1 ]; then
    ROOTPATH="."
else
    ROOTPATH=$1
fi

OS_STRING=$(uname -s | tr A-Z a-z)
ARCH_STRING=`uname -m`

OS=${OS_STRING}
ARCH="amd64"

echo ${OS}
echo ${ARCH}

if [ $ARCH_STRING == "x86_64" ]; then
    echo "os "${OS}'_'${ARCH_STRING}
else
    echo "no support os for "${ARCH_STRING}
    exit 1
fi

OSSTRING=${OS}'_'${ARCH}
#OSSTRING="darwin_amd64"

# download package
curl -LJ -o kratos.tar.gz https://github.com/KuChainNetwork/kratos/releases/download/v${VERSION}/kratos_${VERSION}_${OSSTRING}.tar.gz
mkdir -p ${ROOTPATH}/bin
mkdir -p ${ROOTPATH}/log
tar -xzvf ./kratos.tar.gz -C ${ROOTPATH}/bin

# init node
rm -rf ${ROOTPATH}/node

./bin/kucd_${OSSTRING} init ${NODE_ID} --home ${ROOTPATH}/node --chain-id ${MAINNET_CHAIN_ID}
rm -rf ${ROOTPATH}/node/config/genesis.json
curl -LJ -o  ${ROOTPATH}/node/config/genesis.json https://raw.githubusercontent.com/KuChainNetwork/kratos-genesis/master/genesis/mainnet/genesis.json

rm -rf ${ROOTPATH}/node/config/config.toml
curl -LJ -o  ${ROOTPATH}/node/config/config.toml https://raw.githubusercontent.com/KuChainNetwork/kratos-genesis/master/genesis/mainnet/config.toml

if [ $OS == "linux" ]; then
    nohup ${ROOTPATH}/bin/kucd_${OSSTRING} start --home ${ROOTPATH}/node >> ${ROOTPATH}/log/node.log 2>&1 &
fi

if [ $OS == "darwin" ]; then
    nohup ${ROOTPATH}/bin/kucd_${OSSTRING} start --home ${ROOTPATH}/node >> ${ROOTPATH}/log/node.log 2>&1 &
fi
