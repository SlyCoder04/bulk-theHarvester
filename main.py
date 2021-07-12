from os import listdir
from subprocess import run

import xmltodict

DOMAINS_FILE = "path\\to\\file.txt"
OUTPUT_FOLDER = "path/to/output/"


def bulk_theharvester(domains: list[str]):
    """Runs theHarvester for a list of domains, creates .xml files in the output folder.

    Args:
        domains (list[str]): List of domain names
    """

    for domain in domains:
            print(f"Running domain: {domain}")
            command = f'wsl theHarvester --domain {domain.strip()} -b google,duckduckgo,yahoo,bing -g -f "{OUTPUT_FOLDER}{domain.strip()}"'
            print(f"Running command: {command}")
            run(command, shell=True)

def find_emails() -> list[str]:
    """Finds emails in bulk theHarvester output .xml files.

    Returns:
        list[str]: The list of emails found
    """

    files = listdir(OUTPUT_FOLDER)
    dicts = []
    for file in files:
        if ".html" in file:
            continue
        with open(f"{OUTPUT_FOLDER}{file}", "r") as f:
            dicts.append(xmltodict.parse(f.read()))

    emails = []
    for i in dicts:
        if not i["theHarvester"]:
            continue
        email = i["theHarvester"].get("email")
        if email:
            if type(email) == list:
                for j in email:
                    emails.append(j)
            else:
                emails.append(email)

    return emails

if __name__ == "__main__":
    with open(DOMAINS_FILE, "r") as file:
        domains = file.readlines()

    bulk_theharvester(domains)
    emails = find_emails()
    print("\n".join(emails))
