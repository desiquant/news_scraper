# TODO

- When scraping in "update" mode. Since it has to load a very large dataset to check for URLs and last_date, it becomes very Memory intensive for a small hetzner server and crashes the process.

- In pytest, if it fails, prevent scrapy from showing the entire output
- moneycontrol and indianexpress have very aggressive protection.
  - they don't seem to allow usage of even floating ips from hetzner. but ips of brightdata seem to work
- - pytest fails for these spiders on hetzner server.
