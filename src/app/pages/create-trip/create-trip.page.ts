import { Component, OnInit } from '@angular/core';
import { City } from '../../app.data.model';
import { DataManagement } from '../../services/dataManagement';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { AlertController, NavController } from '@ionic/angular';

@Component({
  selector: 'app-create-trip',
  templateUrl: './create-trip.page.html',
  styleUrls: ['./create-trip.page.scss']
})
export class CreateTripPage implements OnInit {
  public onCreateForm: FormGroup;
  title: string;
  description: string;
  start_date: String;
  end_date: String;
  trip_type: string = 'PUBLIC';
  image;
  city: Number;
  error: string;
  cities: City[];

  constructor(
    public navCtrl: NavController,
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
        this.description === undefined ? '' : this.description,
        this.start_date.split('T')[0],
        this.end_date.split('T')[0],
        this.trip_type,
        this.image === undefined ? '' : this.image,
        this.city
      )
      .then(data => {
        //this.navCtrl.navigateRoot('/discover');
        this.navCtrl.navigateForward('/trips');
      })
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
