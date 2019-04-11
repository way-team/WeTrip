import { Component, OnInit } from '@angular/core';
import { City } from '../../app.data.model';
import { DataManagement } from '../../services/dataManagement';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { AlertController, NavController } from '@ionic/angular';
import { ActivatedRoute } from '@angular/router';
import { TranslateService } from '@ngx-translate/core';

@Component({
  selector: 'app-create-trip',
  templateUrl: './create-trip.page.html',
  styleUrls: ['./create-trip.page.scss']
})
export class CreateTripPage implements OnInit {
  public onCreateForm: FormGroup;
  id: String;
  title: string;
  description: string;
  start_date: string;
  end_date: string;
  trip_type: string = 'PUBLIC';
  city: Number;
  image: File = null;
  error: string;
  cities: City[];
  userImage: File = null;
  privacyPolicites: boolean;
  validateDatesAttr: boolean = true;
  validateDatesBeforeToday: boolean = true;
  minDate: Date = new Date();

  constructor(
    public navCtrl: NavController,
    public dm: DataManagement,
    private formBuilder: FormBuilder,
    public alertCtrl: AlertController,
    private translate: TranslateService,
    private activatedRoute: ActivatedRoute
  ) {
    this.listCities();
    this.id = this.activatedRoute.snapshot.paramMap.get('id');
  }

  ngOnInit() {
    this.onCreateForm = this.formBuilder.group({
      title: [null, Validators.compose([Validators.required])],
      start_date: [null, Validators.compose([Validators.required])],
      end_date: [null, Validators.compose([Validators.required])],
      city: [null, Validators.compose([Validators.required])],
      userImage: [null, null]
    });
  }

  public createTrip() {
    let translation:string = this.translate.instant('TRIPS.ERROR');
    console.log(typeof this.userImage);
    this.dm
      .createTrip(
        this.title,
        this.description === undefined ? '' : this.description,
        this.start_date.split('T')[0],
        this.end_date.split('T')[0],
        this.trip_type,
        this.city,
        this.userImage
      )
      .then(data => {
        this.navCtrl.navigateForward('/trips');
      })
      .catch(error => {
        this.alertCtrl
          .create({
            header: 'Error',
            message: translation,
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

  public editTrip() {
    console.log(typeof this.userImage);
    let translation:string = this.translate.instant('TRIPS.ERROR');
    this.dm
      .editTrip(
        this.id,
        this.title,
        this.description === undefined ? '' : this.description,
        this.start_date.split('T')[0],
        this.end_date.split('T')[0],
        this.trip_type,
        this.city,
        this.userImage
      )
      .then(data => {
        this.navCtrl.navigateForward('/trips');
      })
      .catch(error => {
        this.alertCtrl
          .create({
            header: 'Error',
            message: translation,
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
  goToPrivacyPolicies() {
    this.navCtrl.navigateForward('/gdpr');
  }

  validateDates() {
    const start = new Date(this.start_date);
    const end = new Date(this.end_date);

    if (start > end) {
      this.validateDatesAttr = false;
    } else {
      this.validateDatesAttr = true;
    }
    if (start < this.minDate) {
      this.validateDatesBeforeToday = false;
    } else {
      this.validateDatesBeforeToday = true;
    }
  }
  onFileInputChange(file: File) {
    this.userImage = file[0];
  }
}
