import csv
from io import BytesIO, TextIOWrapper
from urllib.request import Request, urlopen
from zipfile import ZipFile


URL = "https://www.ssa.gov/oact/babynames/names.zip"


def main():
    # Send a non-default User-Agent header so the SSA firewall allows the download
    request = Request(URL, headers={"User-Agent": "Wget/1.21.4"})
    with urlopen(request) as response:
        archive_data = response.read()

    with ZipFile(BytesIO(archive_data)) as archive:
        with open("ssa-baby-names.csv", "w", newline="", encoding="utf-8") as output:
            writer = csv.writer(output)
            writer.writerow(["year", "name", "sex", "count"])

            for filename in sorted(archive.namelist()):
                if not filename.startswith("yob") or not filename.endswith(".txt"):
                    continue

                year = filename[3:7]
                with archive.open(filename) as source:
                    reader = csv.reader(TextIOWrapper(source, encoding="utf-8"))
                    for name, sex, count in reader:
                        writer.writerow([year, name, sex, count])


if __name__ == "__main__":
    main()
