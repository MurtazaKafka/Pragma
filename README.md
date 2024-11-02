# AutoData

**Tasks:**
- Backend:
  - Web scraping 
  - RAG implementation
  - Retrieving data relevant to input questions and organizations
  - Structuring retrieved data in a parsable format (JSON)
  - Converting JSON file to CSV file
- Frontend:
  - Landing Page:
    - 1st text input (research questions; rows)
    - 2nd text input (organizations involved; columns)
    - Submit button
    - CSV file retrieved (with options to download and view; should open modals)
  - About Page:
    - A small description of the projects and some stuff about ourselves.


**Workflow:** User provides research questions and organizations for which they want to collect the data relevant for their research question. They submit it. The submit button should call the web scraping function for the research questions and organizations. For each row i and column j, the scraping performs a single search. There will be i * j search operations performed only on the inputs. For each input around 5 top links should be scrapped. In total, only searching for the data takes us i * j * 5 operations. Once all the data is collected, we call the OpenAI API and store the vectorized formats of the data in PineCone. Then we make i * j number of calls to our vector database and for each time we feed it question i and organization j. Afterwards, we feed the retrieved data from the database to our LLM. We prompt-engineer the LLM to provide the answer to each of the questions in a parsable format like JSON. We provide a JSON schema for our expected response. We submit the prompt to the LLM. Afterwards, we get the JSON data and call a function to convert the data into a csv file. The csv file will be sent to the frontend where it will be ready to be viewed and/or downloaded. 
