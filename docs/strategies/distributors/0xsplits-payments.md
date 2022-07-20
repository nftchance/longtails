 # 0xSplits: a protocol for splitting on-chain income.

[toc]

 Clone contracts receive payments and hold the funds until they are called to transfer the funds to the main contract.

## Profit Mechanism 

The distributors are incentivized to call distributeEth in the main contract which will transfer the funds from the clone contract to the main contract and also split the payment.

But at this point, the funds are still held in the main contract (the contract has a mapping from recipient addresses to the balances). In order to actually receive the funds, users have to call the withdraw function in the main contract.

The primary available places of fund generation are:

- distributeERC20()
- distributeETH()

Distributes the ETH balance for split `split`

## Functions

### `distributeERC20()`

Distributes the ERC20 `token` balance for split `split`

`accounts`, `percentAllocations`, and `distributorFee` are verified by hashing & comparing to the hash in storage associated with split `split`pernicious ERC20s may cause overflow in this function inside _scaleAmountByPercentage, but results do not affect ETH & other ERC20 balances

**Function Args:**
- **split (address)**
    - Address of split to distribute balance for
- **token (address)**
    - Address of ERC20 to distribute balance for
- **accounts (address[])**
    - Ordered, unique list of addresses with ownership in the split
- **percentAllocations (uint32[])**
    - Percent allocations associated with each address
- **distributorFee (uint32)**
    - Keeper fee paid by split to cover gas costs of distribution
- **distributorAddress (address)**
    - Address to pay `distributorFee` to

### `distributeETH()`

`accounts`, `percentAllocations`, and `distributorFee` are verified by hashing & comparing to the hash in storage associated with split `split`

**Function Args:**
- **split (address)**
    - Address of split to distribute balance for
- **accounts (address[])**
    - Ordered, unique list of addresses with ownership in the split
- **percentAllocations (uint32[])**
    - Percent allocations associated with each address
- **distributorFee (uint32)**
    - Keeper fee paid by split to cover gas costs of distribution
- **distributorAddress (address)**
    - Address to pay `distributorFee` to

## Questions and Answers

- **How do I determine all of the splits that are created?**

If the distribution of a split is not needed immediately there is no real reason that we need to strictly watch the creation of new splits and instead we can just refresh every so often.

- **What is the overall timing strategy?**

At the moment I think the best strategy is to just have indexed jobs and then be the first to arrive rather than trying to perfectly time it.

## Generalized Long-Tail Capture Architecture

Right now I think the best way to do this is:

### 1. Transaction API

#### `Opportunity Model`

Defines a long tail strategy that we are watching.

- `contract_address : String`
- `contract_abi : String`
- `transaction_identifiers : Transaction Identifier Model`
- `transactions : Transaction Model`

- `created_at : DateTime`
- `updated_at : DateTime`

- `last_sync_block : Int`

#### `Transaction Identifier Model`

Identifies what type of function we are watching as well as the typing of historical calls.

- `name : String`
- `args : String`

- `machine_rule : String(JSON)`
- `machine_timeout : Int : (blocks to timeout)`

#### `Transaction Model`

Stores the data of a transaction we care about.

- `identifier : Transaction Identifier Model`
- `data: stringify(JSON)`

- `machine_response : String(JSON)`

- `created_at : DateTime`
- `updated_at : DateTime` 

### 2. Machine API

Constantly running clock that calls the Transaction API and checks if we have any transactions that have follow-up processing that is needed.

#### Running Transactions

When a transaction is returned by the api, take the transaction, format the transactions with the rule provided in the transaction identifier.

With this data, you can build and sign the transaction bundle and let it rip.

On success, or timeout of the function return the response to the api.

## Summary

Oxsplits has a nice little stream of free money to offer. Takes a little bit of work but would result in a very nice architecture for anyone that's willing to set it up. With this in place, suddenly one has a generalized keeper that would let them collect on broader strategies.