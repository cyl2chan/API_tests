Phase 1

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


Step 7

1. Change FORECAST to "/v1/forcast". What status comes back? Does the failure message tell you what is wrong?

404. 
AssertionError: assert 404 == 200
AssertionError: Sydney: 404 {"reason":"Not Found","error":true}

2. Change your expected unit to "°F". Does the failure tell you which city failed?

All cities failed. 
AssertionError: assert '°C' == '°F'

3. Run with OPEN_METEO_BASE_URL=https://example.com. What does a "wrong environment" failure look like?
E       AssertionError: Sydney: 404 <!doctype html><html lang=en><head><meta charset=utf-8><link rel=icon href=data:,><meta name=viewport content="width=device-width,initial-scale=1"><title>Example Domain</title><style>html{color-scheme:light dark;background:light-dark(#eee,#222)}body{font:16px/1.6 system-ui,sans-serif;max-width:26em;margin:auto;padding:25vh 2em 2em;text-align:center}</style></head><body><p>This domain is for use in documentation examples without needing permission. This is not a service; avoid relying on it for testing and monitoring purposes.</p><script src=/s.js></script></body></html>
E         
E       assert 404 == 200
E        +  where 404 = <APIResponse url='https://example.com/v1/forecast?latitude=-33.8688&longitude=151.2093&hourly=temperature_2m' status=404 status_text='Not Found'>.status

tests\test_forecast.py:40: AssertionError

FAILED tests/test_forecast.py::test_forecast_success[-33.8688-151.2093-Sydney] - AssertionError: Sydney: 404 <!doctype html><html lang=en><head><meta charset=utf-8><link rel=icon href=data:,><meta ...

4. Question: for each failure, if it happened in CI at 2 a.m., could a teammate understand the problem from the output alone? If not, what would you add to the assert message?
    1. Better to add the URL which is not found
    2. Teammates will understand
    3. Also, better to add URL which is not found


Step 8

1. your Compose tests ran against an API inside your own containers. These run against a public service on the internet. What new reasons could make them fail in CI that have nothing to do with your code?
It works when i entered py -m pytest -s ./tests/test_forecast.py in terminal in local machine.
But same command doesn’t work in Github Actions workflow. Use py -m pytest -s ./tests/test_forecast.py instead. 

That’s becos my Windows computer uses Windows Python launcher, while GitHub Actions setup-python b4 running the tests. 

Other reasons:
Different dependencies 
Service outage, network problems


Phase 2

Step 1

1. Why does temperature_2m allow "null" as well as "number"? The docs don't say whether nulls can appear. Was allowing it the right call? Argue your answer.

It’s a right call, becos it can be null there may not be temperature available yet for reasons. 

2. What can a schema catch that your Phase 1 checks can't? What can your Phase 1 checks catch that a schema can't? (Think about the °C check.)

Schema can catch the data isn’t the correct type. 
Phase 1 can check:
- units, whether length of time and temperature are same, invalid values, correct spelling, range of values of longitude and latitude 


