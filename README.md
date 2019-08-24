# News_App
A news website with article summaries filterable by source, topic, and age.

![Homepage](https://i.imgur.com/kWr0s5v.png)

# Libaries/APIs
Articles are fetched with News API (https://newsapi.org/docs), summarized with sumy (https://pypi.org/project/sumy/), and stored 
in a sqlite database.

Backend utilizes Node.js, client-server communication via socket.io (https://socket.io/docs/), and the frontend in React with 
Blueprint.js (https://blueprintjs.com/docs/) for styling. 

Articles are served to clients when requested and during state changes such as source/topic filtering.

