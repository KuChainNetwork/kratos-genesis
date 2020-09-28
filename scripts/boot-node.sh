#!/usr/bin/env bash

VERSION="0.5.1"

MAIN_SYMBOL='kratos'
CORE_SYMBOL='kts'

MAINNET_CHAIN_ID="kratos"

NODE_ID="nodeid"
ROOTPATH="."

#OSSTRING="linux_amd64"
OSSTRING="darwin_amd64"

# download package
#curl -LJ -o kratos.tar.gz https://github.com/KuChainNetwork/kratos/releases/download/v${VERSION}/kratos_${VERSION}_${OSSTRING}.tar.gz
mkdir -p ${ROOTPATH}/bin
tar -xzvf ./kratos.tar.gz -C ${ROOTPATH}/bin

# init node
rm -rf ${ROOTPATH}/node
./bin/kucd_${OSSTRING} init ${NODE_ID} --home ${ROOTPATH}/node --chain-id ${MAINNET_CHAIN_ID}
rm -rf ${ROOTPATH}/node/config/genesis.json
curl -LJ -o  ${ROOTPATH}/node/config/genesis.json https://raw.githubusercontent.com/KuChainNetwork/kratos-genesis/master/genesis/mainnet/genesis.json

# make config for seed
SEED_CONFIG='seeds = "3192fada5783c4094c5f1e34998d22c28ae17b3c@54.250.252.137:26656"'
SEDPARAM='s/seeds = ""/'${SEED_CONFIG}'/g'
SEDCMD="sed -i '' '"${SEDPARAM}"' "${ROOTPATH}"/node/config/config.toml"

echo ${SEDCMD}

#${SEDCMD}