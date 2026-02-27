**FastAPI Weather & News Service**
A FastAPI application that provides:
🌦 Weather information by city
📰 Top news headlines by country
🗞 Daily briefing (Weather + News in parallel)

**Setup Instruction and run the project.**
1.Clone the repository.
2.Create the virtual environment by using -"python -m venv venv" 
3.pip install fastapi uvicorn httpx python-dotenv install dependencies. 
4.Mention the API_KEY in .env file.
5.Start the fastapi server:uvicorn main:app --reload
6.Open swagger UI to check the API's working:http://127.0.0.1:8000/docs

**API Endpoints**
1. Weather API endpoint-http://127.0.0.1:8000/weather/{city}
2. News API endpoint-http://127.0.0.1:8000/news
3. Daily Briefing API endpoint-http://127.0.0.1:8000/briefing/city

**Example Request**
1.To get the weather detail,we need to put the city detail in parameter like-Delhi 
and will get the response {"city":Delhi,temperature":29.9,"condition":Cloudy}
2.To get the top 5 news we need to put the country detail in params country:in
then we will get the response of top 5 news 
3.To get the Daily Briefing we have to give city in Parameter then will get the response of Weather and News both.