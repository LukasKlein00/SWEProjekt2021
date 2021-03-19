import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthentificationService {

  private readonly apiUrl = 'http://193.196.53.67:1188'
  //private readonly apiUrl = 'http://localhost:1188'
  private currentUserSubject: BehaviorSubject<any>;
  public currentUser: Observable<any>;

  constructor(private http: HttpClient) {
    this.currentUserSubject = new BehaviorSubject<any>(JSON.parse(localStorage.getItem('currentUser')));
    this.currentUser = this.currentUserSubject.asObservable();
  }

  public get currentUserValue() {
    return this.currentUserSubject.value;
  }

  login(username, password) {
    return this.http.post<any>(`${this.apiUrl}/users/authenticate`, { username, password })
      .pipe(map(user => {
        // store user details and token in local storage to keep user logged in between page refreshes
        localStorage.setItem('currentUser', JSON.stringify(user));
        this.currentUserSubject.next(user);
        window.location.reload()
        return user;
      }));
  }

  logout() {
    // remove user from local storage and set current user to null
    localStorage.removeItem('currentUser');
    window.location.reload()
    this.currentUserSubject.next(null);
  }

  register(user) {
    return this.http.post(`${this.apiUrl}/users/register`, user);
  }
}
