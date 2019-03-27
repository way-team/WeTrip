import { Component, OnInit } from '@angular/core';
import { City } from '../../app.data.model';
import { DataManagement } from '../../services/dataManagement';

@Component({
  selector: 'app-create-trip',
  templateUrl: './create-trip.page.html',
  styleUrls: ['./create-trip.page.scss'],
})
export class CreateTripPage implements OnInit {

  title: string;
  description: string;
  start_date: Date;
  end_date: Date;
  trip_type: string;
  image: string;
  city: City;
  error: string;
  cities: City[] = [];




  constructor(public dm: DataManagement) {
    this.listCities();

  }

  ngOnInit() {
  }


  public createTrip() {
    this.dm.createTrip(this.title, this.description, this.start_date, this.end_date, this.trip_type, this.image, this.city).then((data) => {
    }).catch((error) => {
      this.error = error;
    });
  }

  public listCities() {
    this.dm.listCities().then((data) => {
      this.cities = data;
    }).catch((error) => {
      this.error = error;
    });
  }
}



