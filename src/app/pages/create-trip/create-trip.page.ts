import { Component, OnInit } from '@angular/core';
import { City } from '../../app.data.model';
import { DataManagement } from '../../services/dataManagement';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { AlertController } from '@ionic/angular';

@Component({
  selector: 'app-create-trip',
  templateUrl: './create-trip.page.html',
  styleUrls: ['./create-trip.page.scss']
})
export class CreateTripPage implements OnInit {
  public onCreateForm: FormGroup;
  title: string;
  description: string;
  start_date: Date;
  end_date: Date;
  trip_type: string = 'PUBLIC';
  image: string;
  city: Number;
  error: string;
  cities: City[];

  constructor(
    public dm: DataManagement,
    private formBuilder: FormBuilder,
    public alertCtrl: AlertController
  ) {
    this.listCities();
  }

  ngOnInit() {
    this.onCreateForm = this.formBuilder.group({
      title: [null, Validators.compose([Validators.required])],
      start_date: [null, Validators.compose([Validators.required])],
      end_date: [null, Validators.compose([Validators.required])],
      city: [null, Validators.compose([Validators.required])]
    });
  }

  public createTrip() {
    this.dm
      .createTrip(
        this.title,
        this.description,
        this.start_date,
        this.end_date,
        this.trip_type,
        this.image,
        this.city
      )
      .then(data => {})
      .catch(error => {
        this.alertCtrl
          .create({
            header: 'Error',
            message: 'Something went wrong.',
            buttons: [
              {
                text: 'Ok',
                role: 'ok'
              }
            ]
          })
          .then(alertEl => {
            alertEl.present();
          });
      });
  }

  public listCities() {
    this.dm
      .listCities()
      .then(data => {
        this.cities = data;
      })
      .catch(error => {
        console.log(error);
      });
  }
}
