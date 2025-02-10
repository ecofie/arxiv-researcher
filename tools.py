import arxiv  #to access the arxiv data source
import requests # make a request to the server to download the pdf file
import os       # create a directory if it doesnt exist to save the pdf file to the local disk


#refer to the arxiv documentation for more information on how to use the arxiv python library
# Construct the default API client().
client = arxiv.Client()

#function to fetch arxiv papers (A research paper fectch tool)
def fetch_arxiv_papers(title:str,paper_count:int):
    search_query = f'all:"{title}"'  # the search query for for all with the titles
   
    # Search for the "paper count" most recent articles matching the keyword "title."
    search = arxiv.Search(
        query = search_query,
        max_results = paper_count,
        sort_by = arxiv.SortCriterion.SubmittedDate
    )
    
    papers = []
    results = client.results(search)  # a generator object that yields the search results
    
    #create a list of dictionaries containing the paper information
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


#the downlod too:function to download the pdf file of a research paper
def download_pdf(pdf_url:str, output_file_name:str):
    try:
        os.makedirs("papers", exist_ok=True)  # create a directory to save the pdf files, exist_ok=True means it will not raise an error if the directory already exists
        full_output_path = os.path.join("papers", output_file_name) # create the full path by joining the directory(paper) and the file name
        response = requests.get(pdf_url) #making an http request through the url in other to have access to the content of the site 
        response.raise_for_status() #this raises an http error if the response is not ok
        with open(full_output_path, 'wb') as file: #open the file in binary write mode
            file.write(response.content) #write the content of the response to the file
        return f"PDF file downloaded successfully to {full_output_path}" #return the full path of the directory 
    except response.exceptions.RequestException as e:
        return f"Error downloading the pdf file: {e}"
        
    