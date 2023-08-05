# politico-civic-race-ratings


## Ratings scheme

##### Party direction (2018 and incument position)
- Safe Republican
- Likely Republican
- Lean Republican
- Toss-up
- Lean Democratic
- Likely Democratic
- Safe Democratic

##### Race features

- Trump bump
- Trump burn
- Party cash splash
- Star candidate
- Dead-weight candidate
- Made Candidate (endrosements)


## Page structure

#### Home page

- Balance of Power by rating
- Modeler
- Filtered table
- Activity feed

#### Race page

- Current rating
- Shift
- Activity feed
- Candidate info

## Historical Data
#### Where I got the data
- Senate results: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/PEJ5QU
- House results: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/IG0UN2
- President results (by state): https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/42MVDX

#### How to process the data
- First, run `python manage.py bootstrap_ratings` to create the DataProfile object
- [ ] Something funky is going on w/ the South Dakota Governor Data Profile ... it isn't generated automatically when you run `bootstrap_ratings`, which then crashes `bootstrap_historical`, so create that first.
- Then, run `python manage.py bootstrap_historical` to get historical race data for corresponding seat.
- [ ] PA data ... not currently including: https://docs.google.com/spreadsheets/d/1ztOyo95AVogMPltQxkJGsM4o42H7yzxqfIC5AwiFpkk/edit#gid=1739606676

#### Notes on the data
- [ ] Something is weird in House FL-24 in 2016 ... Frederica S. Wilson got 0 votes ...
