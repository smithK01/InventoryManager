# AI Usage Report

## Tools Used

ChatGPT-6.1 Sol max reasoning, ChatGPT-6 Astra max reasoning

## How AI Was Used

AI was used to conceptualize ideas I had, review my code, debug, and helped with finding documentation for syntax or logic errors. I would generally submit my initial attempt at a function/block of code asking for feedback.

AI was also used to assist with verifying tests I created, as well as running automated tests.

AI was also used to fix spelling, to clean up, and verify accuracy of documentation like TESTING.md, README.md, and this AI_USAGE.md.

## Example Prompts

1. "I don't want you to write any code for me unless I get stuck or have a syntax issue, just help me with overall ideas, as well as making sure i meet the project requirements." - my initial prompt, attached with my starting code, file structure, and program requirements.
2. "does this fix the duplicate name issue?" - submitted with my revised add_item function.
3. "verify these tests work as intended, and give me the results. perform your own tests as well, and give me those results." - with my attached code/tests

## Suggestions Accepted

- Correcting string handling by storing the results returned by strip() and split().
- Correcting dictionary access and converting quantities to integers.
- Translating displayed item numbers into list indexes when updating or removing items.
- Correcting loop behavior so duplicate item names are rejected before adding an item.
- Using field-width formatting to improve inventory display readability.
- Documenting expected and actual results for validation, searching, summaries, and file persistence.

## Suggestions Rejected or Modified

I modified the suggested column widths for view_inventory(). I chose widths of 20 characters for item names, 20 for categories, and 5 for quantities to suit my display.

## Verification

I used almost no AI generated code. I only used AI to verify my code, or to provide correct syntax/structuring of my code. Python documentation was used to verify anything too convoluted.

AI assisted documentation draftwork/advice was taken from the AI, and verified against my code and my own results, so I could write my documentation to be accurate and my own work.

## Code Understanding

### save_inventory()
using python's open method, we open/create the filename we passed save_inventory() in write mode, with encoding utf-8. then for each dictionary in 
list inventory, we create a formatted string per dictionary, with all three values separated by  pipes and a newline. when we use write mode, we are replacing the old files contents if it existed before, so we have to write the entire contents of inventory each time.

### search_inventory()
I was really proud of doing this one completely alone, and then only asking the AI to help me with syntax issues like ( if search_query.lower() in i["name"].lower() ), where .lower() was originally .lower, and i["name"] was originally i[i["name"]]. The function works by first checking if the inventory is empty, then by creating an empty list item_matches that we use to store item matches later. then, if the users input is not empty/whitespace, for each dictionary in inventory, we look through the "name" keys in lowercase to find partial and full matches. if we have a partial or full match, item_found is True, and we append that item to the item_matches list. when finished iterating through the dictionaries, if we found any matches, print the search, and then call view_inventory with our list item_matches, so we have some nice formatted output. otherwise we return with the error message.