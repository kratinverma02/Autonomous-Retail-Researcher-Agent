🚀 Autonomous Retail Researcher Agent 
An advanced LLM-powered autonomous research system designed for the Retail industry.
The Autonomous Retail Researcher Agent is an AI-driven system that:   
-Accepts natural language retail queries  
-Conducts autonomous web research  
-Synthesizes insights from multiple reliable sources  
-Generates structured executive-level reports   
-Stores research history for future retrieval   
It transforms traditional manual retail research into a scalable AI-powered workflow.  

⚙️ Technology Stack :-

| Category     | Tools Used                   |
| ------------ | ---------------------------- |
| Language     | Python                       |
| AI Framework | LangChain, CrewAI            |
| LLM          | Gemini (or compatible model) |
| Backend      | FastAPI, Uvicorn             |
| Frontend     | Streamlit                    |
| Database     | MongoDB                      |
| Libraries    | Requests, Pandas             |


🚀 8. Installation & Setup  
  Step 1: Clone Repository
  git clone https://github.com/kratinverma02/Autonomous-Retail-Researcher-Agent.git  
  cd autonomous-retail-researcher-agent

  Step 2: Create Virtual Environment  
  python -m venv venv  
  source venv/bin/activate     # Mac/Linux  
  venv\Scripts\activate        # Windows  

  Step 3: Install Dependencies  
  pip install -r requirements.txt  

  Step 4: Configure Environment Variables
  -Create .env file: 
  GEMINI_API_KEY=your_api_key   
  TAVILY_API_KEY=your_api_key  
  MONGO_URI=your_mongodb_uri  

  Step 5: Run Backend  
  uvicorn app.main:app --reload  

  Step 6: Run Frontend  
  streamlit run frontend/streamlit_app.py  
