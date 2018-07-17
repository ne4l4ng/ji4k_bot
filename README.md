ji4k bot is a simple telegram bot that helps groups decide where to eat
using a simple voting system.

Flow:
/start to start the vote

each user will be presented with a custom keyboard with venues as
buttons. 

User selects a venue and the bot will record the vote

Each user has 1 vote

use /done when all users have voted or group decides to tally 
up the votes.

Bot will present the results, the venue with the highest votes
is the recommended dining option. in case of tie, the tally is 
sorted in alphabetical order.

TODO
- as a user, i want to set a time for the bot to start the 
vote on a daily basis, so that i don't have to keep starting
the bot 
- as a user, i want to be able to suggest venues not already in
the default list

FIXES TODO
- MODULARISE
- differentiate by chat id

sh4d3 
