import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  password = 'mudcakemudcake';
  privateDownloads = false;

  files1 = [
    'Projektplan_Gruppe3_Version0.2.pdf',
    'Projektstrukturplan.pdf',
    'Risikoplanung_Gruppe3_Version 0.1.pdf',
    'Rolleneinteilung_Gruppe3.pdf',
    'Timeline.png',
  ];
  files1p = [
    'Statusbericht1_Gruppe3.pdf',
    'Arbeitspakete,Kapazitäten.xlsx',
    'Zeitaufwandserfassung_Woche1_Gruppe3.xlsx',
  ];


  files2 = [
    'Komponentendiagramm_WrittenRealms.pdf',
    'Recherchebericht_Gruppe3.pdf',
    'UseCase_WrittenRealms_CreateDungeon.pdf',
    'UseCase_WrittenRealms_PlayDungeon.pdf',
    'UseCase_WrittenRealms_Übersicht.pdf',
  ];
  files2p = [
    'Statusbericht2_Gruppe3.pdf',
    'Zeitaufwandserfassung_Woche2_Gruppe3.xlsx',
  ];

  files3 = [
    'Designbeschreibung_MUDCAKE.pdf',
    'Dokumentenvorlage_MUDCAKE.pdf',
    'Glossar_MUDCAKE_Version2.pdf',
    'Lasten_Pflichtenheftvorlage_MUDCAKE.pdf',
    'Lastenheft_MUDCAKE_Version2.pdf',
    'Qualitätssicherungskonzept_MUDCAKE.pdf',
  ];
  files3p = [
    'Statusbericht_Woche3_MUDCAKE.pdf',
    'Aufwandserfassung_Woche3_MUDCAKE.xlsx',
  ];

  files4 = [
    'Glossar_MUDCAKE_Version2.pdf',
    'Pflichtenheft_MUDCAKE_Version1.1.pdf',
  ];
  files4p = [
    'Statusbericht_Woche4_MUDCAKE.pdf',
    'Aufwandserfassung_Woche4_MUDCAKE.xlsx',
  ];

  files5 = [];
  files5p = [
    'Statusbericht_Woche5_MUDCAKE.pdf',
    'Aufwandserfassung_Woche5_MUDCAKE.xlsx',
  ];

  files6 = [
    'Designbeschreibung_MUDCAKE_Version2.pdf',
    'Testkonzept_MUDCAKE_Version1.pdf',
    'Diagramme.zip'
  ];
  files6p = [
    'Statusbericht_6_MUDCAKE.pdf',
    'Aufwandserfassung_6_MUDCAKE.xlsx',
  ];

  files7 = [
    'Storyplanung_MUDCAKE_Version1.xlsx',
  ];
  files7p = [
    'Statusbericht_7_MUDCAKE.pdf',
    'Aufwandserfassung_7_MUDCAKE.xlsx',
  ];

  files8 = [
    'Storyplanung_MUDCAKE_Version1.xlsx',
    'Designbeschreibung_MUDCAKE_Version3.pdf',
    'Testkonzept_MUDCAKE_Version2.pdf'
  ];
  files8p = [
    'Statusbericht_MUDCAKE_Woche8.pdf',
    'Aufwandserfassung_MUDCAKE_Woche8.xlsx',
  ];

  files9 = [
    'Storyplanung_MUDCAKE_Version1.xlsx',
  ];
  files9p = [
    'Statusbericht_MUDCAKE_Woche9.pdf',
    'Aufwandserfassung_MUDCAKE_Woche9.xlsx',
  ];

  files10 = [
    'Storyplanung_MUDCAKE_Version1.xlsx',
    'Designbeschreibung_MUDCAKE_Version3_kommentiert.pdf',
  ];
  files10p = [
    'Statusbericht_MUDCAKE_Woche10.pdf',
    'Aufwandserfassung_MUDCAKE_Woche10.xlsx',
  ];

  constructor() { }

  ngOnInit(): void {
  }

  psw() {
    if (prompt('Enter Password To Download Doc') === this.password) {
      this.privateDownloads = true;
    } else {
      this.privateDownloads = false;
      alert('wrong password');
    }
  }

  download(pfad: string, ordner: string) {
    const d = document.createElement('a');
    d.setAttribute('href', 'assets/' + ordner + '/' + pfad);
    d.setAttribute('download', pfad);
    d.click();
  }

}
