import csv

url_set = set()
no_of_duplicates = 0

with open('links_clean.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    #print(f"no of urls found {len(list(reader))}")
    for row in reader:
        url = row[0].strip()
        if url in url_set:
            no_of_duplicates += 1
            print(f"Duplicate URL found: {url}")
        else:
            url_set.add(url)

print(f"No of duplicates found {no_of_duplicates}")
print("Duplicate check complete!")

# Initialize the CSV writer
csv_file = open('links_nodups.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
for link_url in url_set:
    if 'jpg' in link_url:
        continue
# Write the link URL to the CSV file
    csv_writer.writerow([link_url])
# Close the CSV file
csv_file.close()
