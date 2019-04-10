import { Component, OnInit } from '@angular/core';
import { Trip, UserProfile } from 'src/app/app.data.model';
import { ActivatedRoute } from '@angular/router';
import { DataManagement } from 'src/app/services/dataManagement';
import { CookieService } from 'ngx-cookie-service';
import { AlertController } from '@ionic/angular';

@Component({
  selector: 'app-trip-detail',
  templateUrl: './trip-detail.page.html',
  styleUrls: ['./trip-detail.page.scss'],
})
export class TripdetailPage {

  trip: Trip;
  userLogged: UserProfile;
  myTrip = true;


  constructor(
    private activatedRoute: ActivatedRoute,
    private dm: DataManagement,
    private cookieService: CookieService,
    private alertController: AlertController

  ) {
    const tripId = this.activatedRoute.snapshot.paramMap.get('id');
    const token = this.cookieService.get('token');

    const prom1 = this.dm.getTripById(tripId);
    const prom2 = this.dm.getUserLogged(token);
    Promise.all([prom1, prom2]).then(response => {
      this.trip = response[0];
      this.userLogged = response[1];
      if (this.trip.creator !== this.userLogged.user.username) {
        this.myTrip = false;
      }
    }).catch((_) => {

    });
   }

  join() {
    this.dm.applyForTrip(String(this.trip.id)).then(response => {
      response != null ? this.presentAlert() : this.noPresentAlert();
    });
  }

  async presentAlert() {
    const alert = await this.alertController.create({
      header: 'Congratulations',
      message: 'Your application has been sent.',
      buttons: ['OK']
    });

    await alert.present();
  }

  async noPresentAlert() {}

}
