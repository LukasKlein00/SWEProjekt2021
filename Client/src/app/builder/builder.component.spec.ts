import { HttpClientTestingModule } from '@angular/common/http/testing';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { FormsModule } from '@angular/forms';
import { MatBadgeModule } from '@angular/material/badge';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatSliderModule } from '@angular/material/slider';
import { RouterTestingModule } from '@angular/router/testing';
import { NgSelectModule } from '@ng-select/ng-select';
import { SocketIoConfig, SocketIoModule } from 'ngx-socket-io';
import { environment } from 'src/environments/environment';

import { BuilderComponent } from './builder.component';

describe('BuilderComponent', () => {
  let component: BuilderComponent;
  let fixture: ComponentFixture<BuilderComponent>;
  const config: SocketIoConfig = { url: environment.websocketUrl, options: {} };

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BuilderComponent ],
      imports: [
        SocketIoModule.forRoot(config),
        FormsModule,
        NgSelectModule,
        MatSliderModule,
        MatSlideToggleModule,
        MatBadgeModule,
        HttpClientTestingModule,
        RouterTestingModule,
      ],
      schemas: [
          CUSTOM_ELEMENTS_SCHEMA
        ],  
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BuilderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
