# tweakstream

Stream topics from [gathering.tweakers.net](https://gathering.tweakers.net) in your terminal.

## Install
Note: `tweakstream` requires Python >= 3.6.
```
pip install tweakstream
```

## Usage

### List active topics
```
$ tweakstream list

   #  Titel                                                         Laatste reactie
---  ------------------------------------------------------------  -----------------
  1  Lucht/Water warmtepomp om mee te verwarmen en koelen #6       19:50
  2  Het Hardstyle-topic - deel 2                                  19:50
  3  Panasonic Monoblock [H versie ] ervaringen - settings - help  19:50
  4  [Slowchat] Het grote cryptocurrency slowchat topic #5         19:50
  5  Is de LG 49" 49SK7 een goeie televisie?                       19:49
  6  Welke wielmoeren voor stalen velgen?                          19:49
  7  [Google Assistent] Ervaringen & Discussie                     19:49
  8  Het grote Ford topic                                          19:49
  9  [Verzamel] Long exposure fotografie (ND... filters)           19:48
 10  De gasdiscussie : wanneer stap jij van het gas af?            19:48
```

### Stream a specific topic
```
$ tweakstream stream https://gathering.tweakers.net/forum/list_messages/1852751
19:46 burnebie https://gathering.tweakers.net/forum/list_message/56741767#56741767
Je weet het allemaal nogal 

19:50 freestyler2 https://gathering.tweakers.net/forum/list_message/56741793#56741793
Graag wil ik iedereen erop wijzen dat er een Masternodes topic is. Discussies hieromtrent graag hier bespreken:
freestyler2 in "[Masternodes] Het grote Masternodes topic deel 1" 

19:51 Jaapio https://gathering.tweakers.net/forum/list_message/56741815#56741815
Bartvandelaar schreef op donderdag 11 oktober 2018 @ 19:24:
[...]


Ik moet toch altijd smakelijk lachen om jou reacties. Voor dat we beide miljonair zijn gaan wij nog eens samen een biertje doen in de kroeg. Een avondje hard lachen.
Dat moet een keertje goed komen. En dan tegen random mensen aan de bar zeggen: 'tis toch wat met die shitcoins, dikke pump en dumps man. Hopen dat de uitbraak van de triangle gigantisch naar boven is, anders geen lambo dit jaar ben ik bang...' en weglopen.

Altijd leuk. 
```

### Search for topics
```
$ tweakstream search "F1"

   #  Titel                                                Laatste reactie
---  ---------------------------------------------------  -----------------
  1  [Pocophone F1] Levertijden & Prijzen                 19:43
  2  [F1] Seizoen 2018 - deel 2                           19:48
  3  [F1 2018] Race 17 - GP van Japan                     09-10
  4  [Multi] F1 2018                                      09:45
  5  [PC] F1 2018 race buddies                            01-09
  6  [Pocophone F1] Accessiores                           30-09
  7  Oneplus 6T vs Pocophone F1                           02-10
  8  [F1] Racemanagers/pools 2017                         13-02
  9  Koppeling f1 2017                                    09-03
 10  [Xiaomi Pocophone F1] Stock Android installeren      25-09
 
Choose a topic to stream (1-10): 
```