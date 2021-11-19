# Development ideas

## OO design

Det kunne være fedt at have en `Runner`-klasse, der eksekverer to processer hver baseret på abstrakte/interface klasser:  

En `Grabber`, som står for at hente websiderne. Grabberens opgaver er:
* tag links fra en kø, 
* hent indholdet (html, via http)
* overdrag indhold til `Skraberen`

En `Skraber`, som har to hoved opgaver:  
* find _relevante_ links
  * indsæt disse i Grabberens kø,
  * med oplysninger om hvilken `Skraber`, der skal processere
* find _relevante_ data, 
  * og skrab data til en eller anden struktur

Umiddelbart kan man måske bruge en velskrevet generisk `Grabber`, til mange jobs. Mens hver side, måske skal have hver sin `Skraber` måske med nogen hjælpe klasser, hvor de generalle/generiske ting abstraheres ud.
Man kan, lidt generelt sige at alle data, og links, identifiseres ved den kontekst de står i. Så hvis man kan definere konteksten, har man også data... 

Måske kan man en dag bruge Machine Learning til at "opdage" konteksten.

## Links

* <https://kmdvalg.dk/Main/Home/KV> selvfølgelig :-)

* <https://www.google.com/search?channel=fs&client=ubuntu&q=how+to+write+a+web+scraper>
  * <https://www.edureka.co/blog/web-scraping-with-python/>
  * <https://realpython.com/beautiful-soup-web-scraper-python/>
  * <https://hackernoon.com/building-a-web-scraper-from-start-to-finish-bb6b95388184>
  * <https://betterprogramming.pub/the-only-step-by-step-guide-youll-need-to-build-a-web-scraper-with-python-e79066bd895a>
  * <https://webscraper.io/>
  * <https://towardsdatascience.com/how-to-build-a-web-scraper-in-python-c75563ee60b7>
  * <https://oxylabs.io/blog/python-web-scraping>