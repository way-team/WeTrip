import { Component, OnInit } from '@angular/core';
import { Trip, UserProfile, application_user, CreatorAndTrip } from 'src/app/app.data.model';
import { ActivatedRoute } from '@angular/router';
import { DataManagement } from 'src/app/services/dataManagement';
import { CookieService } from 'ngx-cookie-service';
import { AlertController, NavController } from '@ionic/angular';
import { TranslateService } from '@ngx-translate/core';

@Component({
  selector: 'app-trip-detail',
  templateUrl: './trip-detail.page.html',
  styleUrls: ['./trip-detail.page.scss']
})
export class TripdetailPage {
  trip: Trip;
  userLogged: UserProfile;
  myTrip = true;
  applicationsAccepted: [];
  applicationsPending: [];
  applicationsRejected: [];
  isReady: Boolean;
  rating: any;
  creator: UserProfile;

  usersAccepted: application_user[] = [];
  usersPending: application_user[] = [];
  usersRejected: application_user[] = [];
  creatorAndTrip: CreatorAndTrip;

  constructor(
    private activatedRoute: ActivatedRoute,
    private dm: DataManagement,
    private cookieService: CookieService,
    private alertController: AlertController,
    private translate: TranslateService,
    private navCtrl: NavController
  ) {
  }

  
  ngOnInit() {
    this.getItems();
  }

  private getItems() {
    this.usersAccepted = [];
    this.usersPending = [];

    const tripId = this.activatedRoute.snapshot.paramMap.get('id');
    const token = this.cookieService.get('token');

    const prom1 = this.dm.getTripById(tripId);
    const prom2 = this.dm.getUserLogged(token);

    Promise.all([prom1, prom2])
      .then(response => {
        this.trip = response[0]['trip'];

        this.creatorAndTrip = this.createAndTripFunction(this.trip);

        this.applicationsAccepted = response[0]['applicationsList'];
        this.applicationsPending = response[0]['pendingsList'];
        this.applicationsRejected = response[0]['rejectedList'];
        this.userLogged = response[1];
        if (this.trip.creator !== this.userLogged.user.username) {
          this.myTrip = false;
        }

        this.getUserPending();
        this.getUserAccepted();
        this.getUserRejecteds();

        this.dm
          .getUserBy(this.trip.creator, this.cookieService.get('token'))
          .then(res => {
            this.rating = res.avarageRate;
            this.isReady = true;
            this.creator = res;
          })
          .catch(_ => { });
      })
      .catch(_ => { });

  }

  join() {
    this.dm
      .applyForTrip(String(this.trip.id))
      .then(response => {
        response != null ? this.presentAlert() : '';
        this.getItems();
      })
      .catch(err => { });
  }

  async presentAlert() {
    const translation1: string = this.translate.instant('TRIPS.CONGRATULATION');
    const translation2: string = this.translate.instant(
      'TRIPS.APPLICATION_SEND'
    );

    const alert = await this.alertController.create({
      header: translation1,
      message: translation2,
      buttons: ['OK']
    });

    await alert.present();
  }

  getUserPending() {
    this.applicationsPending.forEach(element => {
      const userId = element['applicant'];
      this.dm.getUserById(userId).then(response => {
        const userPending = new application_user(
          response.user.username,
          element['id']
        );
        this.usersPending.push(userPending);
      });
    });
  }

  getUserAccepted() {
    this.applicationsAccepted.forEach(element => {
      const userId = element['applicant'];
      this.dm.getUserById(userId).then(response => {
        const userAccepted = new application_user(
          response.user.username,
          element['id']
        );
        this.usersAccepted.push(userAccepted);
      });
    });
  }

  getUserRejecteds() {
    this.applicationsRejected.forEach(element => {
      const userId = element['applicant'];
      this.dm.getUserById(userId).then(response => {
        const userRejected = new application_user(
          response.user.username,
          element['id']
        );
        this.usersRejected.push(userRejected);
      });
    });
  }

  goTo(destination: string, username: string) {
    const dest: string = destination + username;
    this.navCtrl.navigateForward(dest);
  }

  acceptApplication(id: string) {
    this.dm.resolveTripApplication('accept', id).then(_ => {
      this.getItems();
    });
  }

  rejectApplication(id: string) {
    this.dm.resolveTripApplication('reject', id).then(_ => {
      this.getItems();
    });
  }

  showJoinButton(): boolean {
    let show = false;
    const pastTrip = new Date(this.trip.startDate) < new Date();
    const accepted =
      this.usersAccepted.find(
        x => x.applicantName === this.userLogged.user.username
      ) != undefined;
    const pending =
      this.usersPending.find(
        x => x.applicantName === this.userLogged.user.username
      ) != undefined;
    const rejected =
      this.usersRejected.find(
        x => x.applicantName === this.userLogged.user.username
      ) != undefined;
    pastTrip || accepted || pending || rejected ? (show = false) : (show = true);
    return show;
  }


  createAndTripFunction(trip: Trip) {
    this.dm
      .getUserBy(trip.creator, this.cookieService.get('token'))
      .then(userProfile => {
        this.creator = userProfile;
        this.creatorAndTrip = new CreatorAndTrip;
        this.creatorAndTrip.status = this.creator.status;
        this.creatorAndTrip.trip = trip;
      });

    return this.creatorAndTrip;
  }
}
