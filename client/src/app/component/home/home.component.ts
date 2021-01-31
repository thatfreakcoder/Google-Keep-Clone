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

  constructor( private data : GetdataService ) {}

  ngOnInit(): void {
    this.getData()
  }
  calculateDate(){
    var curr_date = new Date();
    var curr_day = curr_date.getTime().toLocaleString();
    var post_date = new Date(this.keeps['keeps'][0]['date_time']);
    var post_day = post_date.getTime().toLocaleString();
    // var difference_in_days = (curr_day - post_day) / (1000 * 3600 * 24);
    
    console.log(curr_date, post_date);
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
    var d = new Date()
    var date = `${
      d.getFullYear().toString().padStart(4, '0')}-${
        (d.getMonth()+1).toString().padStart(2, '0')}-${
          d.getDate().toString().padStart(2, '0')} ${
            d.getHours().toString().padStart(2, '0')}:${
              d.getMinutes().toString().padStart(2, '0')}:${
                d.getSeconds().toString().padStart(2, '0')}`
    var data: object = {
      'title' : 'Angular Client Post',
      'body' : 'This Post is test input, producing directly from the hosted Production database.',
      'important' : true,
      'date_time': date,
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
