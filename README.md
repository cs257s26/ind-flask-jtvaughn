# README

## urls
To see `top_n` species within `radius` of a city: 
http://127.0.0.1:5000/top_species?location=<city>&radius=<miles>&top_n=<n>

To see a leaderboard for `animal`:
http://127.0.0.1:5000/leaderboard?animal=<animal>

## write up


Tables were created and data was loaded on Stearns with:
```sql
\copy observations FROM 'amphibians_clean.csv' CSV HEADER;
\copy observations FROM 'birds_clean.csv' CSV HEADER;
\copy observations FROM 'insects_clean.csv' CSV HEADER;
\copy observations FROM 'mammals_clean.csv' CSV HEADER;
\copy observations FROM 'reptiles_clean.csv' CSV HEADER;
```

The orgininal implementation of top_species_command_line required loading the entire data set into memory and computing haversine distances for every observation on each request. When using PostgreSQL the bounding box filter can be run as a where clause which is more efficient.

Write Up:
I used a single table, called observation. The five iNaturalist CSVs have the same format and all represent an observation of a species at a location at a time. I decided not to split into file separate tables because it would require using UNION, and did not offer much benefit. For columns, I kept the 14 fields that were seemed relevant to my user stories (identification, location, time, observer, and taxonomy) and excluded iNaturalist metadata that wasn't used by either query, such as image licensing and time zone fields.

Data Types:
- id and taxon_id are INTEGER since they are numeric identifiers
- observed_on is DATE since these are dates
- latitude and longitude are REAL because they have decimals but do not need double precision
- num_id_agreements is INTEGER since it's a count
- Everything else is TEXT since strings are variable length and I did not think it was worth restricting.
- The primary key is id, the iNaturalist observation ID. It is guaranteed to be unique across all observation and is already an integer so another key was not necessary.


### User Story 1
"As a hiker in Minnesota, I want to select a city and see the most commonly observed species across major taxonomic groups so that I can quickly know what wildlife I might see."
The query filters observation to a bounding box and the input coordinates, and groups by iconic_taxon, taxon_name, and common_name, counts observations per species, and orders by taxon and count. The python wrapper then keeps just the top n species per taxon. Combined with getTopSpeciesByCity, which forward-geocodes a city name via Nominatim, the user can simply enter a city and see what's commonly observed nearby.


### User Story 2
"I am an avid and competitive user of INaturalist. I want to know if I am a top contributor in a certain species sighting in Minnesota. I would really like it if the top 100 contributors for a species, of my choosing, was printed out onto a leaderboard, so I could see how I stack up to the top contributors."
The query filters to a single species by common_name, groups by observer, counts each observer's submissions, orders descending, and returns the top 100.