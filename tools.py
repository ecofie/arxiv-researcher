import arxiv
import requests # make a request to the server to download the pdf file
import os       # create a directory if it doesnt exist to save the pdf file to the local disk

# Construct the default API client.
client = arxiv.Client()

#function to fetch arxiv papers
def fetch_arxiv_papers(title:str,paper_count:int):
    search_query = f'all:"{title}"'
    # Search for the 10 most recent articles matching the keyword "quantum."
    search = arxiv.Search(
        query = search_query,
        max_results = paper_count,
        sort_by = arxiv.SortCriterion.SubmittedDate
    )
    
    papers = []
    results = client.results(search)
    for result in results:
        paper_info = {
            'title': result.title,
            'summary': result.summary,
            'published': result.published,
            'journal_ref' : result.journal_ref,
            'doi': result.doi,
            'primary_category': result.primary_category,
            'categories': result.categories,
            'authors': [author.name  for author in result.authors],
            'pdf_url': result.pdf_url,
            'arxiv_url': result.entry_id,
        }
        papers.append(paper_info)
    return papers

def download_pdf(pdf_url:str, output_file_name:str):
    try:
        os.makedirs("papers", exist_ok=True)  # create a directory to save the pdf files
        full_output_path = os.path.join("papers", output_file_name)
        response = requests.get(pdf_url)
        response.raise_for_status() #this raises an http error if the response is not ok
        with open(full_output_path, 'wb') as file:
            file.write(response.content)
        return f"PDF file downloaded successfully to {full_output_path}"
    except response.exceptions.RequestException as e:
        return f"Error downloading the pdf file: {e}"
        
    