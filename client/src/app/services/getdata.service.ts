import { Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class GetdataService {
  DEV_URL: string = "http://localhost:5000/keeps";
  PROD_URL: string = "https://appsbyyuvraj.pythonanywhere.com/keeps";
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
