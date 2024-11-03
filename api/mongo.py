from pymongo import MongoClient
import os
import dotenv

dotenv.load_dotenv()

# Connect to the MongoDB database
client = MongoClient(os.environ.get("MONGO_URI"))
db = client.get_database("data_collection")
collection = db.get_collection("data")


qanda = """What are the latest trends in AI and machine learning?: Generative AI, reinforcement learning, ethical AI, and AI safety are major trends. Look for insights on VentureBeat and Towards Data Science.

Which programming languages are most in-demand for 2025?: Python, JavaScript, and Go are predicted to remain highly in-demand. Refer to sources like the TIOBE Index and Stack Overflow's Developer Survey.

What's new in cloud computing for startups?: Key advancements include hybrid cloud solutions, serverless architectures, and cost-effective AI/ML integration. TechCrunch and the AWS News Blog have the latest updates.

What are the best certifications for aspiring data scientists?: Popular certifications include Google's Data Analytics Certificate, IBM Data Science, and Microsoft's Azure AI. Look on Coursera or edX for options.

What are the top venture capital firms for tech startups in 2025?: Andreessen Horowitz, Sequoia Capital, and Y Combinator are among the top firms. CB Insights and PitchBook provide rankings and details.

What is Quantitative Analysis in finance, and how do you get into it?: Quantitative Analysis involves mathematical modeling for financial predictions; common paths include math, computer science, or finance degrees. Investopedia and QuantNet offer good starting points.

What are the most popular asset classes in 2025?: Equities, real estate, and alternative investments like private equity and cryptocurrency remain popular. Sources like Bloomberg and Morningstar have insights.

How is blockchain used in finance beyond cryptocurrency?: Blockchain is used in applications like supply chain finance, cross-border payments, and digital identity verification. IBM and Deloitte provide information on this expanding use case.

What are some tips for improving coding interview skills?: Practice problems on platforms like LeetCode, focus on data structures and algorithms, and do mock interviews with peers or online communities. GeeksforGeeks and Interview Cake offer structured paths.

How can I build a strong professional network in the tech industry?: Attend industry conferences, engage with professionals on LinkedIn, and join tech communities online or in your local area. LinkedIn and Meetup are good platforms for this.

What are the key differences between front-end and back-end development?: Front-end focuses on the user interface, while back-end handles the server, database, and application logic. W3Schools and MDN Web Docs have further explanations.

How is quantum computing expected to impact cryptography?: Quantum computing could break traditional cryptographic methods, leading to research in quantum-resistant algorithms. Sources like MIT Technology Review and IEEE Spectrum have detailed information.

What are the main roles in a typical startup team?: Key roles include CEO, CTO, product manager, software engineer, and marketing specialist. Crunchbase and AngelList have information on startup teams and roles.

What is the best way to get started with machine learning for beginners?: Learn Python, explore libraries like Scikit-Learn, and take online courses focused on supervised and unsupervised learning. Resources like Coursera and DataCamp are highly recommended.

What are common misconceptions about blockchain technology?: Some misconceptions include that it's only for cryptocurrency or that it's entirely secure. Information on this can be found in articles by IEEE Spectrum and industry blogs.

How is 5G expected to impact different industries?: 5G will enable faster data transfer, supporting innovations in areas like IoT, autonomous vehicles, and telemedicine. McKinsey and PwC have insights into these developments.

What are the key differences between Scrum and Agile methodologies?: Agile is a broad project management approach, while Scrum is a specific Agile framework with roles and rituals like sprints and stand-ups. Look for guides on Atlassian and the Scrum Alliance.

How can I effectively manage time when learning multiple programming languages?: Prioritize languages by relevance to your goals, set a consistent schedule, and use resources like online courses for structured learning. Sources like CodeAcademy and Medium have tips on this.

What is the best way to prepare for a tech internship interview?: Review core concepts, practice coding questions, and be ready to talk about past projects. Career blogs and LeetCode offer advice on this.

What are some up-and-coming fields in computer science?: Fields like quantum computing, ethical AI, and edge computing are gaining traction. Tech news sites and university research pages often highlight emerging areas.

What are the current challenges in autonomous vehicle technology?: Major challenges include safety in unpredictable environments, regulatory hurdles, and public acceptance. Automotive publications and tech news sites like Wired discuss these issues.

How does the Internet of Things (IoT) impact healthcare?: IoT enables remote patient monitoring, smart medical devices, and real-time health data collection. Research firms and industry blogs on IoT provide deeper insights.

What's the difference between supervised, unsupervised, and reinforcement learning in machine learning?: Supervised learning uses labeled data, unsupervised learning finds patterns in unlabeled data, and reinforcement learning trains models through trial and error. AI-focused websites and textbooks explain these types in detail.

What are some high-impact applications of blockchain beyond finance?: Blockchain is used in supply chain management, voting systems, and digital identity verification. Research articles and whitepapers by consulting firms cover this topic.

What are some essential skills for product managers in tech?: Skills include understanding market trends, user-centered design, project management, and cross-functional communication. Industry blogs and product management guides give more context.

What are the most effective ways to get user feedback on a tech product?: Techniques include surveys, user interviews, beta testing, and analytics tools. Look for resources from UX and product management blogs.

What are the biggest ethical concerns surrounding AI development?: Issues include bias in AI models, privacy concerns, and AI's potential impact on jobs. Tech publications and ethics-focused journals discuss these concerns.

What is digital twin technology, and how is it used?: Digital twins are virtual models of physical systems, used in manufacturing, logistics, and city planning for simulation and optimization. Engineering blogs and tech reports offer insights.

How can data science help improve decision-making in business?: Data science can identify trends, forecast outcomes, and optimize resource allocation, leading to data-driven decisions. Business schools and consulting firm websites have more on this.

What are key considerations for cybersecurity in startups?: Startups should prioritize data encryption, regular security audits, and employee training on cyber threats. Cybersecurity blogs and startup resources explain best practices.

How does augmented reality differ from virtual reality?: Augmented reality overlays digital elements on the real world, while virtual reality creates a fully immersive digital experience. Industry articles and tech blogs explain these differences.

What are some of the top tech conferences to attend for networking?: Major conferences include CES, Web Summit, and TechCrunch Disrupt, where professionals and innovators gather. Event websites and industry publications list top events.

How can artificial intelligence be used in education?: AI can personalize learning, automate grading, and provide real-time feedback for students. EdTech websites and educational journals discuss current AI applications in education.

What are some strategies for avoiding burnout in high-stress tech jobs?: Strategies include setting boundaries, taking regular breaks, and practicing mindfulness. Psychology and career advice websites offer strategies for managing burnout.

How is edge computing changing the way data is processed?: Edge computing processes data closer to where it's generated, improving speed and reducing latency, especially important for IoT and 5G. Tech publications explain edge computing's role.

What's the role of a software architect in a development team?: Software architects design the overall structure of software solutions, making high-level decisions on technologies and frameworks. Job description sites and tech career blogs cover this role.

What are some common misconceptions about machine learning?: Misconceptions include that machine learning is fully autonomous, or that it's the same as AI. Educational sites and tech articles clarify these points.

How does natural language processing (NLP) benefit businesses?: NLP can improve customer service through chatbots, automate content analysis, and provide language translation. Business journals and AI research sites highlight NLP applications.

What are some emerging job roles in tech that didn't exist a decade ago?: New roles include AI ethics manager, data scientist, blockchain developer, and DevOps engineer. Career sites and tech news publications discuss these newer roles.

What are some ways to make a mobile app accessible for all users?: Best practices include using alt text for images, voiceover support, and keyboard navigation. Accessibility guidelines and app design blogs offer tips.

How is data privacy regulated globally?: Different regions have their own laws, like GDPR in Europe and CCPA in California. Legal and privacy-focused websites provide an overview of global regulations.

What are some strategies to successfully scale a startup?: Effective strategies include optimizing operations, leveraging automation, and securing funding. Startup incubators and business advice websites offer guidance on scaling.

What are some tools for version control in software development?: Common tools include Git, SVN, and Mercurial, with Git being widely used through platforms like GitHub. Developer forums and tutorials offer guidance on these tools.

How is quantum cryptography different from traditional cryptography?: Quantum cryptography uses quantum mechanics principles, offering theoretically unbreakable encryption. Scientific journals and research articles discuss this emerging field.

What is DevOps, and why is it important for software development?: DevOps combines development and operations to improve software delivery speed and reliability. Tech blogs and DevOps guides explain its role and importance.

What are some techniques to optimize database performance?: Techniques include indexing, query optimization, and caching. Database management tutorials and forums provide in-depth tips.

What are the benefits of using open-source software in development?: Benefits include cost savings, community support, and faster innovation. Developer blogs and open-source advocacy sites discuss these advantages.

What is the difference between continuous integration and continuous deployment?: Continuous integration involves frequently merging code changes, while continuous deployment means automatically deploying every code change. DevOps resources explain these processes.

What are some effective strategies for managing remote tech teams?: Effective strategies include clear communication, setting regular check-ins, and using collaboration tools. Remote work blogs and leadership articles offer tips.

How can you enhance the performance of a web application?: Techniques include optimizing images, using lazy loading, and minimizing HTTP requests. Web development forums and optimization guides explain these methods."""

qanda = qanda.split("\n\n")


def insert_if_question_doesnt_exist(question, answer):
    if collection.find_one({"question": question}) is None:
        collection.insert_one({"question": question, "answer": answer})
        print(f"Inserted {question} into the database.")
    else:
        print(f"{question} already exists in the database.")

for i in range(len(qanda)):    
    question, answer = qanda[i].split(":")
    question, answer = question.strip(), answer.strip()
    insert_if_question_doesnt_exist(question, answer)


client.close()