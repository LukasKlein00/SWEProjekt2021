import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { environment } from 'src/environments/environment';
import * as uuid from 'uuid';

@Injectable({
  providedIn: 'root'
})
export class AuthentificationService {

  private readonly apiUrl = environment.httpUrl;
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
    return this.http.post<any>(`${this.apiUrl}/login`, { username, password })
      .pipe(map(user => {
        // store user details and token in local storage to keep user logged in between page refreshes
        localStorage.setItem('currentUser', JSON.stringify(user));
        this.currentUserSubject.next(user);
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
    user.userID = uuid.v4();
    return this.http.post(`${this.apiUrl}/register`, user);
  }

  confirm(token) {
    return this.http.post(`${this.apiUrl}/confirm`, {token});
  }

  reset(resetobject) {
    return this.http.post(`${this.apiUrl}/reset`, resetobject);
  }

  forgot(email) {
    return this.http.post(`${this.apiUrl}/forgot`, email);
  }

  check() {
    return this.http.post(`${this.apiUrl}/check`, JSON.parse(localStorage.getItem('currentUser')));
  }
}
