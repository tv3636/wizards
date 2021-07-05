# Forgotten Runes Wizard's Cult Name Rarity Ranking

### Overview
Name rarity is calculated by breaking each wizard’s name into its four component parts: `title`, `name`, `prepositions`, and `origin`.

For example, [_Enchanter Victoria of the Arctic_](https://opensea.io/assets/0x521f9c7505005cfa19a8e5786a9c3c9c9f5e6f42/7016) is broken down as:
  - `title`: Enchanter
  - `name`: Victoria
  - `prepositions`: of the
  - `origin`: Arctic
  
while [_Enchanter of the Keep_](https://opensea.io/assets/0x521f9c7505005cfa19a8e5786a9c3c9c9f5e6f42/4155) becomes:
  - `title`: Enchanter
  - `name`: `None`
  - `prepositions`: of the
  - `origin`: Keep

These 4 categories can then be treated just like traits and scored as such. 

A 5th trait is added to score the combination of categories with a non-null value for each wizard. The combo score acts in place of a score for name length, due to variance in the length of each trait (i.e. [_The Color Master_](https://opensea.io/assets/0x521f9c7505005cfa19a8e5786a9c3c9c9f5e6f42/1234) is 3 words, but its 3 words are all part of a `title`, whereas [_Soran of Limbo_](https://opensea.io/assets/0x521f9c7505005cfa19a8e5786a9c3c9c9f5e6f42/926) is 3 words, but has a name, prepositions, and an origin). 

The full breakdown of values for each trait (`combo`, `title`, `name`, `prepositions`, and `origin`) can be found [here](name-summary.json).

### Scoring

The scoring works as follows:

First, wizards receive a base score for each trait correlated with how often that trait’s value occurs. The title “Enchanter” occurs 479 times, so its score is `10000 / 479 = 20.88`. The combination `{“title”: False, “name”: False, “prepositions”: True, “origin”: True}` (i.e. [_of the Tower_](https://opensea.io/assets/0x521f9c7505005cfa19a8e5786a9c3c9c9f5e6f42/7596)) appears only 8 times, giving it a base score of `10000 / 8 = 1250`, and so on for each category. 

**Note that prepositions are ignored for scoring**.

Next, base scores for each trait are divided by the average base score for that trait across all wizards, in order to normalize categories before weighing them. For example, if the average score for `title` was 100, each wizard's title score would be divided by 100. This would make the score for the `title` Enchanter above `20.88 / 100 = .2088`.

To provide an appropriate weight for each category, scores are multipled by the average _value_ in that category divided by the wizard's value in that category. The average `name` occurs 17.6 times across the collection, so a name that occurs only once is 17.6x more rare than average, and receives that weight.

Finally, a wizard's score for each category (`title score`, `name score`, `origin score`, and `combo score`) is summed up to its `total`. You can view the current ranking including the complete score breakdown [here](rarity.csv).


### Disclaimer

This ranking is a work-in-progress and is subject to change as the algorithm is adjusted to better fit the collection. Please note that this particular ranking is _only for names_ and does not consider any other true traits like Head, Body, Prop, and so on. 


