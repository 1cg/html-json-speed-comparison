# HTML vs JSON Dynamic Generation Speed Comparison

This is a simple project I set up to compare how long it takes flask to render a response in three different
formats:

* A full HTML page
* A partial HTML page
* A JSON response

In all three cases the page is rendering 1000 contacts.  The two HTML responses use 
[Jinja2](https://jinja.palletsprojects.com/en/2.10.x/) templates.  The JSON end point uses the
[dataclass](https://docs.python.org/3/library/dataclasses.html) library to make JSON serialization of the
sole model, `contacts_model.py`, easy.

## Data Setup

The data for this test is stored in `contacts.json` and is loaded at server startup so that responses can
be, as much as possible, purely rendering time.

## Client Side

On the client side we run a tight loop of requests to the same end-point over and over again and record
the time it takes to respond.  Since this is against local host there is very low latency, but the network
connection time is obviously still significant.  In real-world latency environments the results would be
even closer to one another, since latency tends to dominate in most distributed systems.

## Caveats

* This is Flask & Python, other platforms might have different 
* I am not an expert python or flask programmer, this is probably not a great example of python code to follow.
* I intentionally kept things very simple
* I did not do any performance tuning for any of the endpoints
* I may not have chosen the "standard" way to produce JSON, just the easiest
* I am printing the server-side response time which adds CPU to each request

## Results

The results vary of course, but on my machine (Macbook M2) a representative result is as follows:

```
Average Full HTML Time : 4.719ms
Average Partial HTML Time : 4.158ms
Average JSON Time : 4.541ms
```

The full HTML response typically (but not always!) takes the longest, the partial HTML response is usually the
fastest and the JSON response is typically in between the two.

Looking at the logs on the server side, the response time is almost always 0ms (ie undetectably fast), with the occasional spike to 3-6ms.  This
seems likely to be garbage collection time, given its inconsistency.  One theory I have on why JSON serialization might
be a _bit_ slower in some cases is that it often uses reflection, whereas templates are often hard coded.  Also, I would
note that a JSON API often returns all data, regardless of necessity, whereas an HTML API returns the minimum data necessary
for a given UI because, well, it _is_ the UI.

This is speculation, however, and my take-away from all this is not that HTML is faster than JSON: I'm sure with a 
well tuned JSON serialization mechanism it can be made faster than the HTML.  Rather it is that the two approaches are very close 
to one another and are probably round off errors in the overall scheme of total system performance.  Once you hit a data store, or add 
in real-world latency between the client and server, these differences vanish in the wash.

So my opinion continues to be that server-side render performance is not a reason to choose either a JSON-based approach
or a hypermedia/HTML based approach to building your web application.  You should use other criteria for picking between the two.

I try to outline when I think hypermedia is a good choice in my essay ["When To Use Hypermedia"](https://htmx.org/essays/when-to-use-hypermedia/)