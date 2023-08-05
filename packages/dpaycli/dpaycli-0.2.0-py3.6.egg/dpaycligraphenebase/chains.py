
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
default_prefix = "DWB"
known_chains = {
    "DPAY": {
        "chain_id": "38f14b346eb697ba04ae0f5adcfaa0a437ed3711197704aa256a14cb9b4a8f26",
        "min_version": '0.19.6',
        "prefix": "DWB",
        "chain_assets": [
            {"asset": "BBD", "symbol": "BBD", "precision": 3, "id": 0},
            {"asset": "BEX", "symbol": "BEX", "precision": 3, "id": 1},
            {"asset": "VESTS", "symbol": "VESTS", "precision": 6, "id": 2}
        ],
    },
    "DPAYAPPBASE": {
        "chain_id": "38f14b346eb697ba04ae0f5adcfaa0a437ed3711197704aa256a14cb9b4a8f26",
        "min_version": '0.19.10',
        "prefix": "DWB",
        "chain_assets": [
            {"asset": "@@000000013", "symbol": "BBD", "precision": 3, "id": 0},
            {"asset": "@@000000021", "symbol": "BEX", "precision": 3, "id": 1},
            {"asset": "@@000000037", "symbol": "VESTS", "precision": 6, "id": 2}
        ],
    },
    "DPAYZERO": {
        "chain_id": "38f14b346eb697ba04ae0f5adcfaa0a437ed3711197704aa256a14cb9b4a8f26",
        "min_version": '0.0.0',
        "prefix": "DWB",
        "chain_assets": [
            {"asset": "BBD", "symbol": "BBD", "precision": 3, "id": 0},
            {"asset": "BEX", "symbol": "BEX", "precision": 3, "id": 1},
            {"asset": "VESTS", "symbol": "VESTS", "precision": 6, "id": 2}
        ],
    },
    "TESTNET": {
        "chain_id": "79276aea5d4877d9a25892eaa01b0adf019d3e5cb12a97478df3298ccdd01673",
        "min_version": '0.0.0',
        "prefix": "DWT",
        "chain_assets": [
            {"asset": "BBD", "symbol": "BBD", "precision": 3, "id": 0},
            {"asset": "BET", "symbol": "BET", "precision": 3, "id": 1},
            {"asset": "VESTS", "symbol": "VESTS", "precision": 6, "id": 2}
        ],
    }
}
