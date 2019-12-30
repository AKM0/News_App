# News_App
A news website with article summaries filterable by source, topic, and age.

![Homepage](https://i.imgur.com/kWr0s5v.png)

### Libaries/APIs
Articles are fetched with News API (https://newsapi.org/docs), summarized with sumy (https://pypi.org/project/sumy/), and stored 
in a sqlite database.

Backend utilizes Node.js, client-server communication via socket.io (https://socket.io/docs/), with the frontend in React + 
Blueprint.js (https://blueprintjs.com/docs/). 

Articles are served to clients when requested and during state changes such as source/topic filtering.

### Setup

#### Prerequisites

Node.js and NPM

#### Project packages/dependencies

1. Clone repo
2. Navigate to /backend/server/
3. Install packages (npm install)
4. Navigate to /frontend/
5. Install packages (npm install)
6. Revert babel-loader to babel-loader v8.0.4 (npm install babel-loader@8.0.4)

#### Running

1. Navigate to /backend/server/
2. Start server (node server)
3. Navigate to /frontend/
4. Start client page (npm start)
5. Access at http://localhost:3000/

#### Updating articles

Requires Python3 and News API Token

1. Navigate to /backend/data/
2. Execute data script (python3 backend.py)
3. Copy new main.db to /backend/server/
