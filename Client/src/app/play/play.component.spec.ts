import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { MatDialogModule } from '@angular/material/dialog';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { Dungeon } from 'Testfiles/models für Schnittstellen';
import { CreateCharacterComponent } from '../create-character/create-character.component';

import { PlayComponent } from './play.component';

describe('PlayComponent', () => {
  let component: PlayComponent;
  let fixture: ComponentFixture<PlayComponent>;
  const world: Dungeon = {
    dungeonName: "TestDungeon",
    dungeonDescription: "moin",
    races: [
      {
        name: 'newRace',
        description: 'newRaceDescription',
      }
    ],
    classes: [{
      name: 'newClass',
      description: 'newClassDescription',
      equipment: null
    }]
  }

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PlayComponent, CreateCharacterComponent ],
      imports: [
        MatDialogModule,
        BrowserAnimationsModule
      ],
      schemas: [
        CUSTOM_ELEMENTS_SCHEMA
      ],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PlayComponent);
    component = fixture.componentInstance;
    component.world = world;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
