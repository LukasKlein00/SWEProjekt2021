import { HttpClientTestingModule } from '@angular/common/http/testing';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { RouterTestingModule } from '@angular/router/testing';
import { SocketIoConfig, SocketIoModule } from 'ngx-socket-io';
import { environment } from 'src/environments/environment';

import { ConfirmComponent } from './confirm.component';

describe('ConfirmComponent', () => {
  let component: ConfirmComponent;
  let fixture: ComponentFixture<ConfirmComponent>;
  const config: SocketIoConfig = { url: environment.websocketUrl, options: {} };

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [SocketIoModule.forRoot(config), BrowserModule, ReactiveFormsModule, FormsModule, RouterTestingModule, HttpClientTestingModule],
      declarations: [ ConfirmComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ConfirmComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
