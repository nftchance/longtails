# Freemason Frontrunning: Arriving Before The Secret Society

[toc]

Right now there is an outsized opportunity in determining the future releases of a collection before the entire collection even knows. This most recently happening with a massive return from Tableland. With the introduction of their brand, Moonbirds quickly flocked to them having some level of inside information. With Ryan Carson being more leaky than a broken vase, many lined up to have him fill their pockets (just as he did.)

## Profit Mechanism 

There is profit to capture from VCs that have more wealth than sense. Turn the tables and make them enjoy the retail experience.

## Workflow

1. Get all the top collections of an NFT collection
2. Keep track of the new accounts that they follow
3. Build a summary of newly followed accounts
4. Output the list of 'to watch' twitter accounts

## Functions

The needed functionality of a following frontrunner would be best given human discretion. So, a simple rundown / spreadsheet that can be utilized for daily analysis is more than enough. Should just use [NFTInspect](http://nftinspect.xyz) to pull down the owners / followers of a brand. 

The members of a brand can be found at: [https://www.nftinspect.xyz/collections/0x1a92f7381b9f03921564a437210bb9396471050c/members](https://www.nftinspect.xyz/collections/0x1a92f7381b9f03921564a437210bb9396471050c/members)

### 1. Following API

#### `Twitter User Model`

- `username : String`
- `global_followings : Int`
- `global_followers : Int`

- `created_at : DateTime`
- `updated_at : DateTime`

#### `Project Member Model`

- `twitter : Twitter User`
- `wallet_address : String`

- `followers : (M2M) Twitter User`
- `following : (M2M) Twitter User`

- `created_at : DateTime`
- `updated_at : DateTime`

#### `Project Spotlight Model`

- `contract_address : String`
- `members : (M2M) Project Member`

- `created_at : DateTime`
- `updated_at : DateTime`

- `last_sync_at : DateTime`

## Questions and Answers

1. **Will the NFT Inspect API put up a fight?** 

Nope.

2. **How can we get approved by Twitter for API access?**

Should not need to.

## Summary

There is massive money to be made simply by watching the secret followings and interests of individuals. With little automation that can be done this moreso comes down to generating the proper dataset and then giving to a person that has the ability to turn that into something.