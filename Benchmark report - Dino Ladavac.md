# Benchmark report
### Autor: Dino Ladavac
### Mentori: dr. sc. Rok Piltaver i mag. inf. Tomislav Slaviček-Car


<hr>

# Opis ideje 

U ovom eksperimentalnom radu prikazana je i opisana arhitektura web aplikacije koja koristi balanser opterećenja (load-balancer) za potrebe skaliranja. Balanser opterećenja je servis između klijenta i web servera koji omogućuje raspodijelu većeg broja zahtjeva (opterećenja) na više replika servera. Za potrebe rada mjeriti će se vrijeme odaziva sa 2 , 5 i 15 replika web poslužitelja iza balansera opterećenja. Ukoliko web server nebi koristio balanser-opterećenja, svi zahtjevi bi se izvodili nad istim web poslužiteljom što kod aplikacija u stvarnom vremenu dovodi do velikog opterećenja i dugog odaziva jer web poslužitelj može izvesti samo jedan zahtjev istovremeno. Dodavanjem balansera opterećenja u arhitekturu postiže se (how and why):

### - Poboljšanje performansi

Jednako raspoređivanje opterećenja nad više poslužitelja omogućuje sveopće bolje performanse web sustava jer se web sustav prekomjerno ne opterećuje.

### - Bolju dostupnost usluge
U slučaju pada rada jednog od web poslužitelja (u ovom slučaju jedne replike), ostali sustavi pokrivaju njegov rad da ga korisnik može nesmetano koristiti.

### - Horizontalna skalabilnost
Dodavanje više poslužitelja nakon balansera opterećenja omogućuje ubrzanje rada sustava čak i kod velikih porasta opterećenja.

# Prikaz arhitekture 


![load2](https://hackmd.io/_uploads/BJfY-QIvp.png)

*Arhitektura sustava sa 2 web poslužitelja nakon balansera opterećenja*

![load5](https://hackmd.io/_uploads/Bk-P7QIvT.png)

*Arhitektura sustava sa 5 web poslužitelja nakon balansera opterećenja*

<br>

***Zbog jednostavnosti arhitektura sustava sa 15 web poslužitelja neće biti grafički prikazana***

Web aplikacija stvorena je u Django okviru koj sam vodi računa o stvaranju Web poslužitelja i baze podataka (po *defaultu* dolazi SQLite, ali je moguće promjeniti vrstu baze podataka).

U ovom projektu stvorena je web aplikacija za evidenciju knjiga u knjižnici. U web aplikaciji moguće je izlistati sve knjige na stanju te sve knjige od određenog autora ili određenog izdavača. Na stranici /add_book/ moguće je putem formi unijeti detalje o novoj knjizi koja se zatim dodaje u bazu podataka.

Za balanser opterećenja koristi se servis *nginx* koji se konfigurira pomoću datoteke *nginx.conf*.

Poslužitelj se pokreće putem *docker*-a, a balanser opterećenja i kontenjeri web poslužitelja definirani su u datoteci *docker-compose.yml*. 

U repozitoriju na GitHub-u su za svaki od 3 slučajeva testiranja (sa 2, 5  i 15 web poslužitelja) priložene odgovarajuće konfiguracijske datoteke (*nginx.conf* i *docker-compose.yml*).

# Simulacija Podataka

Za simulaciju opterećenja kao i mjerenje performasni koristi se Apache Benchmark te se provode testovi nad velikim brojem zahtjeva. U ovom projektu simulirano je 2000 i 20000 POST zahtjeva na stranicu /add_book/ te se forme popunjuju sa sadržajem koji se nalazi u datoteci *post-data.txt*. Uz to postavljen je broj konkurentnih zahtjeva na 10 kako bi se testirao rad aplikacije sa čim večim opterećenjem.

Odabran je ovoliko veliki broj zahtjeva kako bi rezultati mjerenja bili što preciziniji, različitiji te vrijeme za usporedbu bilo čim duže da se izbjegne uspoređivanje desetog djela milisekunde odnosno da se usporedba vrši nad većim mjernim jedinicima poput sekunda.

Za potrebu izrade aplikacije simulirani su i podaci koji se spremaju u bazu podataka. Za to je korišten *faker* te su podaci za simulaciju definirani u datoteci *factory.py*  prema modelima zadanim u *models.py*.


# Mjerenje vremena odaziva

Kao što je već spomenuto, za mjerenje vremena odaziva koristio se Apache Benchmark sljedećom naredbom:

```bash
ab -n 20000 -c 10 -k -r -l -p post-data.txt http://127.0.0.1:8080/add_book/
```

Sa parametrima *-n 20000* specificira se broj zahtjeva na testu. Ovdje je ostavljeno 20000 zahtjeva iako se za vrijeme testiranja koristi i 2000 zahtjeva.

Parametrima *-c 10* definira se broj zahtjeva koji će se izvesti istovremeno. Ovdje je dedfinirano 10 konkurentnih zahtjeva.

Parametar *-k* poziva *KeepAlive* funkciju koja omogućuje više zahtjeva da se izvede nad istom HTTP vezom.

*-r* parametar se koristi zbog bržeg testiranja. Ovim se omogućuje da se svi problemi nastali prilikom pokretanja naredbe ignoriraju, odnosno da se *ab* naredba nastavi izvodit bez prekida.


Parametrom *-l* definira se učitavanje HTML dokumenta bez slika iako možda stranica sadrži slike.

Podatke koje šaljemo na stranicu unosimo u *post-data.txt* datoteku te ih šaljemo POST zahtjevom što specificiramo *-p post-data.txt* parametrom.

Na kraju je potrebno specificirati URL web servera na koji šaljemo podatke.

Ova naredba vraća detaljni prikaz mjerenja vršenim nad naređenim testovima.


# Rezultati i usporedba podataka

Pošto na poslužitelju bez balansera opterećenja ne može konkurirati više zahtjeva, usporedit će se podaci za 2, 5 i 15 web poslužitelja.

Nakon 2000 zahtjeva sa 10 konkurentnih zahtjeva, dobiveni su sljedeći podaci:

**Balanser opterećenja sa 2 web poslužitelja:**

- Srednja vrijednost vremena odziva: 299.687 ms
- 98-mi percentil: 748 ms
- Zahtjevi po sekundi: 33.37

**Balanser opterećenja sa 5 web poslužitelja:**

- Srednja vrijednost vremena odziva: 140.732 ms
- 98-mi percentil: 660 ms
- Zahtjevi po sekundi: 71.06


**Balanser opterećenja sa 15 web poslužitelja:**

- Srednja vrijednost vremena odziva: 117.619 ms
- 98-mi percentil: 246 ms
- Zahtjevi po sekundi: 85.02

<br>

Nakon 20000 zahtjeva sa 10 konkurentnih zahtjeva, dobiveni su sljedeći podaci:

**Balanser opterećenja sa 2 web poslužitelja:**
- Srednja vrijednost vremena odziva:  297.409ms
- 98-i percentil vremena odaziva: 644ms
- Zahtjevi po sekundi: 33.62

**Balanser opterećenja sa 5 web poslužitelja:**
- Srednja vrijednost vremena odziva: 174.147ms
- 98-i percentil vremena odaziva:  512ms
- Zahtjevi po sekundi: 57.42

**Balanser opterećenja sa 15 web poslužitelja:**
- Srednja vrijednost vremena odziva: 149.430ms
- 98-i percentil vremena odaziva:  259ms
- Zahtjevi po sekundi: 66.92

Primjećuje se da se srednja vrijednost smanjuje kako se povećuje broj web-poslužitelja. Time se dokazuje da se dodavanjem više web poslužitelja iza balansera opterećenja, uspije kvalitetno jednako rasporedit opterećenje na web poslužitelje te se stoga samo vrijeme smanjuje.

<br>


![image](https://hackmd.io/_uploads/BJoZrULwT.png)


*Grafikon odnosa srednje vrijednosti vremena odziva po zahtjevu i broja web poslužitelja*


<br>


![image](https://hackmd.io/_uploads/SkmRUL8PT.png)



*Grafikon odnosa 98-mog percentila vremena odziva po zahtjevu i broja web poslužitelja*


<br>

![image](https://hackmd.io/_uploads/rkljDI8DT.png)

*Grafikon odnosa 98-mog percentila vremena odziva po zahtjevu i broja web poslužitelja*


<br>

Na isti se način smanjuje i srednja vrijednost  vremena odaziva kao i 98-mi percentil, no valja napomenuti kako je skok između srednjih vrijednosti puno manji od skok između percentila. Srednje vrijednosti nisu dobro mjerilo stoga se primarno uvjek promatraju percentili.


