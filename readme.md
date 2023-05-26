# Duomenys
Talpykla dirba su Lietuvos miestų koordinačių duomenimis failais:
- demands.dat - vietų, kuriose egzistuoja klientai, koordinatės
- candidates.dat - vietų indeksai, iš kurių bus renkami nauji objektai.
- competitors.dat - egzistuojančių objektų indeksai, pirma eilutė nusako kiek egzistuoja įmonių ir kiek objektų kiekviena įmonė turi.
Duomenys saugomi data/ kataloge ir yra suskirstyti į kelis galimus testavimo atvejus su skirtingais paklausos taškų skaičiais ir su jais susijusiais objektais. Šie atvejai yra 3:
- case0 - 50 vietų duomenys
- case1 - 12395 vietų duomenys
- case2 - 1000 vietų duomenys
# Aprašytos funkcijos
## Algoritmai
- Paprasta atsitiktinė paieška (Pure Random Search), pavadinta `random`
- Rangavimu grįsta paieška (Ranking-based Discrete Optimisation Algorithm). Pagal potencialių objektų rinkimą skirstomas į 2 tipus:
  - RDOA, objektai renkami tik pagal rangus, pavadintas `rdoa`
  - RDOA-D, objektai renkami pagal rangus ir atstumus, pavadintas `rdoa-d`
- Pilnas perėjimas (Brute force), pavadintas `brute`
## Klientų elgsenos modeliai
- Proporciniai:
  - Pilnai proporcinis - klientai pasiskirsto į visus objektus pagal patrauklumą, `proportional`
  - Dalinai proporcinis - klientai pasisikirto į patraukliausius įmonių objektus, `partiallyProportional`
  - Pareto Huff - klientai pasiskirsto į Pareto optimalius objektus, `paretoProportional`
- Binarinis, visi klientai eina į artimiausią objektą, `binary`
## Uždaviniai
Dirbta su konkurencingos įmonės (CFLP) uždavinio variantais:
- Į firmą įeinančiai įmonei (Entering Firm), jos algoritmai yra kataloge `enteringFirm`
- Besiplečiančiai įmonei (Firm Expansion), kataloge `firmExpansion`
# Naudojimas
## Įrankių diegimas
- Parsisiųsti Python
- Rekomenduojama sukurti virtualią Python aplinką norint reikalingus modulius suinstaliuoti lokaliai programoje. 
  - Virtuali programa sukuriama komanda `python -m venv .venv`
  - Aplinka terminale aktyvuojama komanda:
    - Windows: `.\.venv\Scripts\activate`
    - Unix: `source ./.venv/bin/activate`
- Suinstaliuoti reikalingus modulius, komanda `python -m pip install -r requirements.txt`
## Programos leidimas
- Keli programos paleidimo variantai:
  - Paleisti pagrindinį failą ir parinkti paieškos parametrus per GUI: `python main.py`
  - Paleisti PRS proporciniu modeliu: `python main.py -o binary random`
  - Sugeneruoti algoritmų sprendinius su 50 miestų: `python tests.py algorithmTest --case case0 --algorithms random rdoa rdoa-d --cycles 5 10 20 30  --repeats 100`
  - Nubrėžti sprendinių grafikus:
    - Iš sugeneruotų sprendinių: 
      - Pagal vidutines reikšmes: `python tests.py visualiseAccuracy -f 'output/case0'` 
      - Pagal tikimybes: `python tests.py visualiseProbability -f 'output/case0'`
    - Iš iš anksto sugeneruotų sprendinių:
      - Pagal vidutines reikšmes: `python tests.py visualiseAccuracy -f 'output/generated/average-case2'`
      - Pagal tikimybes: `python tests.py visualiseProbability -f 'output/generated/probability-case2'`
