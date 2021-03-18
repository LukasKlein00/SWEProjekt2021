import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  password = 'mudcakemudcake';

  constructor() { }

  ngOnInit(): void {
  }

  psw(pfad: string) {
    if (prompt('Enter Password To Download Doc') === this.password) {
      const d = document.createElement('a');
      d.setAttribute('href', 'assets/' + pfad);
      d.setAttribute('download', pfad);
      d.click();
    } else {
      alert('wrong password');
    }
  }

}
