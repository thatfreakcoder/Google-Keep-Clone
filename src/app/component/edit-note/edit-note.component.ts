import { Component, OnInit, Inject } from '@angular/core';
import { GetdataService } from 'src/app/services/getdata.service';
import { MAT_DIALOG_DATA } from "@angular/material/dialog";

@Component({
  selector: 'app-edit-note',
  templateUrl: './edit-note.component.html',
  styleUrls: ['./edit-note.component.css']
})
export class EditNoteComponent {
  url = this.service.PROD_URL;
  title: string = "First Edited Note";
  body: string = "This note has been edited to check whether position of the note changes.\n EDIT: Doesn't Change hence SUCCESS";
  color: string = "#f542f5";
  important: boolean = false;
  
  constructor(@Inject(MAT_DIALOG_DATA) public data: any, private service : GetdataService) { }

  editNote(){
    var data: object = {
      'id': 1,
      'title': this.title,
      'body': this.body,
      'color': this.color,
      'important': this.important
  }
    // console.log(post_id);
    this.service.editNote(this.url, data).subscribe(
      res =>{
        console.log(res)
      }
    );
  }

}
