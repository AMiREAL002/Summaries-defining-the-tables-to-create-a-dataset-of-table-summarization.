import os
import multiprocessing
from downloader import getPath

CPU_count = multiprocessing.cpu_count() * 4     # Multiprocessing functionality to specify the number of CPU cores to be provissioned for tasking

txt_dir = "./Project/NAACL Conference Papers/to_txt/"                # Path to the converted pdf files
final_out_dir = "./Project/NAACL Conference Papers/final_txt/"       # Path to store the final output.txt file


def scrapper(sum: str) -> str:       
    sum = sum.strip()    
    if len(sum) != 0:
        if sum.strip()[0] == '\n':           # Removes unecessary blank spaces in the string for better formatting
            sum = f"{sum[1:]}"            
    sum = sum.replace("\n", "\n\t\t")
    return sum


def extractSum(_lines: list[str], _table_no, _paper_no) -> str:    # function to extact and generate the syntax for the output.txt file
    abs_sum: str = ""
    ext_sum: list[str] = []
    fsum: str = ""
    if_table: bool = False
    fsum += f"<Paper ID={_paper_no}> <Table ID ={_table_no}>\n"        # Provides the paper and table id at the start of each block

    for line in _lines:
        search_str: str = f"Table {_table_no}"           # Checks for the presence of the substring table in each line
        search_str_len: int = len(search_str)
        index = line.find(search_str)
        if index != -1:
            if_table = True
            if(len(line) < index + search_str_len + 1):  # Searches for character ":" after the Table substring
                continue
            next_char = line[index + search_str_len]
            if next_char == ":":                         # To determine whether the line is abstractive or extractive in nature ; abs - Table no: ; ext - Table no ....
                abs_sum += line
            else:
                ext_sum.append(line)

    if if_table:
        fsum += f"\t<Abstractive Summary> =\n\t\t{scrapper(abs_sum)}\n\t</Abstractive Summary>\n"        # Generates the abstractive sum
        
        for refext_sum in ext_sum:
            fsum += f"\t<Extractive Summary> =\n\t\t{scrapper(refext_sum)}\n\t</Extractive Summary>\n"   # Generates the extractive sum and adds it to fsum 
        fsum += f"</Paper ID={_paper_no}>\n\n\n"                                                         # Provides the paper id at the end of each block
    else:
        fsum = ""

    return fsum    # Stores the entire chunk of abstractive and extractive sum data in a string


def toParser(txt_file_name) -> str:
    suffix = txt_file_name[txt_file_name.index("doc") + 3:txt_file_name.index(".txt")]      # Gets the name of the files in the to_txt directory
    root_txt_path = os.path.join(txt_dir, f"doc{suffix}.txt")                           # Gets the file path to the previously converted txt files 
    text_buffer: str = ""                                                                   # Variable to store scrapped text from the txt files

    if os.path.isfile(root_txt_path):
        with open(root_txt_path, "r", encoding="utf-8") as src_txt_file:
            lines = src_txt_file.read().split(".")                          # Reading txt files line by line
            text = ""
            
            for line in lines:                   # Reads the txt files line by line
                line = line.strip() + "."        # Strips the sentence and is stored 
                text += f"A Line:\n {line}\n"                
            
            for table_no in range(1, 100):
                sum: str = extractSum(
                    lines, table_no, suffix)
                if sum == "":
                    break
                else:
                    text_buffer += sum       # Updates incoming sum content 
                    
    return text_buffer


def toProcessor() -> None:
    files_to_parse: list[str] = os.listdir(txt_dir)
    text_buffer: str = ""
    
    with multiprocessing.Pool(processes=CPU_count) as pool:     # Accelerates the speed for reading from the previously converted txt files using multiprocessing
       pool.map(toParser, files_to_parse)

    for file in files_to_parse:
        text_buffer += toParser(file)             # continuouslt updates the extracted table content in a string

    with open(final_out_dir+"output.txt", "w", encoding="utf-8") as final_out:       # keeps writing the extracted abstractive and extractive sum to the same output.txt file
        final_out.write(text_buffer)


def getTask() -> None:              # function to initiate the conversion process
    getPath([final_out_dir])
    print("Generating the final Text Output File.... please be patient ....")
    toProcessor()
    print(f"Output.txt file generated successfully\n")


if __name__ == "__main__":
    getTask()