import { HttpClientModule } from '@angular/common/http';
import { TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';
import { RouterTestingModule } from '@angular/router/testing';
import { AppComponent } from '../app.component';

import { AuthguardService } from './authguard.service';


describe('AuthguardService', () => {
  let service: AuthguardService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [RouterTestingModule, HttpClientModule]
    });
    service = TestBed.inject(AuthguardService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
