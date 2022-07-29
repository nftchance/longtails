# Cooltopia Boss Required Items

Cooltopia is currently plagued by dog-shit tokenomics and token models that were given five seconds of thought. This has resulted in a Boss Fight mechanism that can be controlled with salt-levels of capital.

## Profit Mechanism

For Boss Bottles, there are required items for participation. This is baked into the raw functioning of the website. While the only alpha found in tracking the diffs of the website are not boss battles, that is the focus for this.

## Functions

In the code of the website, there is constant inclusion of "to-come" features thanks to the way that features are rolled out. (This is only fixed by a proper update workflow which is asking far more than I would expect from CC at this point.)

```
[{"name":"Clumping Deserts","description":"<p>The sun looms over the desert during the day, causing an unbearable heat that reflects off the rolling sands. Water and vegetation is hard to find here, except for the odd grouping of Cacti and Ficus.</p>\\n<p>Due to the severe temperatures and lack of water the clumping desert is a harsh place to live. It is home to few creatures who either require little water or have enough ingenuity to find it.</p>\\n<p>Furnados rage this land, causing huge sandstorms that make it impossible to navigate the rolling sands.</p>\\n","live":true,"image":"https://content.coolcatsnft.com/wp-content/uploads/2022/07/location.jpg","bosses":[{"id":"65","name":"Sand Golem","image":"https://content.coolcatsnft.com/wp-content/uploads/2022/07/sand-golem.png","jsonUrl":"/assets/spine/boss-quests/SandGolem/SandGolem.json","atlasUrl":"/assets/spine/boss-quests/SandGolem/SandGolem.atlas","price":"2000","requiredItems":[50,50,50,3],"styleOverrides":"","live":true,"partySize":1,"challenge":"rockPaperScissor","rewards":["65","66","67"]}]},{"name":"Dusty Temple","description":"<p>Centuries old and shrouded by swirling sandy winds, the Dusty Temple is a place of great mystery and wonder.</p>\\n<p>Situated in the south western valley of the The Clumping Desert and carved into the face of the dusty limestone the temple is rumored to contain many ancient tombs, where mummified cats lie in peculiar looking sarcophaguses waiting to be discovered.</p>\\n<p>Many have ventured here in the past attempting to uncover the mysteries the temple conceals, but due to its inaccessible location and hostile environment it remains largely unexplored to this day.</p>\\n","live":false,"image":"https://content.coolcatsnft.com/wp-content/uploads/2022/07/location-1.jpg","bosses":[{"id":"68","name":"Dusty Temple Boss","image":"https://content.coolcatsnft.com/wp-content/uploads/2022/07/dusty-temple-boss.png","jsonUrl":"/assets/spine/boss-quests/DustyTempleBoss/DustyTempleBoss.json","atlasUrl":"/assets/spine/boss-quests/DustyTempleBoss/DustyTempleBoss.atlas","price":"9999999","requiredItems":[51,52],"styleOverrides":"","live":false,"partySize":1,"challenge":"ticTacToe","rewards":[]}]}]'
```

## Functions

The need to lead the capitalistic curve of Cooltopia requires very little effort and just requires a very tiny knowledge advantage.

### 1. Website Scraper

With this the Discord bot will run every 6 hours and store a diff of the log.

### 2. Required Items Logger

Using Regex we will find all instances of `"requiredItems":[*]` and log them into the Longtails channel so that we can always just front-run the bosses. Poor saps.

## Summary

This startegy requires the gall to go to the marketplace and manipulate the price upwards before the boss fight announcement is made. This only becomes more true if they change the price of an item. Playing the strategy of manipulation without a tool like this is a losing game.