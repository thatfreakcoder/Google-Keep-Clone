import { Component, OnInit } from '@angular/core';
import { GetdataService } from 'src/app/services/getdata.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  keeps: any = {};
  colorVal: string;
  url: string = this.data.DEV_URL;

  constructor(private data : GetdataService) { }

  ngOnInit(): void {
    this.getData();
  }
  onSignIn(googleUser) {
    var profile = googleUser.getBasicProfile();
    console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
    console.log('Name: ' + profile.getName());
    console.log('Image URL: ' + profile.getImageUrl());
    console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
  }

  getValue(val){
    console.log(typeof val, val.length, val);
    
  }
  getData(){
    this.data.getData(this.url).subscribe(
      res => {
        this.keeps = res;
        console.log(res);
      }
    );
  }
  postData(){
    var data: object = {
      'title' : 'Sent Thru Angular Test 2',
      'body' : 'This Post is ALSO sent from the angular client using HTTP Client Module and Flask API, but after reframing the API Request',
      'important' : false,
      'color': '#26ffb0'
    }
    this.data.postData(this.url, data).subscribe(
      res => {
        console.log(res);
        this.getData();
      }
    );
  }
  deleteData(id:number){
    var data = {
      'id': id
    };
    console.log(data);
    // this.data.deleteNote(this.url, data).subscribe(
    //   res => {
    //     console.log(res);
    //     this.getData()
    //   }, 
    //   err => {
    //     console.log(err);
        
    //   }
    // )
  }

}
