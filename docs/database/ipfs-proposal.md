# IPFS Proposal

The document outlines a proposal for utilizing the decentralized P2P file system IPFS for shared communication among miners, validators, and monitoring.

IPFS is easy to use; all that's needed is to install the Python module ipfs-api (and configure an API key?). Uploading a file is as simple as executing ipfsClient.add('file.txt'), and the function will return an object containing the file's hash. Access from elsewhere is achieved using ipfs file hash.

```
>>> import ipfsApi
>>> api = ipfsApi.Client('127.0.0.1', 5001)
>>> res = api.add('test.txt')
>>> res
{'Hash': 'QmWxS5aNTFEc9XbMX1ASvLET1zrqEaTssqt33rVZQCQb22', 'Name': 'test.txt'}
>>> api.cat(res['Hash'])
'fdsafkljdskafjaksdjf\n'
```

Features of IPFS:
- Reliability: Files are stored locally until someone downloads them, and a duplicate will be available to them. Therefore, there is a risk of file loss if it's stored in a single instance.
- Anonymity: When uploading a file to the IPFS network, the IP addresses of the sender and receiver are visible to the node uploading and receiving. For added security, miners may require a VPN.
- Backend Read-Write, Frontend Read-only: There is an issue with uploading from the browser frontend. Some solutions exist for the frontend, but the ipfs architecture design seems primarily focused on the backend. (?)
- Not all local features are available on the IPFS mainnet. (?)

# IPFS Resources

## OrbitDB

OrbitDB is a distributed database built on top of the IPFS file system.

https://orbitdb.org/
https://github.com/orbitdb/orbit-db/blob/master/GUIDE.md

## IPFS Examples

IPFS from ETH smart contract

https://github.com/tooploox/ipfs-eth-database


