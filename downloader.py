import os
import multiprocessing
from bs4 import BeautifulSoup
import requests

pdf_dir= "./Project/NAACL Conference Papers/pdf/"                # Folder in VS code root directory to store downloaded pdf files

downlink = {
    2018: [ "https://aclanthology.org/events/naacl-2018/"            # Website to scrape the NAACL 2018 Papers
            ],
    2019: [ "https://aclanthology.org/events/naacl-2019/"            # Website to scrape the NAACL 2019 Papers
            ]
}

def getPath(root_dirs):
        for root_dir in root_dirs:                       # Check if the directory exits    
                if not os.path.isdir(root_dir):          # Makes the directory if already not present
                        os.makedirs(root_dir)
                else:
                        for entity in os.listdir(root_dir):
                                if os.path.isfile(os.path.join(root_dir, entity)):    # Checks files in the directory
                                        os.remove(os.path.join(root_dir, entity))     # Removes preexisting paths to prevent filepath errors


def getLink():                                        # Function to scrape all downloadable links of pdf files
        files : list[str] = []
        for weblink in (downlink[2018] + downlink[2019]):     # Queries the mentioned websites to scrape for downloadable links
                page = requests.get(weblink)
                soup = BeautifulSoup(page.content, "html.parser")
                results = soup.find_all("a", class_="badge badge-primary align-middle mr-1", href=True)   # Searchess this section in the html source to get downloadable links
                for pdf_element in results:
                        files.append(pdf_element["href"])
        return files 


def downloader(pdf_link, suffix):                  # Writes the downloader data to the pdf file created locally
        response = requests.get(pdf_link)
        with open(f"{pdf_dir}doc{suffix}.pdf", 'wb') as f:
                f.write(response.content)


def fetch():                                       # Fetches the download link for the downloader function to process
        files = getLink()
        indexer = list(range(0, len(files)))
        packed_args = tuple(zip(files, indexer))

        with multiprocessing.Pool(processes=50) as pool:   # Enables multi file processing for accelerated downloading
                pool.starmap(downloader, packed_args)


def task():                                            # Function to shot the execution time and progress of the program
        getPath([pdf_dir])
        print("Scavenging the website and downloading the Research Papers.... please be patient....\n")
        fetch()
        print(f"All the Research Papers have been downloaded successfully.... \nYou may now proceed for conversion")


if __name__ == "__main__" :
        task()
