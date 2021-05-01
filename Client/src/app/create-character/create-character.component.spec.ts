import { InteractivityChecker } from '@angular/cdk/a11y';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatDialogModule, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { NgSelectModule } from '@ng-select/ng-select';
import { Dungeon } from 'Testfiles/models für Schnittstellen';

import { CreateCharacterComponent } from './create-character.component';

describe('CreateCharacterComponent', () => {
  let component: CreateCharacterComponent;
  let fixture: ComponentFixture<CreateCharacterComponent>;

  const world: Dungeon = {
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
      imports: [
        FormsModule,
        ReactiveFormsModule,
        NgSelectModule,
        MatDialogModule,
      ],
      declarations: [ CreateCharacterComponent ],
      providers: [
        { provide: MAT_DIALOG_DATA, useValue: world }
    ],
    schemas: [
      CUSTOM_ELEMENTS_SCHEMA
    ],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CreateCharacterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
