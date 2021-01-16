import { NgZone } from '@angular/core';
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
  url: string = this.data.PROD_URL;
  name: any;
  email: any;
  profile: any;

  constructor(
    private data : GetdataService,
    ngZone: NgZone 
    ) { 
      window['onSignIn'] = user => ngZone.run(
        () => {
          this.onSignIn(user);
        }
      );
     }

  ngOnInit(): void {
    this.getData();
  }

  onSignIn(googleUser){
    console.log(JSON.stringify(googleUser.getBasicProfile()));
    this.name = googleUser.getBasicProfile()['Ad'];
    this.email = googleUser.getBasicProfile()['cu'];
    this.profile = googleUser.getBasicProfile()['SJ'];
    console.log(this.name, this.profile, this.email);
    
  }
 // Google Sign In Boilerplate Code

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
      'title' : 'Angular Client Post',
      'body' : 'This Post is test input, producing directly from the hosted Production database.',
      'important' : true,
      'edited': false,
      'date_time': new Date().toISOString().replace(/T/, ' ').replace(/\..+/, ''),
      'color': '#29f4ff'
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
    this.data.deleteNote(this.url, data).subscribe(
      res => {
        console.log(res);
        this.getData()
      }, 
      err => {
        console.log(err);
        
      }
    )
  }

}
