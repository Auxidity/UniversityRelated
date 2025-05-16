# Chatbot Training Data Generation Process
## Disclaimer
Useage of AI generated text is widely present

Author: Daniel Kortesmaa

## Table of Contents
1. Introduction and Objective
2. Research and Planning
3. Implementation
4. Testing and Results
5. Conclusion and Future Work
6. References

## 1. Introduction and Objective
The objective of this project is to generate training data for a RASA chatbot using data collected from Reddit and processing it to create structured YAML files. The chatbot aims to provide responses based on the topics discussed in the Reddit posts and comments. The chatbot itself will not be implemented.

## 2. Research and Planning
The foundation of this project draws inspiration from various sources, including educational content from sentdex's YouTube videos on machine learning techniques[1]. These resources provide valuable insights into data processing, natural language understanding, and chatbot development methodologies. Additionally, the project leverages the power of OpenAI's ChatGPT model for generating responses, utilizing its advanced language processing capabilities to create coherent and contextually relevant dialogue[2]. 

The project utilizes several scripts to collect data from Reddit, process it, filter out relevant information, and then convert it into YAML format suitable for training a chatbot. The primary tools used for this project are Python along with the PRAW library for Reddit API access and OpenAI's GPT-3.5 model for generating responses.

## 3. Implementation
### Implementation Plan:
####  Reddit Data Collection Algorithm (crawler.py): 
This script collects raw data from a specified subreddit using the Reddit API. It retrieves both post data and their associated comments[3]. 

##### Data Structures Used: 
List of Dictionaries. Each dictionary represents a Reddit post along with its associated comments. The keys in the dictionary correspond to attributes such as post title, content, author, etc.

#### Data Filtering Algorithm
##### Preliminary Data Processing (preliminary_data_processing.py): 
The collected raw data is split into separate files based on topics, with each file containing the post and its comments[3].
##### Data Structures Used: 
File I/O. The script utilizes file handling operations to organize the raw data into separate files based on predefined topics.

##### Secondary Data Processing (secondary_data_processing.py): 
This script filters out posts and comments based on specified criteria, such as post score and comment score, to ensure that only relevant data is included[3].
##### Data Structures Used: 
List of Dictionaries. Similar to the Reddit Data Collection Algorithm, the filtered data is stored as a list of dictionaries, with each dictionary representing a post and its associated comments.

#### Conversation Structuring Algorithm (tertiary_data_processing.py): 
The filtered data is structured into parent-child conversation pairs, representing the flow of discussions within each topic[3].
##### Data Structures Used: 
Nested Lists. The conversation structure is represented using nested lists, where each list contains parent-child pairs representing the flow of discussions within a topic.

#### Response Generation Algorithm (yamlifier.py): 
The structured data is then passed through the GPT-3.5 model to generate YAML files containing intents and responses suitable for training the chatbot[3].
##### Data Structures Used: 
YAML Format. The script generates YAML files to represent intents and responses. These files encapsulate structured data suitable for training the chatbot.

#### Database Insertion Algorithm (db_insertion.py): 
YAML files are inserted into a SQLite database to store the training data[3].
##### Data Structures Used: 
SQLite Database. The script utilizes SQLite to store the training data. SQLite databases organize data into tables, providing efficient storage and retrieval mechanisms.

#### Database Training Data Creation Algorithm (db_create_training_data.py): 
A single YAML file containing all the data from the SQLite database is created, serving as the final training dataset for the chatbot[3].
##### Data Structures Used: 
File I/O. Similar to the Preliminary Data Processing step, file handling operations are employed to create a YAML file containing the training data from the SQLite database.

#### Raw Data Cleaner Script (raw_data_cleaner.py):
Automation script that executes all the aforementioned steps sequentially to create the final training data. Additionally, it handles data cleaning and error handling for better processing efficiency[3].
##### Data Structures Used: 
N/A. The script orchestrates the execution of other processing steps and does not manipulate data directly.

### Overview
The implementation involves a series of Python scripts orchestrated to collect, process, filter, and structure the raw Reddit data into a usable format for chatbot training. Each script serves a specific purpose and contributes to the overall data generation pipeline.

## 4. Testing and Results
The generated training data consists of YAML files containing intents and responses derived from Reddit discussions. The data is structured and organized, ready for training the RASA chatbot. Test cases can be performed by feeding the generated data into the chatbot and evaluating its responses against expected outcomes.

For testing purposes, a singular YAML file named "golden_answer.yaml" was created, containing manually curated intents and responses that represent the ideal outcome of the chatbot's training data. This file serves as the benchmark against which the output generated by the GPT-3.5 model is compared. During testing, the YAML file is used as input for the GPT-3.5 model via an API call, and the resulting responses are evaluated manually for accuracy and coherence. Any discrepancies or deviations from the expected responses are noted and analyzed to identify potential areas for improvement in the data processing pipeline. This testing approach ensures that the chatbot's training data aligns closely with the desired outcome, facilitating the development of a high-quality conversational agent.

### Analysis of Results
Throughout the testing phase, it became evident that a notable portion of the generated data exhibited poor formatting or coherence issues, which required further attention. In response to this challenge, the data processing pipeline was designed to offer flexibility to the user. Rather than enforcing a specific approach, the pipeline allows users to choose between manual intervention or attempting automated fixes for the poorly formatted data. This discretionary approach empowers users to tailor the data correction process according to their preferences and requirements. Whether opting for manual refinement to ensure precision or exploring automated solutions for efficiency, users can navigate the data processing pipeline with autonomy. By providing this flexibility, the testing process promotes a collaborative effort between human oversight and automated tools, facilitating iterative improvements in the quality of the training data and the overall performance of the chatbot.

The solution implemented for data processing in this project may appear somewhat inefficient in terms of space management, as it involves creating intermediate files and directories at various stages of the pipeline. However, this approach proves to be practical and effective, particularly when dealing with moderate-sized datasets and incremental updates to the training data. While it may not be the most space-efficient solution for handling massive amounts of data, it strikes a balance between simplicity, reliability, and ease of implementation. Additionally, it mitigates the risk of API timeouts due to excessive calls, ensuring the smooth execution of the data processing pipeline. Overall, while there may be room for optimization in terms of space management, the current solution meets the project's requirements effectively.

### Complexity Analysis
#### Crawler Script (crawler.py):
This script, responsible for fetching raw data from a specified subreddit using the Reddit API, operates with a time complexity of O(n), where n represents the number of Reddit posts and comments fetched. Its space complexity is minimal, typically O(1), as it processes data in batches without storing significant amounts of data in memory.

#### Preliminary Data Processing (preliminary_data_processing.py):
After the raw data collection, the preliminary data processing script splits the collected data into separate files based on topics, with each file containing posts and associated comments. This operation involves a time complexity of O(n), where n is the number of posts and comments processed. Additionally, its space complexity is O(n) as it creates separate files for each topic, potentially increasing disk space usage linearly with the number of topics.

#### Secondary Data Processing (secondary_data_processing.py):
The secondary data processing script filters out posts and comments based on specified criteria, such as post score and comment score, to ensure that only relevant data is included. With a time complexity of O(n), where n is the number of filtered posts and comments, and a space complexity ranging from O(1) to O(n), depending on the data structures used for temporary storage, this script efficiently manages data filtration.

#### Tertiary Data Processing (tertiary_data_processing.py):
This script structures the filtered data into parent-child conversation pairs, representing the flow of discussions within each topic. Its time complexity is O(n), where n is the number of filtered posts and comments processed, while its space complexity is O(n) as it utilizes additional data structures to store conversation pairs.

#### YAMLifier (yamlifier.py):
The YAMLifier script passes the structured data through the GPT-3.5 model to generate YAML files containing intents and responses suitable for training the chatbot. With a time complexity of O(n) and space complexity of O(n), where n is the number of conversation pairs processed, this script efficiently generates training data while maintaining the integrity of the conversations.

#### Database Insertion (db_insertion.py):
As YAML files are generated, the database insertion script inserts them into a SQLite database to store the training data. It operates with a time complexity of O(n), where n is the number of YAML files inserted into the database, and a space complexity of O(n) as the database size grows with the insertion of YAML files.

#### Database Training Data Creation (db_create_training_data.py):
This script aggregates all YAML files from the database to create a single training dataset. Its time complexity is O(n), where n is the number of YAML files processed, and its space complexity is O(n) as the final training dataset grows in size proportional to the number of YAML files combined.

#### Raw Data Cleaner (raw_data_cleaner.py):
The raw data cleaner script orchestrates all the aforementioned steps sequentially and handles data cleaning and error handling. With a time complexity of O(n) and space complexity ranging from O(1) to O(n), depending on the specific operations performed during cleaning and temporary storage requirements, it efficiently prepares the data for further processing.

These complexity analyses provide insights into the performance characteristics of each script.

### Cumulative Complexity Analysis:
The data generation pipeline comprises several scripts, each with its own time and space complexity. As these scripts are executed sequentially, their individual complexities contribute to the overall performance characteristics of the pipeline. Since many of these scripts have a time complexity of O(n), where n represents the size of the input data or processed entities, the cumulative time complexity of the pipeline can indeed be approximated as O(N), where N is the total size of the dataset processed across all scripts.

However, it's important to note that the space complexity of the pipeline may not scale linearly due to the accumulation of intermediate files and data structures created by each script. While individual scripts may have a linear space complexity, the cumulative space requirements of the pipeline could potentially exhibit exponential growth, especially when processing large datasets or executing resource-intensive operations. This exponential growth in space complexity underscores the importance of efficient resource management and cleanup procedures to mitigate the risk of excessive resource utilization and storage overhead.

Moreover, at the conclusion of the pipeline, the raw data cleaner script performs cleanup operations to remove excessive files and optimize storage usage. This cleanup phase introduces an additional time complexity, typically O(m), where m represents the number of files or entities removed. However, since this cleanup operation is performed once at the end of the pipeline, its impact on the overall time complexity is minimal compared to the cumulative complexity of the preceding scripts.

In summary, while the time complexity of the pipeline remains linear due to sequential execution, the space complexity may exhibit exponential growth, necessitating careful consideration of resource utilization and cleanup strategies to ensure efficient processing and resource management.

## 5. Conclusion and Future Work
In conclusion, the project successfully achieves its objective of generating training data for a chatbot using Reddit data and OpenAI's GPT-3.5 model. Future work may involve refining the data processing pipeline, improving filtering criteria, and optimizing response generation to enhance the chatbot's performance and accuracy. Additionally, ongoing maintenance and updates to adapt to changes in Reddit content and user interactions may be necessary. In the far future, it is also on the table to actualize a chatbot using the data that can be gathered using this project. Time spent on the entire project is approximately 14 hours.

## 6. References

[1] Sentdex. "Sentdex YouTube Channel." [Online]. Available: [[link to Sentdex YouTube channel](https://www.youtube.com/@sentdex/)]. Accessed: [16/03/2024].

[2] OpenAI. "ChatGPT: A Large-Scale Generative Pretrained Transformer for Conversational Response Generation." [Online]. Available: [[chat.openai.com](https://chat.openai.com/)]. Accessed: [16/03/2024].

[3] Daniel Kortesmaa. "Source code repository." [Online]. Retrieved from [[Link to source code](https://git.dc.turkuamk.fi/edu.daniel.kortesmaa/algoritmit/-/tree/main/CourseProject/src?ref_type=heads)]. Accessed: [16/03/2024].