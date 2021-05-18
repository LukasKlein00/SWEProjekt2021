import { HttpClientTestingModule } from '@angular/common/http/testing';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed, tick } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { RouterTestingModule } from '@angular/router/testing';
import { SocketIoConfig, SocketIoModule } from 'ngx-socket-io';
import { environment } from 'src/environments/environment';

import { ProfilComponent } from './profil.component';

describe('ProfilComponent', () => {
  let component: ProfilComponent;
  let fixture: ComponentFixture<ProfilComponent>;
  const config: SocketIoConfig = { url: environment.websocketUrl, options: {} };

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ProfilComponent ],
      imports: [
        SocketIoModule.forRoot(config),
        RouterTestingModule,
        HttpClientTestingModule,
      ],
      schemas: [
        CUSTOM_ELEMENTS_SCHEMA
      ],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ProfilComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  xit('should call deleteUser() if Delete-Button clicked', async(() => {
    spyOn(component, 'deleteUser');
  
    let button = fixture.debugElement.query(By.css('.btn-danger'));
    button.triggerEventHandler('click', null);
  
    fixture.whenStable().then(() => {
      expect(component.deleteUser).toHaveBeenCalled();
    });
  }));
});
