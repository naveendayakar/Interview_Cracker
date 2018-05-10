from bs4 import BeautifulSoup # For HTML parsing
import requests
from urllib.request import urlopen
import urllib.request as urllib2
import re # Regular expressions
from time import sleep # To prevent overwhelming the server between connections
from collections import Counter # Keep track of our term counts
from nltk.corpus import stopwords # Filter out stopwords, such as 'the', 'or', 'and'
import pandas as pd # For converting results to a dataframe and bar chart plots
get_ipython().magic('matplotlib inline')

def text_cleaner(website):
    try:
        site = urllib2.urlopen(website).read()# Connect to the job posting
    except: 
        return    
    
    soup_obj = BeautifulSoup(site,"lxml") # Get the html from the site
    
    for script in soup_obj(["script", "style"]):
        script.extract() # Remove these two elements from the BS4 object
    
    

    text = soup_obj.get_text() # Get the text from this
        
    
    lines = (line.strip() for line in text.splitlines()) # break into lines
    
        
        
    chunks = (phrase.strip() for line in lines for phrase in line.split("  ")) # break multi-headlines into a line each
    
    def chunk_space(chunk):
        chunk_out = chunk + ' ' # Need to fix spacing issue
        return chunk_out  
        
    
    text = ''.join(chunk_space(chunk) for chunk in chunks if chunk).encode('utf-8') # Get rid of all blank lines and ends of line
        
        
        
    try:
        text = text.decode("utf-8") # Need this as some websites aren't formatted
    except:                                                            # in a way that this works, can occasionally throw
        return                                                         # an exception
       
        
    text = re.sub("[^a-zA-Z.+3]"," ", text)  
        
       
    text = text.lower().split()  # Go to lower case and split them apart
        
        
    stop_words = set(stopwords.words("english")) # Filter out any stop words
    text = [w for w in text if not w in stop_words]
        
        
        
    text = list(set(text)) 
        
    return text


sample = text_cleaner('https://www.indeed.com/jobs?q=data%20Scientist&l&vjk=d5495782828f8403') 


sample[0:20]# Just show the first 20 words
m



def skills_info(city = None, state = None):
        
    final_job = 'data+scientist' # searching for data scientist exact fit("data scientist" on Indeed search)
    
    
    if city is not None:
        final_city = city.split() 
        final_city = '+'.join(word for word in final_city)
        final_site_list = ['http://www.indeed.com/jobs?q=%22', final_job, '%22&l=', final_city,'%2C+', state] # Join all of our strings together so that indeed will search correctly
    else:
        final_site_list = ['http://www.indeed.com/jobs?q="', final_job, '"']

    final_site = ''.join(final_site_list) 

    
    base_url = 'http://www.indeed.com'
    
    
    try:
        html = urllib2.urlopen(final_site).read() # Open up the front page of our search first
    except:
        'That city/state combination did not have any jobs. Exiting . . .' 
        return
    soup = BeautifulSoup(html,"lxml") # Get the html from the first page
    
    # Now find out how many jobs there were
    
    num_jobs_area = soup.find(id = 'searchCount').string 
    
    job_numbers = re.findall('\d+', num_jobs_area) # Extract the total jobs found from the search result
    
    print((job_numbers))
    # if len(job_numbers) > 3: # Have a total number of jobs greater than 1000
    #     total_num_jobs = (int(job_numbers[2])*1000) + int(job_numbers[3])
    # else:
    total_num_jobs = int(job_numbers[1]) 
    
    city_title = city
    if city is None:
        city_title = 'Nationwide'
        
    print ('There were', total_num_jobs, 'jobs found,', city_title) # Display how many jobs were found
    
    num_pages = total_num_jobs/10 # This will be how we know the number of times we need to iterate over each new
                                      # search result page
    job_descriptions = [] # Store all our descriptions in this list
    
    for i in range(1,int(num_pages+1)): # Loop through all of our search result pages
        print ('Getting page', i)
        start_num = str(i*10) # Assign the multiplier of 10 to view the pages we want
        current_page = ''.join([final_site, '&start=', start_num])
        # Now that we can view the correct 10 job returns, start collecting the text samples from each
            
        html_page = urllib2.urlopen(current_page).read().decode('utf-8') # Get the page
            
        page_obj = BeautifulSoup(html_page,"lxml") # Locate all of the job links
        job_link_area = page_obj.find(id = 'resultsCol') # The center column on the page where the job postings exist
            
        job_URLS = [base_url + link.get('href') for link in job_link_area.find_all('a') if link.get('href') != None]
        job_URLS = list(filter(lambda x:'clk' in x, job_URLS))
        
        
        for j in range(0,len(job_URLS)):
            final_description = text_cleaner(job_URLS[j])
            if final_description: 
                job_descriptions.append(final_description)
        sleep(1)  
        
    print ('Done with collecting the job postings!')    
    print ('There were', len(job_descriptions), 'jobs successfully found.')
    
    
    doc_frequency = Counter() # This will create a full counter of our terms. 
    [doc_frequency.update(item) for item in job_descriptions] # List comp
    

    
    prog_lang_dict = Counter({'R':doc_frequency['r'], 'Python':doc_frequency['python'],
                    'Java':doc_frequency['java'], 'C++':doc_frequency['c++'],
                    'Ruby':doc_frequency['ruby'],
                    'Perl':doc_frequency['perl'], 'Matlab':doc_frequency['matlab'],
                    'JavaScript':doc_frequency['javascript'], 'Scala': doc_frequency['scala']})
                      
    analysis_tool_dict = Counter({'Excel':doc_frequency['excel'],  'Tableau':doc_frequency['tableau'],
                        'D3.js':doc_frequency['d3.js'], 'SAS':doc_frequency['sas'],
                        'SPSS':doc_frequency['spss'], 'D3':doc_frequency['d3']})  

    hadoop_dict = Counter({'Hadoop':doc_frequency['hadoop'], 'MapReduce':doc_frequency['mapreduce'],
                'Spark':doc_frequency['spark'], 'Pig':doc_frequency['pig'],
                'Hive':doc_frequency['hive'], 'Shark':doc_frequency['shark'],
                'Oozie':doc_frequency['oozie'], 'ZooKeeper':doc_frequency['zookeeper'],
                'Flume':doc_frequency['flume'], 'Mahout':doc_frequency['mahout']})
                
    database_dict = Counter({'SQL':doc_frequency['sql'], 'NoSQL':doc_frequency['nosql'],
                    'HBase':doc_frequency['hbase'], 'Cassandra':doc_frequency['cassandra'],
                    'MongoDB':doc_frequency['mongodb']})
                     
               
    overall_total_skills = prog_lang_dict + analysis_tool_dict + hadoop_dict + database_dict # Combine our Counter objects
    
    final_frame_list = list(overall_total_skills.items()) # Convert these terms to a                                                                   # dataframe 
    final_frame=sorted(final_frame_list,key=lambda x: x[1])    
        
        
    return final_frame # End of the function
    


    
    
city_info = skills_info(city = 'Newark', state = 'NJ')
type(city_info)
city_info#list of tuples

set_skills=[i[0] for i in city_info]#splitting the tuple and getting only the skill set
common_skills=set_skills[-10:]#getting the top most common skills from all the html pages
common_skills
common_skills=[x.lower() for x in common_skills]#converting to lower case 



def trade_spider(lang):
        url = 'https://www.javatpoint.com/' + str(lang) + '-interview-questions'
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "lxml")
        #print(soup.contents)
        one = 1
        test =soup.findAll('td')
        path = "/Users/naveendayakar/Desktop/train_data.csv"
        for th in test:
            var = th.find_all('h3',{'class': 'h3'})
            #var1 = th.find_all('p')
            #var2 = th.find_all('hr')
            #var3 = th.find_all('item')
            if(var==[]):
                pass
            else:
                for en in var:
                    ques = en.string
                    #Hpg_Data['visit_datetime'] = Hpg_Data['visit_datetime'].map(lambda x: str(x)[:-9])
                    ques = ques[3:]
                    ques = ques.strip(' ')
                    #print(ques)
                    ques = ques.replace('\n','')
                    #appen_csv(path,ques) #print(en.string)
                    gh = en.find_next_sibling()
                    ans = gh.string
                    #print(gh.text)
                    if(ans==None):
                        ans = gh.text
                        ans = ans.strip('\n')
                    else:
                        ans = ans.strip('\n')
                    ij = gh.find_next_sibling()
                    if(ij.name=="hr"):
                        pass
                    elif(ij.name=="ul"):
                        ans = ans + ij.text
                        ans = ans.strip('\n')
                    elif(ij.name=="p"):
                        if(ij.string==None):
                            pass
                        else:
                            if(ans==None):
                                ans = ans + ij.text
                                ans = ans.strip('\n')
                            else:
                                ans = ans + ij.string
                                ans = ans.strip('\n')
                    else:
                        pass
                    if(ans==None):
                        pass
                    else:
                        ans = ans.replace('\n','')
                    qtype = "theory"
                    fields = [lang,ques,qtype,ans]
                    appen_csv(path,fields)
                    
       # for quest in soup.findAll('h3',{'class': 'h3'}):
       #     conten = quest.string
       #     #appen_csv(path,conten)
       #     #one += 1
       # page += 1

def write_file(path,header):
    import csv
    with open(path,'w',newline='') as file:
        csvwriter=csv.writer(file)
        csvwriter.writerow(header)

def appen_csv(path,fields):
    import csv
    with open(path,'a',newline='') as file:
            csvwriter = csv.writer(file)
            csvwriter.writerow(fields)
            #file.write(conten + '\n')

#lang = 'python'
header=['Domain','Question','Question_type','Answer']
path = "/Users/naveendayakar/Desktop/train_data.csv"
write_file(path,header)
##for loop that will take all the common skills and write interview ques into a CSV
for lang in common_skills:
    trade_spider(lang)


