import { Component, OnInit } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { Observable } from 'rxjs';
import { GetdataService } from 'src/app/services/getdata.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  keeps: any = {};
  constructor(private data : GetdataService) { }

  ngOnInit(): void {
    this.getData();
  }
  getData(){
    this.data.getData().subscribe(
      res => {
        this.keeps = Object.assign(res, this.keeps);
        console.log(this.keeps);
      }
    );
  }
  postData(){
    var data: object = {
      'title' : 'Sent Thru Angular',
      'body' : 'This Post is sent from the angular client using HTTP Client Module and Flask API',
      'important' : true
    }
    this.data.postData(data).subscribe(
      res => {
        console.log(res);
      }
    );
    this.getData()
  }

}
