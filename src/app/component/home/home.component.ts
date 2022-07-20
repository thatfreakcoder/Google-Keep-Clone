import { Component, OnInit } from '@angular/core';
import { GetdataService } from 'src/app/services/getdata.service';
import {MatDialog} from '@angular/material/dialog';
import { EditNoteComponent } from '../edit-note/edit-note.component';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  keeps: any = {};
  colorVal: string;
  url: string = this.service.PROD_URL;

  constructor( private service : GetdataService, public dialog: MatDialog) {}

  ngOnInit(): void {
    this.getData()
  }

  openDialog(id){
    let dialogRef = this.dialog.open(EditNoteComponent, {data: {
                                                              title: this.keeps['keeps'][id]['title'],
                                                              body: this.keeps['keeps'][id]['body'],
                                                              color: this.keeps['keeps'][id]['color'],
                                                              important: this.keeps['keeps'][id]['important']
                                                                    }, 
                                                          minHeight: '50%', minWidth: '70%',hasBackdrop: true});

    dialogRef.afterClosed().subscribe(
      result => {
        console.log(`Dialog Result : ${result}`);
        if (result === 'refresh') {
          this.getData();
        }
      }
    )
  }

  getData(){
    this.service.getData(this.url).subscribe(
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
    this.service.postData(this.url, data).subscribe(
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
    this.service.deleteNote(this.url, data).subscribe(
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
