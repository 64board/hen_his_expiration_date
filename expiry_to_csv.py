import csv

with open('eggs.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'] + [10])
    spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])