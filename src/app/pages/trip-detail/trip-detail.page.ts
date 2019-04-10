import { Component, OnInit } from '@angular/core';
import { Trip, UserProfile, application_user } from 'src/app/app.data.model';
import { ActivatedRoute } from '@angular/router';
import { DataManagement } from 'src/app/services/dataManagement';
import { CookieService } from 'ngx-cookie-service';
import { AlertController, NavController } from '@ionic/angular';

@Component({
  selector: 'app-trip-detail',
  templateUrl: './trip-detail.page.html',
  styleUrls: ['./trip-detail.page.scss'],
})
export class TripdetailPage {

  trip: Trip;
  userLogged: UserProfile;
  myTrip = true;
  applicationsAccepted: [];
  applicationPending: [];

  usersAccepted: application_user[] = [];
  usersPending: application_user[] = [];

  constructor(
    private activatedRoute: ActivatedRoute,
    private dm: DataManagement,
    private cookieService: CookieService,
    private alertController: AlertController,
    private navCtrl: NavController
  ) {
    this.getItems();
   }

  private getItems() {
    this.usersAccepted = [];
    this.usersPending = [];

    const tripId = this.activatedRoute.snapshot.paramMap.get('id');
    const token = this.cookieService.get('token');

    const prom1 = this.dm.getTripById(tripId);
    const prom2 = this.dm.getUserLogged(token);

    Promise.all([prom1, prom2]).then(response => {
      this.trip = response[0]['trip'];
      this.applicationsAccepted = response[0]['applicationsList'];
      this.applicationPending = response[0]['pendingsList'];
      this.userLogged = response[1];
      if (this.trip.creator !== this.userLogged.user.username) {
        this.myTrip = false;
      }
      if (this.myTrip) {
        this.getUserPending();
        this.getUserAccepted();
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

  getUserPending() {
    this.applicationPending.forEach(element => {
      const userId = element['applicant'];
      this.dm.getUserById(userId).then((response) => {
        const userPending = new application_user(response.user.username, element['id']);
        this.usersPending.push(userPending);
      });
    });
  }

  getUserAccepted() {
    this.applicationsAccepted.forEach(element => {
      const userId = element['applicant'];
      this.dm.getUserById(userId).then((response) => {
        const userAccepted = new application_user(response.user.username, element['id']);
        this.usersAccepted.push(userAccepted);
      });
    });
  }

  goTo(destination: string, username: string) {
    const dest: string = destination + username;
    this.navCtrl.navigateForward(dest);
  }

  acceptApplication(id: string) {
    this.dm.resolveTripApplication("accept", id).then((_) => {
      this.getItems();
    });
  }

  rejectApplication(id: string) {
    this.dm.resolveTripApplication("reject", id).then((_) => {
      this.getItems();
    });
  }


}
