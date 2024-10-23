# Pararius huurwoning scraper

Dit project is een web scraper die huurwoningadvertenties verzamelt van de [Pararius](https://www.pararius.com/apartments/nederland) website, een van de grootste platforms voor huurwoningen in Nederland. De scraper haalt gegevens op zoals huurprijs, locatie, oppervlakte (in vierkante meters), aantal kamers, interieur en extra functies zoals balkon, tuin, energielabel, en meer.

## Vereisten

Voor het web scrapen zijn Python 3.x and Chrome Webdriver (beheerd met `webdriver_manager`) nodig. De volgende Python-pakketten zijn nodig:
- `selenium_wire`
- `webdriver_manager`
- `pandas` (voor de analyse)
- `time`

Je kunt de vereiste pakketten installeren met `pip`:

```bash
pip install -r requirements.txt
```

## Installatie

1. Clone de repository of download de projectbestanden.
2. Zorg ervoor dat je Chrome WebDriver hebt geïnstalleerd. De `webdriver_manager` handelt de installatie automatisch af wanneer je de scraper uitvoert.
3. Zorg ervoor dat de volgende mappenstructuur aanwezig is in je project:

├── driver/

├── data/

└── main.py

4. De map `data/` wordt gebruikt om de gescrapete links en woningadvertenties op te slaan.

## Gebruik

Het toegangspunt voor het uitvoeren van de scraper is via `main.py`, waar het web scraper proces wordt gestart en wordt opgeslagen. 

1. **Voer de scraper uit**

    Open een terminal in de projectdirectory en voer het volgende uit:

   ```bash
   python main.py
   ```

   - Dit verzamelt alle huurwoninglinks van Pararius. Vervolgens bezoekt het elke link en haalt het details op, die worden opgeslagen in `data/pararius_listings.csv`.

2. **Data verzamelen**

   De scraper verzamelt de volgende gegevens van elke huuradvertentie voor de CSV:
   
   - **Link**: URL van de woningadvertentie.
   - **Huurprijs**: De huurprijs.
   - **Locatie**: Postcode en buurt.
   - **m²**: Oppervlakte van de woning in vierkante meters.
   - **Kamers**: Aantal kamers.
   - **Interieur**: Kaal, gestoffeerd of gemeubileerd.
   - **Huurovereenkomst**: Duur van de huurovereenkomst.
   - **Type woning**: Appartement, vrijstaande woning, enzovoorts.
   - **Bouwjaar**: Bouwjaar van de woning.
   - **Badkamers**: Aantal badkamers.
   - **Faciliteiten**: Aanwezige faciliteiten in de woning.
   - **Balkon**: Aanwezigheid van een balkon.
   - **Tuin**: Aanwezigheid van een tuin.
   - **Omschrijving tuin**: Voortuin, achteruin, enzovoorts.
   - **Energie label**: Energielabel van de woning.
   - **Opslag**: Soort opslag beschikbaar in de woning.
   - **Parkeren**: Aanwezigheid van parkeerplaatsen.
   - **Type parkeerplaats**: Soort parkeergelegenheden.
   - **Garage**: Aanwezigheid van een garage.
   - **Beschrijving**: Woningbeschrijving.

3. **Analyse**

   In het bestand `analysis.ipynb` wordt het CSV bestand ingeladen, omgezet als DataFrame en vervolgens opgeschoond. Verschillende filters kunnen worden toegepast op de data.

## Verbeteringen

- **Error handling**: Pagina's die niet kunnen worden geladen of resulteren in time-outs beter afhandelen.
- **Parallel verwerking**: Het scrapen kan worden versneld door het parallel uitvoeren van de gegevensverzameling via meerdere threads.
- **Uitbreiden van filters**: Filters toevoegen op basis van stad, prijs, enzovoorts.
