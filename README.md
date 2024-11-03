# Pragma

## Inspiration
In today’s data collection standards, research organizations frequently rely on manual data collection methods, often hiring multiple data collectors to access reliable and scalable data. This approach is both financially burdensome and time-consuming, significantly slowing down the research process. There have been attempts at automating this process by large language models, however the outputs that these models prvoide are not very reliable. Trying to solve this problem, we were able to create a maximally accurate automated data collector by grounding the outputs of large language models to the factual information scrapable from the internet. We have used Retrieval Augmented Generation in order to ground the data we can scrape from the web and create a similarity score between the data points that come as inputs and the organizations from which we try to collect data. This tool enables:

- Precise similarity scoring between input queries and source organizations
- Verification of data points against real-world sources
- Reliable automation that maintains accuracy while reducing costs


Our solution emerged from recognizing the urgent need for a pragmatic tool that could bridge the gap between manual reliability and automated efficiency, particularly in data-intensive fields like finance and education.

## What it does
Pragma automates the data collection process by gathering accurate and relevant information from verified online sources. Users can log into their accounts, enter organizations or topics they wish to research, and specify the questions they want answered. Pragma then compiles these inputs into structured search queries, retrieves reliable content from the web, processes it, and presents the information in a user-friendly interface. The platform also stores data for users, ensuring continuity and ease of access in future sessions.

## How we built it
Pragma’s frontend is built on React and Tailwind while backend utilizes a Node.js/Express server. Our FastAPI applications handle the entire data retrieval and structuring pipeline:
1. Google’s Search API identifies top resources, which are then scraped with Python’s requests and BeautifulSoup.
2. This unstructured content is filtered and formatted, creating JSON objects that capture each resource's title, date, and content, with metadata for added accuracy using regular expressions and datetime objects.
3. OpenAI’s Vector Embeddings API vectorizes the content, which we store in Pinecone for efficient similarity search and real-time query responsiveness.
4. OpenAI’s Completions API and Databricks then organize and filter results before presenting them to the user.
5. MongoDB Atlas stores all data linked to the user account for future access capabilities.

Apart from the code, we have utilized tools like Figma, Terraform, or certain Databricks services to ensure the functionality of our UX and DevOps. 

### Sponsor Product Integrations
- **Databricks:**: We have fully utilized Databricks to support RAG process with multiple LLM functions. 
  - Cleaning data and creating a vector database for retrieval
  - Databricks Jumpstart Package
  - Setting up the AI Gateway
  - Using ChatDataBricks for completion after retrieval for generating a response for the user 
- **MongoDB Atlas:** We used MongoDB in a few ways in our project. Firstly, we set a up a cluster and two collections in our remote Atlas directory. We utilized MongoDB along with JWT for user authentication. Additionally, we used MongoDB's efficiency querying and storage for saving large amounts of data that is being fetched on the frontend. Due to being able to store this large amount of data on MongoDB, we provide our users an option to view and go back to their old data collections. 
- **Terraform:** Due to having multiple components of our application ─ frontend React app, backend Express app, two FastAPI apps ─ we had to run multiple tests for our deployments which was possible through Terraform. 
- **.Tech Domains:** Since pragma.tech was taken, we decided to take [getpragma.tech](getpragma.tech) which fits our slogan Get Pragmatic, Get Data.

## Challenges we ran into
One of the key challenges was minimizing hallucinations that can arise with LLMs, especially when working with niche data fields. Additionally, managing the accuracy and structuring of web-scraped content required extensive testing and validation. Implementing a reliable vector database and efficiently querying it to support real-time data requests was also technically challenging, as was ensuring scalability and performance across various API integrations.

## Accomplishments that we're proud of
We’re proud to have created an automated data collection platform through a fully working RAG process from contextual web scraping and embeddings to retrieval and completions. Our successful integration of multiple APIs, including but not limited to Google Search API and OpenAI's Vector Embedding and Completion API, coupled with our robust data processing pipeline makes us proud.

## What we learned
We gained valuable insights into how language can be represented as a set of relations of different vectors. We learnred techniques such as embedding and querying, web scraping, and managing data storage for quick access. Additionally, we deepened our understanding of APIs like Google Search, Pinecone, and OpenAI’s suite, as well as the backend workflow required to manage large volumes of structured data.

## What's next for Pragma
Pragma’s next steps include refining our data validation processes and incorporating a human-in-the-loop review system for further accuracy. We aim to expand into more fields beyond finance and education, allowing for specialized data retrieval in healthcare, law, and other data-intensive industries. Furthermore, we plan to enhance our UI for seamless user interaction and explore additional vector database options to scale Pragma’s real-time search capabilities.


## Our Team
* [Alp Niksarli](https://github.com/alpnix/)
* [Murtaza Nikzad](https://github.com/murtazakafka/)
* [Hejin Wang](https://github.com/wanghejin/)
* [Sky Wang](https://github.com/skywang1234/)
