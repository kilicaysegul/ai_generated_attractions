import json, re, collections

with open("attractions_recent.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Total records:", len(data))

# Check for missing fields
missing = [i for i, x in enumerate(data, 1)
           if not all(k in x for k in ("name", "city", "description", "coordinates"))]
print("Records with missing fields:", len(missing))

# Year condition: description must contain Opened in 2021–2025
yr_pat = re.compile(r"Opened in (2021|2022|2023|2024|2025)")
ok = sum(1 for x in data if yr_pat.search(x["description"] or ""))
print("Records satisfying year condition:", ok)

# Show a couple of sample records
for x in data[:2]:
    print("Sample record:", x)

# Count how many records per year
years = collections.Counter(
    yr_pat.search(x["description"]).group(1)
    for x in data if yr_pat.search(x["description"])
)
print("Year distribution:", dict(years))
