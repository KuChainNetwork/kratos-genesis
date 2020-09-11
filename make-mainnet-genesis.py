#!/usr/bin/env python

import argparse
import json
import os
import subprocess
import sys
import time
import logging
import re
import random

# Symbols
chainID = 'kratos-mainnet'
mainChainSymbol = 'kratos'
coreCoinSymbol = 'kts'
coreCoinDenom = '%s/%s' % (mainChainSymbol, coreCoinSymbol)
cliCmd = 'kucli'
nodeCmd = 'kucd'
coinBase = 1000000000000000000

keyInit1 = 'kratos1kh9tvl7qdhqkm2lq5xvclj0y2nxlzu3dvazh6z'
keyInit2 = 'kratos1flvs32r3074k3cm3guj6rhnyade0mh8cyzw652'
keyInit3 = 'kratos1q4ku5v7jgs8f6khj7pg33sdrw5cl3tyq5y8pmd'

conAddress = 'kratos1tkklqkveyx8hgmgna4wnz60f9jn7fe49dh76dm'
conPubkey = '03dcea6425fbdf9ccc3d1a267d58ecc8b013d53097bd9d74a58c92393f1f69045d'

# auths for test
auths = {}

# node info for test
nodes = {}

logging.basicConfig(level=logging.DEBUG)

args = None

def run(args):
   logging.debug('%s', args)
   if subprocess.call(args, shell=True):
      logging.error('run \"%s\" error, exitting', args)
      sys.exit(1)

def sleep(t):
    time.sleep(t)

def run_output(args):
   logging.debug('%s', args)

   try:
      out_bytes = subprocess.check_output(args, shell=True)
   except subprocess.CalledProcessError as e:
      out_bytes = e.output
      out_text  = out_bytes.decode('utf-8')
      code      = e.returncode
      logging.error('run \"%s\" error by %d and %s', args, code, out_text)
      sys.exit(1)

   return out_bytes.decode('utf-8')

def cli(cmd):
   cliParams = "--home %s/cli/ --keyring-backend test" % (args.home)
   return run_output('%s/%s %s %s' % (args.build_path, cliCmd, cliParams, cmd))

def cliByHome(home, cmd):
   cliParams = "--home %s" % (home)
   return run_output('%s/%s %s %s' % (args.build_path, cliCmd, cliParams, cmd))

def getNodeHomePath(name):
   return "%s/nodes/%s/" % (args.home, name)

def node(name, cmd):
   cliParams = "--home %s" % (getNodeHomePath(name))
   cmdRun = '%s/%s %s %s' % (args.build_path, nodeCmd, cliParams, cmd)
   return run_output(cmdRun)

def nodeInBackground(name, logPath, cmd):
   cliParams = "--home %s" % (getNodeHomePath(name))
   cmdRun = '%s/%s %s %s' % (args.build_path, nodeCmd, cliParams, cmd)

   with open(logPath, mode='w') as f:
      f.write(cmdRun + '\n')
   subprocess.Popen(cmdRun + '    2>>' + logPath, shell=True)

def nodeByCli(name, cmd):
   cliParams = "--home-client %s/cli/ --keyring-backend test" % (args.home)
   return node(name, '%s %s' % (cliParams, cmd))

def coreCoin(amt):
   return '%s%s' % (amt, coreCoinDenom)

def initWallet():
   logging.debug("init wallet")

   run('rm -rf %s/cli' % (args.home))
   genAuth(mainChainSymbol)
   return

def genAuth(name):
   cli('keys add ' + name)
   valAuth = cli('keys show %s -a' % (name))
   valAuth = valAuth[:-1]
   auths[name] = valAuth
   return valAuth

def getAuth(name):
   return auths[name]

def getNodeName(num):
   return "validator%d" % (num)

def initGenesis(nodeNum):
   # 1 kratos kratos1kh9tvl7qdhqkm2lq5xvclj0y2nxlzu3dvazh6z 0
   node(mainChainSymbol, 'genesis add-account %s %s' % ('kratos', keyInit1))
   node(mainChainSymbol, 'genesis add-coin %s \"%s\"' % (coreCoin(0), "core token for kratos chain"))
   node(mainChainSymbol, 'genesis add-account-coin %s %s' % ('kratos', coreCoin(25 * coinBase)))
   
   # 2 kratos1kh9tvl7qdhqkm2lq5xvclj0y2nxlzu3dvazh6z 50
   node(mainChainSymbol, 'genesis add-address %s' % (keyInit1))
   node(mainChainSymbol, 'genesis add-account-coin %s %s' % (keyInit1, coreCoin(25 * coinBase)))

   # 3 initial@kratos kratos1flvs32r3074k3cm3guj6rhnyade0mh8cyzw652
   node(mainChainSymbol, 'genesis add-account %s %s' % ('initial@kratos', keyInit2))
   node(mainChainSymbol, 'genesis add-account-coin %s %s' % ('initial@kratos', coreCoin(100000000 * coinBase)))
   
   # 4 foundation@kratos kratos1q4ku5v7jgs8f6khj7pg33sdrw5cl3tyq5y8pmd
   node(mainChainSymbol, 'genesis add-account %s %s' % ('foundation@kratos', keyInit3))
   node(mainChainSymbol, 'genesis add-account-coin %s %s' % ('foundation@kratos', coreCoin(40000000 * coinBase)))

   genTx()

def modifyNodeCfg(name, key, oldValue, newValue=None):
   file = "%s/config/config.toml" % (getNodeHomePath(name))

   patternStr = r"^%s = .+" % (key)
   newStr = '%s = %s' % (key, oldValue)

   if (newValue is not None):
      patternStr = r"^%s = %s" % (key, oldValue)
      newStr = '%s = %s' % (key, newValue)

   with open(file, "r") as f1, open("%s.bak" % file, "w") as f2:
      for line in f1:
         f2.write(re.sub(patternStr, newStr, line))

   os.remove(file)
   os.rename("%s.bak" % file, file)

def appendNodeCfg(name, key, value):
   cliByHome(getNodeHomePath(name), "config %s %s" % (key, value))

def initNode(name, num):
   run('rm -rf %s' % (getNodeHomePath(name)))
   node(name, 'init --chain-id %s %s' % (chainID, name))

def initChain(nodeNum):
   initNode(mainChainSymbol, 0)
   initGenesis(nodeNum)
   return

def genTx():
   nodeByCli(mainChainSymbol, 'gentx %s %s --name %s --pubkey %s ' % (mainChainSymbol, keyInit1, mainChainSymbol, conPubkey))
   node(mainChainSymbol, 'collect-gentxs')

def message(msg, *args):
    for arg in args:
        print(msg + ' comes from ' + arg)

# Parse args
parser = argparse.ArgumentParser()
parser.add_argument('--build-path', metavar='', help='Kuchain build path', default='../build')
parser.add_argument('--home', metavar='', help='testnet data home path', default='./mainnet')
parser.add_argument('--trace', action='store_true', help='if --trace to kucd')
parser.add_argument('--log-level', metavar='', help='log level for kucd', default='*:info')
parser.add_argument('--node-num', type=int, metavar='', help='val node number', default=12)

args = parser.parse_args()
logging.debug("args %s", args)

# Start Chain
logging.info("start kuchain testnet by %s to %s", args.home, args.build_path)

run('rm -rf %s/' % (args.home))

initWallet()
initChain(int(args.node_num))

# rm tmp files
run('rm -rf %s/cli' % (args.home))
run('mv  %s/nodes/kratos/config/genesis.json %s/' % (args.home, args.home))
run('mv  %s/nodes/kratos/config/gentx %s/' % (args.home, args.home))
run('rm -rf %s/nodes' % (args.home))