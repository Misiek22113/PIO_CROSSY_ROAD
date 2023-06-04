# PIO_CROSSY_ROAD

**Tytuł:** Pass the exam.

**Liczba graczy:** 3

**Info:** Gra typu Crossy road (https://en.wikipedia.org/wiki/Crossy_Road), jednak w 2D.

**Przebieg gry:** Gracze zaczynają od startu po lewej stronie ekranu i kierują się w prawą stronę – w stronę mety. Po drodze muszą unikać różnych przeszkód, część z nich powoduje automatyczną przegraną. Gracze kolidują ze sobą, tj. nie mogą na siebie wchodzić, przez co mogą sobie przeszkadzać. Gra kończy się w momencie, kiedy pierwszy gracz dotrze na metę.

**Warunek zwycięstwa:** Gracz jako pierwszy dociera do mety. 

**Warunek przegranej:** Gracz wchodzi w kolizje z przeszkodą, która powoduje automatyczną przegraną lub nie dotarcie do mety w momencie, kiedy inny gracz do niej dotarł lub pierwszy gracz ma zbyt dużą przewagę względem gracza ostatniego, wtedy ostatni gracz przegrywa.

**Warunek braku zwycięzcy:**  Każdy z graczy przegrał przed dotarciem do mety.

# Środowisko

Do działania potrzebny jest python 3.10.11.

Potrzebne biblioteki można zainstalować poprzez odpalenie cmd w głównym folderze gry i wpisanie komendy:

pip install -r requirements.txt

# Uruchomienie gry

Na początku uruchamiamy server.py. Następnie możemy uruchomić client.py. Żeby gra została uruchomiona, potrzebne są 3 osoby w lobby, dlatego client musi być odpalony 3 razy.

