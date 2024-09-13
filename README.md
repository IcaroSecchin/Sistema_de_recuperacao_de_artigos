# Sistema_de_recuperacao_de_artigos
This repository contains the code developed during the third semester of the Control and Automation Engineering course, with the objective of retrieving, storing and managing scientific articles using the arXiv API. The project focuses on exploring the integration between API technology and the use of databases.

Features:
Search for Scientific Articles: Automatically searches the arXiv API based on keywords, authors or categories, returning a list of relevant articles.

Storage in Own Database: The code uses a custom database to store article metadata (such as title, authors, publication date and abstract) in a structured manner.

Custom Login System: The project includes a login and authentication system, allowing users to create accounts and manage their own queries and lists of retrieved articles.
Periodic Update: The system is able to periodically update the database to include new articles based on queries already performed.


Technologies Used:
Python: Programming language used.

arxiv-python: Library used to communicate with the arXiv API.

SQLite, ChromaDB: Database for storing articles, with the choice being configurable by the user.
PyQt: For creating interfaces, to improve the aesthetics of the project.

The system also includes password recovery via email and address search by zip code for user registration.
