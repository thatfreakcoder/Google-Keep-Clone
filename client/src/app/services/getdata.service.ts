import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class GetdataService {
  DEV_URL: string = "http://localhost:5000";
  PROD_URL: string = "https://yuvrajdagur.pythonanywhere.com";
  constructor(private http : HttpClient) { }

  getData(url:string){
    return this.http.get(`${url}/get`)
  }
  
  postData(url:string, data:any){
    return this.http.post(`${url}/new`, data)
  }

  deleteNote(url:string, data:any){
    return this.http.post(`${url}/delete`, data)
  }
}
