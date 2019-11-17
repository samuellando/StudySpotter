This is the api source.

There are two types of GET calls:

- For all locations: api.studyspotter.ca?key=<key>
    - Returns JSON in the format:
```
{
    "locations":[
        {
            "id":"concordialibrary",
            "lat":"45.49687",
            "lng":"-73.57811",
            "name":"Concordia Webster Library",
            "density":"57"
        },
        ...
    ]
}
```

- For a specific location: api.studyspotter.cs?key=<key>&location=...
    - Returns JSON in the format:
```
{
    "id":"concordialibrary",
    "name":"Concordia Webster Library",
    "dsc":"Largest library on campus.",
    "labels":{
        "First floor":{
            "data":[57,149,51,136,72,107,62,75,69,100,102,131,128,124,65,81,122,120,76,70,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            "avg":["111","111","111","111","111","111","111","111","111","111","111","111","111","111","111","111","111","111","111","111","111","111","111","111","111","111","111","111","111","111","111","111","111","111","111","111","111","111","111","111","111","111","111","111","111","111","111","111" ]
        }
        ...
```