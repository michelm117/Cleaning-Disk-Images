# Cleaning-Disk-Images

**Ziel:** Personenbezogene Daten überschreiben, sodass gesehen werden kann, um welche Information es sich handelt, ohne aber den tatsächlichen Inhalt preiszugeben.
Beispiele:
- hans@gmail.com -> xxxxxxxx@xxxxx.xxx
- meinSicheresPasswort123 -> xxxxxxxxxxxxxx
- 0352687545231 -> 0352xxxxxxxxx

Daten die mir einfach erscheinen zu finden (Alles was man mit Hilfe von  Regex suchen kann):
- Telefonnummer
- Kreditkartennummer
- Emailadressen
- Passwörter (Wenn in einer "Passwortdatei")
- ssh, gpg Keys

Erst einmal beschränke ich mich auf die Zeichenketten, die sich nicht in bereits gelöschten Dateien oder unallocated sind! Im zweiten Schritt würde ich mich dann daran machen, gelöschte Dateien zu manipulieren. Da muss ich mich aber noch genauer einlesen.


### Meine Vorgehensweise:
1. Mittels [strings](https://linux.die.net/man/1/strings) laufe ich einmal über das komplette Image und lasse mir alle Zeichenketten herausgeben. Diese untersuche ich dann mit *grep*. Strings gibt mir leider nur den Offset in byte des Treffers (Match) auf dem gesamten Image zurück. Ich muss also noch herausfinden wo sich die Datei im Image befindet. Folgendes Beispiel findet alle Zeichenketten in denen die Wörter Passwort, Password oder Passwörter drin steht.
    ```bash
    $ strings -t d bachelor_os.img | grep -iE '(passwor[d|t]|passwörter)'
    1440216870 _ZN9ucbhelper31InteractionSupplyAuthentication19setRememberPasswordEN3com3sun4star3ucb22RememberAuthenticationE
    1592532992 password_dump:
    1782769015 file:///home/michelm/Downloads/passwortliste.pdf
    1783305614 passwortliste.xlsx
    1578654795 PASSWORT-LISTE Thema Benutzername Eingerichtet am Bemerkungen Internetadresse/Software Soziale Medien Software https://facebook.de https://outlook.de https://twitter.de https://instagram.de Office Kennwort/Serienummer Max2017 Max2016 Max!2016 - myPasswordxkwe ) + $234!agmB:
    ```

    Für das Beispiel habe ich mir folgende Zeile ausgesucht:
    ```bash
    1592532992 password_dump:
    ```
    Das Script muss nachher natürlich zwischen Binärdateien, Officedateien, Text, Pdf und anderen Dateitypen unterscheiden. Ich denke Binärdateien können vernachlässigt werden, da *normale* User da vermutlich eher keine Spuren hinterlassen.


2. Als nächstes müssen wir herausfinden in welcher Partition sich der gefundene Offset befindet. Dafür wird *mmls* verwendet:
    ```bash
    $ mmls bachelor_os.img
    DOS Partition Table
    Offset Sector: 0
    Units are in 512-byte sectors

          Slot      Start        End          Length       Description
    000:  Meta      0000000000   0000000000   0000000001   Primary Table (#0)
    001:  -------   0000000000   0000002047   0000002048   Unallocated
    002:  000:000   0000002048   0001050623   0001048576   Win95 FAT32 (0x0b)
    003:  -------   0001050624   0001052671   0000002048   Unallocated
    004:  Meta      0001052670   0025163775   0024111106   DOS Extended (0x05)
    005:  Meta      0001052670   0001052670   0000000001   Extended Table (#1)
    006:  001:000   0001052672   0025163775   0024111104   Linux (0x83)
    007:  -------   0025163776   0025165823   0000002048   Unallocated
    ```
    Da das Script nicht auf Anhieb wissen kann, dass in diesem Fall sich die Datei nur in der Linux Partition befinden kann, muss dies berechnet werden. Da *strings* einem den Offset des Matches auf dem gesamten Images zurück gibt, müssen wir den Offset auf dem Dateisystem berechnen. Ist dieser größer als die Länge der Partition, kann sich der Match nicht auf dieser befinden. Hier nur ein paar Beispiele, das Script würde es dann für jedes Dateisystem machen:
    - **W95 FAT32**:
      - 2048 * 512 = 1048576
      - 1592532992 - 1048576 = 1591484416
      - 1591484416 > 1048576
    - **Extended Table**:
      - 1052670 * 512 = 538967040
      - 1592532992 - 538967040 = 1053565952
      - 1053565952 > 1

    Da die Tests alle fehlschlagen, muss der Match sich in dem letzem Dateisystem **Linux (0x83)** befinden. Dieses fängt  ab Sector 1052672 an.


3. Um die passende Datei zu identifizieren brauchen wir als nächstes den *block offset*. Um diesen zu finden brauchen wir den Start des Linux Dateisystems 1052672 und das Programm *fsstat*:
    ```bash
    $ fsstat -o 1052672 bachelor_os.img | grep "Block Size:"
    Block Size: 4096
    ```
    Die Block Size beträgt 4096 bytes.

4. Für den nächsten Schritt brauchen wir den Offset des Matches auf der Linux Partition.
    - Linux (0x83):
      - 1052672 * 512 = 538968064
      - 1592532992 - 538968064 = **1053564928**


5. Um die Anzahl der Blöcke zu erhalten müssen wir jetzt den gerade errechneten Partitions Offset durch die Block Size teilen: 1053564928 / 4096 = **257218**


6. Die gesamte Berechnung sieht dann wie folgt aus:
    ```bash
    (match_offset - (sektor_start_des_filesystems * 512)) / block_size = file_system_block
    (1592532992 - (1052672 * 512)) / 4096 = 257218
    ```
    und liest sich wie folgt: Der Offset des Matches auf dem Disk (1592532992) wird mit dem Start Offset des Dateisystems (1052672 * 512) substraiert. Das Resultat wird dann mit der Block Size (4096) dividiert. Der gesuchte Dateisystem block ist 257218.


7. Mit Hilfe von *blkstat* kann man jetzt noch überprüfen ob der Block Allocated ist:
   ```bash
   $ blkstat -o 1052672 bachelor_os.img 253829
   Fragment: 253829
   Allocated
   Group: 7
   ```


8. Mittels *ifind*  kann man sich nun noch den Inode / meta-data structure entry (MFT entry) ausgeben lassen.
   ```bash
   $ ifind -f ext -o 1052672 -d 257218 bachelor_os.img
   397692
   ```


9. Mittels *icat* kann ich mir jetzt den Inhalt der Datei mit dem gefundenen Inode ausgeben lassen:
    ```bash
    $ icat -o 1052672 bachelor_os.img 397692
    password_dump:
    1234
    123@abc
    sir786
    vsc1601
    k4njut
    b1r2n3u4r5
    belingaro123456
    123expo123
    jan90020
    Qwerty12345
    qwerty1
    tongea3672
    ConnorM1522
    gabriel160594
    asdfgh14
    987654q
    ```


10. Wenn man den Output von *icat* in *file* rein piped, dann bekommt man den Datentype gesagt:
    ```bash
    $ icat -o 1052672 bachelor_os.img 397692 | file -
    /dev/stdin: ASCII text
    ```


11. Mit Hilfe von *fls* kann man sich allozierte und gelöschte Dateien rekursiv anzeigen lassen. Mit grep filtere ich mir dann unseren gefundenen Inode heraus.
    ```bash
    $ fls -o 1052672 bachelor_os.img -rF | grep 397692
    r/r 397692:	home/michelm/Documents/passwords.md
    ```


### Fazit
Jetzt wissen wir wo die Datei sich im Image befindet. Wir könnten das Image jetzt mounten und bearbeiten. Ich habe mir ein Script geschrieben um etwas mit dieser Vorgehensweise zu experimentieren. Ich packe es mal in den Anhang, glaube aber nicht, das es von nützen sein wird, da der Dateisystem Sektor noch hard-coded ist. Hier einmal der Output des Scripts als Beispiel. Die gewählte Eingabe wird im nächsten Abschnitt erklärt:
```bash
$ ./scan.sh -i=bachelor_os.img -r="Max2017"
Collecting offsets from 'bachelor_os.img' for 'Max2017' using grep

Collecting informations from offsets:
-------------------------------------

Offset:    1578454566
Block:     253780
Status:    Allocated
Inode:     434078
File Type: SQLite 3.x database
File Path: home/michelm/.cache/tracker/meta.db

Offset:    1578655517
Block:     253829
Status:    Allocated
Inode:     434078
File Type: SQLite 3.x database
File Path: home/michelm/.cache/tracker/meta.db

Offset:    1782615838
Block:     303624
Status:    Allocated
Inode:     434081
File Type: SQLite Write-Ahead Log
File Path: home/michelm/.cache/tracker/meta.db-wal
```


### Probleme
* Ich habe mehrere Dateien auf dem Image erstellt und versucht diese mit Hilfe meines Scripts zu finden (alle beinhalten die Zeichenkette *Max2017*). Nur die Textdatei im obigen Beispiel konnte ich finden. Pdfs, Excel- & Worddateien findet das Script nicht. Das Problem liegt an *strings* und *grep*. Diese können diese Dateien leider nicht richtig durchsuchen, eine Alternative habe ich aber noch nicht gefunden.
* Des Weiteren ist mir aufgefallen, dass zB Gnome Dateien durchsucht und diese in einer Datenbank speichert, um diese schneller bei einer Suche zu finden. Also müsste man auch Datenbankdateien bearbeiten. Dafür habe ich leider auch noch kein Programm gefunden, das dies einfach so machen kann.
* Ich habe versucht mit Hilfe eines Scripts Pdf-Dateien zu bearbeiten. Ist da zB eine Email Adresse drin, müsste man diese ja überschreiben. Leider klappen die gefundenen Lösungen nur in weniger als der Hälfte der Versuche. Hierzu habe ich folgenden [Link](https://askubuntu.com/questions/1100970/command-line-tool-to-search-and-replace-text-on-a-pdf/1104538#1104538) gefunden. Wenn ich das also richtig verstehe, kann man PDFs nicht wirklich ändern. Soll ich Pdfdateien dann einfach ignorieren? Das wäre aber eigentlich ein grosser Rückschritt, da gerade in solchen Dateien sich oft Personenbezogene Daten befinden.

### Source:
Das sind die Ressourcen die ich am meisten genutzt habe.
- [The Sleuth Kit](http://wiki.sleuthkit.org/index.php?title=FS_Analysis)
- [Disk-Forensik/ Beweismittelanalyse/ SleuthKit](https://de.wikibooks.org/wiki/Disk-Forensik/_Beweismittelanalyse/_SleuthKit)
- [The Law Enforcement and Forensic Examiner's Introduction to Linux](https://linuxleo.com/Docs/LinuxLeo_4.95.1.pdf)
- [Device vs Partition vs File System vs Volume](https://stackoverflow.com/questions/24429949/device-vs-partition-vs-file-system-vs-volume-how-do-these-concepts-relate-to-ea)
