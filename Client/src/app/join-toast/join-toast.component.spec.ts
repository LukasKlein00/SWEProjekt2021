import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { SocketIoConfig, SocketIoModule } from 'ngx-socket-io';
import { environment } from 'src/environments/environment';

import { JoinToastComponent } from './join-toast.component';

describe('JoinToastComponent', () => {
  let component: JoinToastComponent;
  let fixture: ComponentFixture<JoinToastComponent>;
  const config: SocketIoConfig = { url: environment.websocketUrl, options: {} };

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [SocketIoModule.forRoot(config)],
      declarations: [ JoinToastComponent ],
      schemas: [
        CUSTOM_ELEMENTS_SCHEMA
      ],
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
