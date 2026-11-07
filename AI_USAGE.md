# AI Usage Report

# HW 1:

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


# HW 2:

## Testing and refactoring
- AI assistance was used to confirm testing that I did myself first as a sanity check. AI only assisted in debugging durring refactoring, all other refactoring work was done myself.
- I created initial test placeholders, and worked on every single test. AI helped with understanding fixtures and parameterization, and then helped my debug tests, and suggested example tests that I integrated. I asked for help with some of the tests, because I wanted to do every example from the instruction, but some of them needed a bit of explaining for me to get right. I had ChatGPT write it's own version of tests for test_inventory_manager.py, which I compared to my own, which I then used to implement better tests, variable names and fixes.
- I ran the 48 tests I made, and all pass on Windows 10 Python 3.13.3
- AI ran it's own 48 tests, and those all passed on Linux Python 3.12.14.

## Prompts
1. lets work on refactoring so we can test easier. do you see any standout issues i need to fix for testability?
2. here is my attempt at refactoring search_inventory(), did I miss anything important? (followed by the function)
3. im having a difficult time thinking about how i am going to move all of the input validation in add_item(). Because i have so many nested if else's. 
- 3's response: The key is to keep retrying input in add_item() and move the validation rules into a helper that checks one set of values Use early returns: when a check fails, return immediately. Later checks can then sit at the same indentation instead of inside another else.
4. ok, are we good to make a commit and focus on the test cases? (inventory_manager.py uploaded here)
- 4's  response: Yes—this is a good point to commit the refactor and begin the pytest suite. I ran representative helper checks and an interactive walkthrough on Python 3.12.14. Adding, updating, removing, searching, summaries, and saving/reloading worked with temporary data. The empty summary now returns the correct zero values. These were review checks; your assignment’s pytest suite still needs to be written.
## Suggestions accepted
ChatGPT suggested the function names, and helped with some doc strings to make sure they came accross the right way. It also suggested better variable names when I made them too convoluted.

I also used AI provided sample data ammounts/dictionaries, like ({"name": "Laptop Charger", "category": "Electronics", "quantity": 4},
        {"name": "USB-C Charger", "category": "electronics", "quantity": 5},
        {"name": "Pen", "category": "Office Supplies", "quantity": 10},
        {"name": "Notebook", "category": "Office Supplies", "quantity": 0})
simply because it was faster to give it some items, and for it to make a list of random stuff that I could then work with.

I also accepeted suggestions like:
- The tuple order and placement after the loop are now correct. The remaining issue is the empty-inventory result. Your display guard prevents the crash, but HW2 requires the calculation helper to return correct summary values for an empty inventory. With your current five-value tuple, that result should be: (0, 0, 0, {}, []) Remove the early return None. Your initialized variables already contain those values, and an empty inventory simply skips the loop before reaching the tuple construction. The display function can still check whether inventory is empty and print “No inventory found.” That display decision doesn’t require the calculation helper to return None. Also, your tuple approach is valid—you can remove the TODO. The initial summary_tuple = () assignment is unnecessary because you assign the completed tuple before returning it.
- Yes—the responsibilities are now separated correctly: the helper returns validated data, and the wrapper appends and saves it There’s one important testability issue: quantity.strip() requires a string. A direct call with an integer quantity, such as 5, would raise AttributeError. Remove that cleanup line; your existing int(quantity) already handles integers and numeric strings with surrounding whitespace. Two remaining cleanup items: Update the helper docstring. It returns a new item dictionary or an error code, rather than an appended inventory. Flatten the remaining else blocks. They work, but are unnecessary. Category validation can follow the duplicate-checking loop directly, and quantity validation can follow the category check. Earlier failures already return. Your error branches correctly repeat the input loop, and successful input gets appended exactly once

## Suggestions rejected or modified
- Yes—this now separates the responsibilities correctly: The helper validates the number, removes the item, and returns its dictionary—or None for invalid input. The wrapper handles input, display, and saving. break works here because nothing follows the loop. One naming improvement: removed_item would be clearer than is_item_removed, since the variable holds a dictionary rather than a Boolean. This helper is ready for tests covering first, middle, and last removal, plus zero, negative, and too-large item numbers. For successful removal, assert both the returned dictionary and the remaining inventory. For invalid input, assert that the result is None and the inventory is unchanged. (rejected starting tests, wanted to finish refactoring. did use the variable name suggestion though.)
- (my input: lets use every example that is given in the hw2 instructions. just give me a list of function names, ill build the boilerplate stuff, copy it 20 times, that way I can go through and fill them out quicker. got it?) output: Worked for 1m 14s Got it. Use these 20 test-function names. We’ll parameterize several so they cover every required case and collect more than 20 tests. Don't forget to use the assignemts required use of 1. Arrange 2. Act 3. Assert.) (I used most of the function names, some of them were fairly long and too complex.)

## Independent verification of results and code

- I ran the 48 tests I made, and all pass on Windows 10 Python 3.13.3. 
- I refactored Inventory_manager.py completely myself, with AI debugging help and review.
- I wrote the documentation, and AI reviewed it and fact checked me, where I reviewed what it was attempting to clarify.
- I created the initial test placeholders, AI helped with the fixtures, parameterization and test body starting points before I filled them all the way out. Some AI sample data (as stated above), test variable names, a few test structures, and a few fixed assertions remain in the final version after I reviewed and edited them.
- After refactoring, I went through and made sure the program still worked as before.
- Anything that went into the inventory_manager project was either my own, or something that I fully understood. 