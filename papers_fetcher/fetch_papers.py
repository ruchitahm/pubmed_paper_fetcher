import requests
import pandas as pd
import re
import click

# PubMed API URLs
SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
DETAILS_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

@click.command()
@click.option("-d", "--debug", is_flag=True, help="Enable debug mode for detailed logs.")
@click.option("-f", "--file", default="pubmed_papers.csv", help="Specify filename to save results.")
@click.option("--max_results", default=10, help="Number of results to fetch from PubMed.")
def fetch_pubmed_papers(debug, file, max_results):
    """Fetches research papers from PubMed and saves them to a CSV file."""

    # Prompt user for search query
    query = click.prompt("Enter your search query")

    if debug:
        click.echo(f"Debug Mode: Fetching papers for query: {query}")

    # Step 1: Get list of PubMed IDs for the query
    search_params = {
        "db": "pubmed",
        "term": query,  # Uses user input query
        "retmode": "json",
        "retmax": max_results
    }
    search_response = requests.get(SEARCH_URL, params=search_params)

    if debug:
        click.echo(f"PubMed API Response: {search_response.status_code}")

    search_response.raise_for_status()
    search_data = search_response.json()
    pubmed_ids = search_data.get("esearchresult", {}).get("idlist", [])

    if not pubmed_ids:
        click.echo("No papers found for the given query.")
        return

    # Step 2: Fetch details for each paper
    details_params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "json"
    }
    details_response = requests.get(DETAILS_URL, params=details_params)

    if debug:
        click.echo(f"Fetching details for {len(pubmed_ids)} papers...")

    details_response.raise_for_status()
    details_data = details_response.json().get("result", {})

    papers = []
    for pmid in pubmed_ids:
        paper = details_data.get(pmid, {})

        # Extract fields
        title = paper.get("title", "N/A")
        pub_date = paper.get("pubdate", "N/A")
        authors = paper.get("authors", [])

        # Extract Non-academic Authors & Company Affiliations
        non_academic_authors, company_affiliations = extract_company_authors(authors)

        # Extract Corresponding Author Email
        corresponding_email = extract_corresponding_email(paper)

        papers.append({
            "PubmedID": pmid,
            "Title": title,
            "Publication Date": pub_date,
            "Non-academic Authors": ", ".join(non_academic_authors),
            "Company Affiliations": ", ".join(company_affiliations),
            "Corresponding Author Email": corresponding_email
        })

    # Step 3: Always Save to CSV (even if -f is not provided)
    df = pd.DataFrame(papers)
    df.to_csv(file, index=False)
    click.echo(f"Results saved to {file}")

def extract_company_authors(authors):
    """Identify authors with company affiliations."""
    non_academic_authors = []
    company_affiliations = []

    for author in authors:
        affiliation = author.get("affiliation", "")
        if affiliation and not is_academic(affiliation):
            non_academic_authors.append(author.get("name", "Unknown"))
            company_affiliations.append(affiliation)

    return non_academic_authors, company_affiliations

def is_academic(affiliation):
    """Heuristic to determine if an affiliation is academic."""
    academic_keywords = ["university", "institute", "college", "school", "hospital"]
    return any(keyword in affiliation.lower() for keyword in academic_keywords)

def extract_corresponding_email(paper):
    """Extract corresponding author's email."""
    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    abstract_text = paper.get("abstract", "")

    emails = re.findall(email_pattern, abstract_text)
    return emails[0] if emails else "Not Available"

if __name__ == "__main__":
    fetch_pubmed_papers()
