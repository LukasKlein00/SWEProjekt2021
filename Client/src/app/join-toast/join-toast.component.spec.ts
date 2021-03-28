import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { JoinToastComponent } from './join-toast.component';

describe('JoinToastComponent', () => {
  let component: JoinToastComponent;
  let fixture: ComponentFixture<JoinToastComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ JoinToastComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(JoinToastComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
