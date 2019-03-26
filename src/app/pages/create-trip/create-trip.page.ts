import { Component, OnInit } from '@angular/core';
import { City } from 'src/app/app.data.model';
import { DataManagement } from 'src/app/services/dataManagement';

@Component({
  selector: 'app-create-trip',
  templateUrl: './create-trip.page.html',
  styleUrls: ['./create-trip.page.scss'],
})
export class CreateTripPage implements OnInit {

  title: String;
  description: String;
  start_date: Date;
  end_date: Date;
  trip_type: String;
  image: String;
  city: City;
  error: string;




  constructor(public dm: DataManagement) {


  }

  ngOnInit() {
  }


  public createTrip() {
    this.dm.createTrip(this.title, this.description, this.start_date, this.end_date, this.trip_type, this.image, this.city).then((data) => {
    }).catch((error) => {
      this.error = error;
    });
  }













}
