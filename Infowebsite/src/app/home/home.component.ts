import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  password = 'mudcakemudcake';

  files1 = [
    'Projektplan_Gruppe3_Version0.2.pdf',
    'Projektstrukturplan.pdf',
    'Risikoplanung_Gruppe3_Version 0.1.pdf',
    'Rolleneinteilung_Gruppe3.pdf',
    'Statusbericht1_Gruppe3.pdf',
    'Arbeitspakete,Kapazitäten.xlsx',
    'Zeitaufwandserfassung_Woche1_Gruppe3.xlsx',
    'Timeline.png'
  ];

  files2 = [
    'Komponentendiagramm_WrittenRealms.pdf',
    'Recherchebericht_Gruppe3.pdf',
    'Statusbericht2_Gruppe3.pdf',
    'UseCase_WrittenRealms_CreateDungeon.pdf',
    'UseCase_WrittenRealms_PlayDungeon.pdf',
    'UseCase_WrittenRealms_Übersicht.pdf',
    'Zeitaufwandserfassung_Woche2_Gruppe3.xlsx',
  ];

  files3 = [
    'Designbeschreibung_MUDCAKE.pdf',
    'Dokumentenvorlage_MUDCAKE.pdf',
    'Glossar_MUDCAKE_Version2.pdf',
    'Lasten_Pflichtenheftvorlage_MUDCAKE.pdf',
    'Lastenheft_MUDCAKE_Version2.pdf',
    'Qualitätssicherungskonzept_MUDCAKE.pdf',
    'Statusbericht_Woche3_MUDCAKE.pdf',
    'Aufwandserfassung_Woche3_MUDCAKE.xlsx',
  ];

  files4 = [
    'Statusbericht_Woche4_MUDCAKE.pdf',
    'Glossar_MUDCAKE_Version2.pdf',
    'Pflichtenheft_MUDCAKE_Version1.1.pdf',
    'Aufwandserfassung_Woche4_MUDCAKE.xlsx',
  ];

  constructor() { }

  ngOnInit(): void {
  }

  psw(pfad: string, ordner: string) {
    if (prompt('Enter Password To Download Doc') === this.password) {
      const d = document.createElement('a');
      d.setAttribute('href', 'assets/' + ordner + '/' + pfad);
      d.setAttribute('download', pfad);
      d.click();
    } else {
      alert('wrong password');
    }
  }

}
