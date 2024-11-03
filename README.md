# Pragma

## Inspiration
In today’s data collection standards, research organizations frequently rely on manual data collection methods, often hiring multiple data collectors to access reliable and scalable data. This approach is both financially burdensome and time-consuming, significantly slowing down the research process. Team Pragma was inspired to innovate in this space by creating a streamlined, automated data collection tool that not only reduces costs and time but also enhances data reliability, particularly for fields like finance and education.

## What it does
Pragma automates the data collection process by gathering accurate and relevant information from verified online sources. Users can log into their accounts, enter organizations or topics they wish to research, and specify the questions they want answered. Pragma then compiles these inputs into structured search queries, retrieves reliable content from the web, processes it, and presents the information in a user-friendly interface. The platform also stores data for users, ensuring continuity and ease of access in future sessions.

## How we built it
Pragma’s backend utilizes a Node.js/Express server to manage user inputs and search queries. Our FastAPI application handles the data retrieval and structuring pipeline:
1. Google’s Search API identifies top resources, which are then scraped with Python’s requests and BeautifulSoup.
2. This unstructured content is filtered and formatted, creating JSON objects that capture each resource's title, date, and content, with metadata for added accuracy.
3. OpenAI’s Vector Embeddings API vectorizes the content, which we store in Pinecone for efficient similarity search and real-time query responsiveness.
4. The query is vectorized and matched against the vector database, leveraging Pinecone’s similarity scoring.
5. OpenAI’s Completions API and Databricks then organize and filter results before presenting them to the user.
6. MongoDB Atlas stores all data linked to the user account for future reference.

## Challenges we ran into
One of the key challenges was minimizing hallucinations that can arise with LLMs, especially when working with niche data fields. Additionally, managing the accuracy and structuring of web-scraped content required extensive testing and validation. Implementing a reliable vector database and efficiently querying it to support real-time data requests was also technically challenging, as was ensuring scalability and performance across various API integrations.

## Accomplishments that we're proud of
We’re proud to have created an automated data collection platform that bridges a crucial gap in research by providing a fast, cost-effective alternative to manual data collection. Our successful integration of multiple APIs, coupled with a robust data processing pipeline, demonstrates our commitment to innovation in data handling and analysis.

## What we learned
This project taught us the intricacies of handling real-time data retrieval and processing while maintaining accuracy. We gained valuable insights into embedding and querying techniques, web scraping challenges, and managing data storage for quick access. Additionally, we deepened our understanding of APIs like Google Search, Pinecone, and OpenAI’s suite, as well as the backend workflow required to manage large volumes of structured data.

## What's next for Pragma
Pragma’s next steps include refining our data validation processes and incorporating a human-in-the-loop review system for further accuracy. We aim to expand into more fields beyond finance and education, allowing for specialized data retrieval in healthcare, law, and other data-intensive industries. Furthermore, we plan to enhance our UI for seamless user interaction and explore additional vector database options to scale Pragma’s real-time search capabilities.

## Our Team
* [Alp Niksarli](https://github.com/alpnix/)
* [Murtaza Nikzad](https://github.com/murtazakafka/)
* [Hejin Wang](https://github.com/wanghejin/)
* [Sky Wang](https://github.com/skywang1234/)
