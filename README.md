# kratos genesis

Genesis for kratos.

## Genesis accounts

| Index |       Name        |                  AuthAddress                  |   Assets    |        Note         |
| ----- | ----------------- | --------------------------------------------- | ----------- | ------------------- |
| 1     | -                 | kratos1xaaxd4p3ll0cgw3l0ujrasuz93knecaet9x9rn | 25          | chain boot Fee      |
| 2     | kratos            | kratos1xaaxd4p3ll0cgw3l0ujrasuz93knecaet9x9rn | 25          | kratos root account |
| 3     | initial@kratos    | kratos1ul7zrgzwwf90j7lxrla09hhcr456j5yae5xkml | 100,000,000 | initial tokens      |
| 4     | foundation@kratos | kratos1v7mv73v0d4gac54pn22ja6qptuxp3u8flls09h | 40,000,000  | foundation tokens   |

## Chain Defines

Baseic defines for chain:

- Main symbol : kratos
- Core token symbol : kts

So build should use params like:

```bash
make all -e CORE_SYMBOL=kts -e MAIN_SYMBOL=kratos
```

## Boot steps

- 1. create key for kratos boot validator.
- 2. create genesis accounts and assets to genesis.
- 3. create genesis trx.
- 4. sign the genesis trx and put to genesis file.
- 5. boot the genesis kratos validator.
- 6. create the other validator and join the network.

## Gen genesis

First use `make-mainnet-genesis.py` to gen txs:

```bash
./make-mainnet-genesis.py --build-path kratos-path/build
```

it will gen this file to genesis:

```bash
./mainnet
├── genesis.json
└── gentx
    └── gentx-xxxxxxxxxxxxxx.json
```

the `gentx-xxxxxxxxxxxxxx.json` need sign by `kratos1xaaxd4p3ll0cgw3l0ujrasuz93knecaet9x9rn` (or the key in `kratos` if gen new keys)

then set into genesis.json signatures info.

```bash
../kratos/build/kucli --chain-id kratos-mainnet --keyring-backend test --home ./mainnet/cli tx sign --from kratos --offline --account-number 0 --sequence 0 ./mainnet/gentx/gentx-xxxxxxxxxxxxxx.json > ./mainnet/gentx/gentx-signed.json
```

put the sign data to genesis.json:

```bash
{
    ...

    "genutil": {
        "gentxs": [
            {
                "type": "kuchain/Tx",
                "value": {
                    "msg": [ ... ],
                    "fee": { ... },
                    "signatures": [
                        {
                            "pub_key": {
                                "type": "tendermint/PubKeySecp256k1",
                                "value": "A/m4d/b/jljWZsIN9xP0EJdz6vuwjxDYZGymUzsAyKhn"
                            },
                            "signature": "mHIxiVHUo9o/lH4PNgxMKVqly3dgXAAIw1bTNb1zKi1QKmFKDVUt/Vzp6PuZGDCXFkodux+9ge3BexhovmrkpQ=="
                        }
                    ],
                    "memo": "......"
                }
            }
        ]
    },

    ...
}
```

than can start `kucd` in `./nodes/kratos`:

```bash
../kratos/build/kucd --home ./mainnet/nodes/kratos/ start
1600087635930506000     info    kucd/start.go:90        starting ABCI with Tendermint
1600087635970941000     info    constants/versions.go:35        Kuchain Version {"version": "0.5.1", "branch": "release", "time": "2020-09-14 09:51.49", "sdkVersion": "github.com/cosmos/cosmos-sdk@v0.38.5"}
1600087636081138000     info    distribution/genesis.go:51      genesis module account asset    {"account": "kudistribution", "asset": ""}
1600087636081625000     info    staking/genesis.go:104  genesis module account asset    {"account": "kubondedpool", "asset": ""}
1600087636081665000     info    staking/genesis.go:114  genesis module account asset    {"account": "kunotbondedpool", "asset": ""}
1600087636081687000     info    staking/genesis.go:119  genesis module account  {"name": "kustaking"}
1600087639201582000     info    state/execution.go:310  Executed block  {"height": 1, "validTxs": 0, "invalidTxs": 0}
1600087639211280000     info    state/execution.go:226  Committed state {"height": 1, "txs": 0, "appHash": "4C773228696705BB3AB300C8E655F05CB064E87D97B2B24F8472D71E7B252FD6"}
```

After boot the kratos node, can use kratos account to create other nodes.
