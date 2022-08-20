## Functions

> Network Name: CANTO
> New RPC URL: https://jsonrpc.canto.nodestake.top/
> Chain ID: 7700
> Currency Symbol: CANTO
> Block Explorer URL: https://evm.explorer.canto.io/

To get started, you are first going to need to get Canto on the Canto network. That is because Canto is the gas token on Canto. 

So, we need to buy Canto on ETH and then we will be able to run other transactions on Canto. This would be where we are going to swap it back to a stable as we are chasing an arb opportunity on stables.

The breakdown looks like:

`ETH (or ERC20) -> Swap to Canto ->  Bridge Canto to Canto -> Swap most to stable`

### The Process

#### Connecting to Canto

As an EVM compatible chain, you can connect to the Canto network using MetaMask. Assuming you have already installed and configured the MetaMask in your browser of choice, start by adding the Canto network:
* Open the MetaMask extension.
* At the top of the interface, click on the network you are connected to e.g. "Ethereum Mainnet".
* Click on "Add Network":

Enter the following RPC settings:
> Network Name: CANTO
> New RPC URL: https://canto.evm.chandrastation.com
> Chain ID: 7700
> Currency Symbol: CANTO
> Block Explorer URL: https://evm.explorer.canto.io/

After saving the network, you will be able to connect to it at any time using the dropdown menu.

#### Bridging Assets into Canto from Ethereum

To bridge assets such as ETH, USDC, and USDT from the Ethereum network to the Canto network, follow these steps: 

1. Navigate to [bridge.canto.io](bridge.canto.io) and connect your MetaMask wallet, making sure you are on the Ethereum network.

2. Before bridging assets to Canto, you will be prompted to generate a Canto public key for your Metamask wallet address. You will only need to do this once, per wallet address. This is so you can sign Cosmos transactions from that Metamask address. There is no interaction with private keys. 

3. Select the token you would like to bridge and input the quantity. Quantities less than 1 must include a 0 in the ones place value (e.g. 0.99).

4. Confirm the approval transaction in your wallet to approve transfer of the asset to the bridge.

5. Sign the message in your wallet to confirm the transfer.

#### Convert Assets for Use on the Canto EVM

> Right now there is a major hurdle in getting your initial Canto as that is the transaction gas token. There is a really big opportunity for bridges in general that provide the token through a fee.

After following the steps above, you will receive your assets on the Canto blockchain. However,  the Canto Lending Market, Canto DEX, and various third-party DApps operate on the Canto EVM, which tracks assets independently.

Before you can use assets on the Canto EVM, you must convert them:

* Navigate to [convert.canto.io](convert.canto.io) and connect your MetaMask wallet, making sure you are on the Canto network.

* Select the token you would like to convert and input the quantity. Quantities less than 1 must include a 0 in the ones place value (e.g. 0.99).

* Click transfer and sign the message in your wallet.

#### Bridging from Canto to Ethereum

To bridge assets from the Canto network to Ethereum, you must have the following:

* Keplr Wallet

* Gravity Bridge address

* Assets on the Canto Native side. If the assets you want to bridge out are on the Canto EVM, use Convert Coin to bridge them back to the Canto Native side.

Select bridge with from as Canto and to as Gravity Bridge. Switch network in Metamask to Canto if not already on Canto.

2. Select the token you wish to bridge out and enter an amount.

3. Copy your Gravity Bridge address from Keplr wallet and input it into the box in the bridge.

4. Click ‘send token’ button and sign Metamask transaction. After a few minutes, you should see the tokens in your Keplr wallet at the address you provided.

5. Once the tokens are in your Keplr wallet, bridge from Gravity Bridge to Ethereum using the Gravity Bridge portal.

#### Hitting an Arb (Triangular Arbitrage)

USDT -> USDC
USDC -> USDT

Canto is like a snake and anyone playing around with other arbitrage opportunities is insane. The market is extremely inefficient and it would be nice to capture that upside quickly.

This means, that we are looking for the opportunities of:

* USDT < $1 when we are holding USDC and USDC > $1
* USDC < $1 when we are holding USDC and USDT > $1
* NOTE 

#### Automating the Process

Basically, all that needs to happen is every block check the price of the market and see if there is an arbitrage available.

When there is, the bot will run the transaction as it has the private key and is interfacing with the contract directly.

#### Validator Machine

The minimum requirements are:

- 16 GB RAM
- 100 GB NVME SSD
- 3.2 GHz x4 CPU

- [Case](https://www.amazon.com/Thermaltake-Computer-Chassis-Pre-installed-CA-1D5-00S1WN-00/dp/B00PDDMN6S/ref=sr_1_4?crid=8389OF85G4AB&keywords=mini+atx&qid=1660970282&sprefix=mini+at%2Caps%2C102&sr=8-4&ufe=app_do%3Aamzn1.fos.006c50ae-5d4c-4777-9bc0-4513d670b6bc)