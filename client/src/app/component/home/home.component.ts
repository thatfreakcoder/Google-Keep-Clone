import { Component, OnInit } from '@angular/core';
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
        this.keeps = res;
        console.log(res);
      }
    );
  }
  postData(){
    var data: object = {
      'title' : 'Sent Thru Angular Test 2',
      'body' : 'This Post is ALSO sent from the angular client using HTTP Client Module and Flask API, but after reframing the API Request',
      'important' : false
    }
    this.data.postData(data).subscribe(
      res => {
        console.log(res);
        this.getData();
      }
    );
  }

}
