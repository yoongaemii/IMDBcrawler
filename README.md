# IMDB crawler
- Collects title, year, imgsrc, country, genre, time, director, oscar, award, budget, opening_wknd, openingUSA, grossUSA, grossWorld
- Country, genre, director can have one or more elements
- `ignore_exception` ignores errors in a function `get_money_stuff`
- `ignored` ignores error while dealing with soup object in the main function(`crawler`)
- HTML of IMDB can be updated thus yielding unexpected results
