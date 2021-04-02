import { Injectable } from '@angular/core';
import { Class, Race } from 'Testfiles/models für Schnittstellen';

@Injectable({
  providedIn: 'root'
})
export class DungeonService {


  constructor() { }

  createNewClass(): Class {
    const x: Class = {
      name: 'newClass',
      description: 'newClassDescription',
      equipment: null
    }
    return x
  }

  createNewRace(): Race {
    const x: Race = {
      name: 'newRace',
      description: 'newRaceDescription',
    }
    return x
  }
}
