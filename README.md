# Naughty or Nice — Christmas Analytics System

A Python command-line program that scores children on their behaviour, sorts them into four categories, and assigns each one a gift from a limited supply.

Written for AP Computer Science.

## What it does

You either enter a child manually and answer ten behaviour questions about them, or simulate twenty children with random answers. The program then:

1. Calculates a behaviour score for each child
2. Sorts them into angelic, nice, naughty or evil
3. Assigns a gift based on their category, and removes it from stock
4. Prints reports and statistics

There is also an option to nudge the results so the category percentages land in a target range.

## How scoring works

Each child answers ten questions like "How often did this child help others this year?" and "How often did they lie to parents or teachers?"

Every question has three possible answers — frequently, sometimes, never — and each answer is worth a different number of points. Good behaviour questions give points for "frequently" and take them away for "never." Bad behaviour questions work the opposite way, so answering "never" to "did they lie?" earns points.

The weights are not symmetrical. Lying frequently costs 20 points, while helping others frequently earns 15. Bad behaviour is punished harder than good behaviour is rewarded.

After the questions, three rules based on the child's name adjust the score:

- A double letter anywhere in the name adds 5 points
- A name where every letter is unique loses 4 points
- A name starting with A, J or S adds 6 points

Finally a random number between −3 and +3 is added, so two children with identical answers won't always get the same score.

## The categories

The final score decides the category:

| Score | Category |
| --- | --- |
| 70 and above | Angelic |
| 30 to 69 | Nice |
| −30 to 29 | Naughty |
| Below −30 | Evil |

The lowest possible score is about −127 and the highest is about +124.

## How gifts get assigned

Each category has its own list of gifts:

- **Angelic** — Remote Control Car, Doll Set, Video Game Console, Bike
- **Nice** — Art Kit, Soccer Ball, Rubik's Cube, LEGO Set
- **Naughty** — Coal, Socks, Chores List
- **Evil** — a Krampus visit

The program builds a list of which gifts the child is actually eligible for, filtering out any that are restricted to a different gender. A child registered as X can receive anything.

Each gift also has a **bias** number, which represents how much a child would want it. The program picks randomly from the eligible gifts, but weighted by that bias, so a Video Game Console (bias 60) gets picked more often than a Bike (bias 40).

Every gift has a limited quantity. Once a gift is assigned, its stock drops by one. If a child is eligible for nothing, they get an IOU instead.

Each gift also has ASCII art, which prints with the child's report.

## The percentage adjustment

This is the most complicated part of the program.

The assignment required the final results to fall within certain ranges: 50–80% nice, 0–20% angelic, 10–40% naughty, 0–10% evil. Random scores don't naturally land in those ranges, so option 6 in the menu fixes that.

For each category, the program compares the current percentage to the target. If a category has too few children, it moves children up from the category below. If it has too many, it moves some down.

The important part is *which* children get moved. Instead of picking at random, the program sorts candidates by how close their score is to the boundary, then moves the closest ones first. So if angelic needs more children, a child scoring 68 moves before a child scoring 45 — the ones who were already borderline.

After the categories change, all the gifts are wrong, so the inventory is reset and every gift is assigned again from scratch.

## Running it

```bash
python CodeKringle_Naughty_Nice_Analytics_Engine.py
```

You need Python 3. There is nothing to install — the program only uses `random` and `os`, which come with Python.

## The menu

```
  1. Add child manually
  2. Simulate 20 children
  3. View per-child reports
  4. View category lists
  5. Generate summary statistics
  6. Use data percentage approximation
  7. Clear all data
  8. Exit
```

Option 1 asks you all ten questions yourself. Option 2 answers them randomly for twenty children, weighted so most children come out reasonably well behaved.

Option 3 prints a full report for each child, including every question, their answer, and the points it was worth. Option 5 prints the overall statistics: how many children in each category, the most common gift, and what's left in stock.

## How the code is organised

Everything is in one file.

- `Child` — a class holding one child's name, gender, answers, score, category and gift
- `behaviour_questions` — the ten questions and their point values
- `GIFT_INVENTORY` — every gift with its quantity, gender restriction and bias
- `GIFT_ART` — the ASCII art for each gift
- `calculate_behaviour_score()` — asks the questions (or simulates them) and applies the name rules
- `categorize_child()` — turns a score into a category
- `assign_gift()` — picks a gift and reduces the stock
- `adjust_category_percentages()` — the rebalancing described above
- `generate_summary_statistics()` — the overall report
- `main()` — the menu loop

## Known issues

- `os.system("clear")` only works on Mac and Linux. On Windows the screen won't clear.
- The angelic and nice gift lists don't check whether a gift is still in stock before offering it, so those quantities can go below zero. The naughty list does check.
- Nothing is saved. Closing the program loses all the data.
