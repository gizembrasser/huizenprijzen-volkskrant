# Onderzoek naar huuraanbod Pararius

Dit project is een web scraper die huurwoningadvertenties verzamelt van de [Pararius](https://www.pararius.com/apartments/nederland) website, een van de grootste platforms voor huurwoningen in Nederland. De scraper haalt gegevens op zoals huurprijs, locatie, oppervlakte (in vierkante meters), aantal kamers, interieur en extra functies zoals balkon, tuin, energielabel, en meer. 

Op basis van deze gegevens wordt een analyse gemaakt van de puntentelling van de woningen, op basis van het [woningwaarderingsstelsel](https://www.huurcommissie.nl/huurcommissie-helpt/beleidsboeken_html/waarderingsstelsel-zelfstandige-woonruimte/bijlage-1) (zie kopje 'Analyse').

## Vereisten

Voor het web scrapen zijn Python 3.x and Chrome WebDriver (beheerd met `webdriver_manager`) nodig. De volgende Python-pakketten zijn nodig:
- `selenium_wire`
- `webdriver_manager`
- `pandas` (voor de analyse)
- `time`

Je kunt de vereiste pakketten installeren met `pip`:

```bash
pip install -r requirements.txt
```

*Opmerking: als de Chrome WebDriver niet werkt is het misschien nodig om een [versie te downloaden](https://developer.chrome.com/docs/chromedriver/downloads#chromedriver_1140573590) passend bij jouw versie van Google Chrome. In dat geval moet je het bestand `chromedriver.exe` in de `driver/` folder vervangen met de juiste versie.*

## Installatie

1. Clone de repository of download de projectbestanden.
2. Zorg ervoor dat je Chrome WebDriver hebt geïnstalleerd. De `webdriver_manager` handelt de installatie automatisch af wanneer je de scraper uitvoert.
3. Zorg ervoor dat de volgende mappenstructuur aanwezig is in je project:

├── driver/

├── data/

└── main.py

4. De map `data/` wordt gebruikt om de gescrapete links en woningadvertenties op te slaan.

## Gebruik

Het toegangspunt voor het uitvoeren van de scraper is `main.py`. Via de command line kun je verschillende opdrachten uitvoeren met behulp van de `argparse` configuratie in de code.

### Command-line opties
Er zijn twee beschikbare opdrachten die je via de command line kunt uitvoeren:

1. **Listings verzamelen**  
   Om de links van alle Pararius-huurwoningadvertenties te verzamelen en vervolgens de informatie voor elke woning op te slaan als CSV-bestand, gebruik je het `collect_listings` commando:

   ```bash
   python main.py collect_listings --city --min_price --max_price --csv_file_name
   ```

   - `city`: De stad waarvoor je advertenties wilt verzamelen. De standaardwaarde is 'nederland'.
   - `min_price` en `max_price`: Optionele filters voor de huurprijzen. 
   - `csv_file_name`: De naam voor het CSV bestand waarin je de data wilt opslaan (met extensie).

2. **HTML-bestanden lokaal opslaan**  
   Om de HTML-bestanden van elke woningadvertentie lokaal op te slaan, gebruik je het `save_html` commando. Zorg ervoor dat de CSV een kolom `Link` bevat die naar de advertentielinks verwijst:

   ```bash
   python main.py save_html --csv_file
   ```

   - `csv_file`: Pad naar het CSV-bestand met een `Link`-kolom.

### Analyse

In het bestand `analysis.ipynb` wordt het ruwe CSV bestand ingeladen, omgezet als DataFrame en vervolgens opgeschoond. Verschillende filters worden toegepast op de data om visualisaties te maken.

Voor de analyse wordt van elke huurwoning een schatting gemaakt van de puntentelling op basis van het woningwaarderingstelsel. Het resultaat is een CSV bestand met de volgende kolommen:

- **Link**: URL van de woningadvertentie.
- **Huurprijs**: De huurprijs.
- **Prijs details**: Welke kosten er inbegrepen zijn in de huurprijs (servicekosten, water, gas, enzovoorts).
- **Locatie**: Postcode van de woning.
- **Specificaties**: Overige informatie over de woning (bijvoorbeeld monumentstatus).
- **m²**: Oppervlakte van de woning in vierkante meters.
- **Kamers**: Aantal kamers.
- **Interieur (optioneel)**: Kaal, gestoffeerd of gemeubileerd.
- **Huurovereenkomst**: Duur van het huurcontract.
- **Type woning (optioneel)**: Appartement, vrijstaande woning, enzovoorts.
- **Bouwjaar**: Bouwjaar van de woning.
- **Badkamers**: Aantal badkamers.
- **Faciliteiten**: Aanwezige faciliteiten in de woning (bad, douche, glasvezel, enzovoorts).
- **Balkon**: Aanwezigheid van een balkon.
- **Tuin**: Aanwezigheid van een tuin.
- **Omschrijving tuin (optioneel)**: Voortuin, achteruin, enzovoorts.
- **Energie label**: Energielabel van de woning.
- **Opslag (optioneel)**: Soort opslag beschikbaar in de woning.
- **Parkeren**: Aanwezigheid van parkeerplaatsen.
- **Type parkeerplaats**: Soort parkeergelegenheden.
- **Garage**: Aanwezigheid van een garage.
- **Beschrijving**: Woningbeschrijving.
- **Tuin m²**: Oppervlakte van de tuin, indien beschikbaar.
- **Buurt**: Buurt waarin de woning staat.
- **Stad**: Stad waarin de woning staat.
- **Gemiddelde WOZ**: Gemiddelde WOZ waarde voor de buurt in 2023.
- **Punten oppervlakte**: Aantal punten toegekend voor de oppervlakte (zie 2.1 in `analysis.ipynb`).
- **Punten verwarming**: Aantal punten toegekend voor verwarming van de woning (zie 2.2 in `analysis.ipynb`).
- **Punten sanitair**: Aantal punten toegekend voor sanitair in de woning (zie 2.3 in `analysis.ipynb`).
- **Punten buitenruimten**: Aantal punten toegekend voor buitenruimten van de woning (zie 2.4 in `analysis.ipynb`).
- **Punten energie**: Aantal punten toegekend voor energieprestatie van de woning (zie 2.5 in `analysis.ipynb`).
- **Punten parkeerruimten**: Aantal punten toegekend voor privé parkeerruimten (zie 2.6 in `analysis.ipynb`).
- **Punten keuken**: Aantal punten toegekend voor de keuken (zie 2.7 in `analysis.ipynb`).
- **Punten WOZ**: Aantal punten toegekend voor de WOZ-waarde, berekend zonder enige beperkingen/uitzonderingen (zie 2.8 in `analysis.ipynb`). 
- **COROP**: Geeft aan of de woning zich in een COROP-gebied bevindt, een bouwjaar tussen 2018 - 2022 heeft en een oppervlakte kleiner dan 40 m² heeft.
- **Punten**: Benadering van het totale aantal punten van de woning.
- **Punten WOZ max**: Aantal punten toegekend voor de WOZ-waarde, berekend met de alle beperkingen en uitzonderingen toegepast (zie 2.8 in `analysis.ipynb`).
- **Punten zonder CAP**: Benadering van het totale aantal punten, zonder enige berperkingen/uitzonderingen voor het aantal punten van de WOZ-waarde.