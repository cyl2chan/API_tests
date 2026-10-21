Step 1: Look at an API call in the browser (no code)

Questions (answer in NOTES.md):
1. Which part of the URL is the base URL, which is the path, and which are the query parameters? 

Base: https://api.open-meteo.com/, 
path: /v1/forecast, 
Query para: latitude=49.25, longitude=-122.85, hourly=temperature_2m, forecast_days=1

2. Which HTTP method did the browser use? GET

3. What status code came back? Find the content-type response header and write down its value. 

Code: 200, (application/json; charset=utf-8 ) Value is 8

4. Describe the shape of the response body. What is the relationship between hourly.time and hourly.temperature_2m? 

They display the temperature of a specific time

Now change latitude=49.25 to latitude=91 and reload.
5. Question: what changed, the status, the body, or both? Copy the body into your notes.

Both.
Status code changed to 400
body:
{"reason":"Latitude must be in range of -90 to 90°. Given: 91.0.","error":true}


Step 2
Question: for your UI tests you had to run playwright install. You won't need it here. Why not? (Hint: does an API call need a browser?)

API call doesn’t need a browser while UI tests need it

Step 3

1. The test takes a playwright argument, but you never created one. Where does it come from? (Hint: it works the same way as page in your UI tests.)

Imported from Playwright package

2. What did each print show? Match each one to what you saw in the browser in Step 1.

print(response.status)
		tests\test_forecast.py 200
print(response.headers["content-type"])
		application/json; charset=utf-8
print(response.json().keys())
dict_keys(['latitude', 'longitude', 'generationtime_ms', 'utc_offset_seconds', 'timezone', 'timezone_abbreviation', 'elevation', 'hourly_units', 'hourly'])
3. What does api.dispose() do, and what would happen if you forgot it? 

Cleans up the session of Playwright uses for sending API requests
If forgotten, resources can remain in memory longer than necessary, and potentially increase memory usage when running many tests. 


Step 4

1. Why is BASE_URL read from an environment variable instead of written into the tests?

If we set up in the system to have a certain URL as the base url, we wanna use that instead of changing the url written. 

2. The code after yield in the fixture: what does it do, and when does it run?

The code after yield cleans up the API Request Context and releases its resources. It runs at the end of pytest session becos the fixture has session scope. 

3. Why scope="session" and not the default scope? Would the default be wrong, or only wasteful?
Scope = “session” reuses API Request across different tests, and reduces repeated setup and clean up. The default isn’t wrong or wasteful. It provides a fresh context for each test, which slows down the tests. 

4. What is **extra for? (You will use it in Phase 2.)
Extra parameters besides the parameters stated inside get_forecast(). 


Step 5

0. For TODO 5, first write the obvious check, assert data["latitude"] == latitude, and run it. It will fail. Before fixing it, read what the docs say the latitude field in the response means, and explain the failure in your notes. Then change the check to allow a tolerance. You choose the tolerance; write down why you chose it.

The decimal places of latitude in the data are inconsistent: three places are 6 dc, one is 1 dc. Also, that doesn’t match the dc in the data of the code. Therefore the test failed. 
It isn’t necessary for weather app to provide temperature with dc. Integers are enough. Questions:

1. For each of your five checks, describe a bug that it would catch but a status check would miss.

Status check: response.text() can display a HTML text that page isn’t available but status code could still be 200
Header: inappropriate content type
Time and temperature_2m same length: when temperature isn’t available yet, it’d only show time, which lead to time length longer than temperature_2m same length
Temperature unit: unit is Fahrenhite instead of degree Celcius 
Latitude: decimal places

2. Why is Sydney in the list? What do Vancouver, Chicago and Tokyo have in common that Sydney doesn't? What would a fifth city have to be to add something new?

Sydney has a negative latitude while others have positive ones. 
A fifth city can be in a different continent, like Africa and South America, to add something new.
