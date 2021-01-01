import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class GetdataService {
  serverURL = "http://localhost:5000"
  constructor(private http : HttpClient) { }

  getData(){
    return this.http.get(this.serverURL)
  }
  
  postData(data:any){
    return this.http.post(`${this.serverURL}/new`, data)
  }
}
