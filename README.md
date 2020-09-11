# kratos genesis

Genesis for kratos.

## Genesis accounts

| Index |       Name        |                  AuthAddress                  |   Assets    |        Note         |
| ----- | ----------------- | --------------------------------------------- | ----------- | ------------------- |
| 1     | -                 | kratos1kh9tvl7qdhqkm2lq5xvclj0y2nxlzu3dvazh6z | 5          | chain boot Fee      |
| 2     | kratos            | kratos1kh9tvl7qdhqkm2lq5xvclj0y2nxlzu3dvazh6z | 5          | kratos root account |
| 3     | initial@kratos    | kratos1flvs32r3074k3cm3guj6rhnyade0mh8cyzw652 | 100,000,000 | initial tokens      |
| 4     | foundation@kratos | kratos1q4ku5v7jgs8f6khj7pg33sdrw5cl3tyq5y8pmd | 40,000,000  | foundation tokens   |

## Chain Defines

Baseic defines for chain:

- Main symbol : kratos
- Core token symbol : kts

So build should use params like:

```bash
make all -e CORE_SYMBOL=kts -e MAIN_SYMBOL=kratos
```

## Gen genesis

First use `make-mainnet-genesis.py` to gen txs:

```bash
./make-mainnet-genesis.py --build-path kratos-path/build
```

it will gen this file to genesis:

```
./mainnet
├── genesis.json
└── gentx
    └── gentx-xxxxxxxxxxxxxx.json
```

the `gentx-xxxxxxxxxx.json` need sign by `kratos1kh9tvl7qdhqkm2lq5xvclj0y2nxlzu3dvazh6z` (or the key in `keyInit1`)

then set into genesis.json signatures info.