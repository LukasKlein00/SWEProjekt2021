import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CorgiComponent } from './corgi.component';

describe('CorgiComponent', () => {
  let component: CorgiComponent;
  let fixture: ComponentFixture<CorgiComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CorgiComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CorgiComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
