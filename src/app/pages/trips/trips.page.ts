import { Component, OnInit } from '@angular/core';
import { NavController, AlertController } from '@ionic/angular';
import { DataManagement } from '../../services/dataManagement';
import { Trip } from '../../app.data.model';
import { ConfigService } from 'src/config/configService';
import { TranslateService } from '@ngx-translate/core';
@Component({
  selector: 'app-trips',
  templateUrl: './trips.page.html',
  styleUrls: ['./trips.page.scss']
})
export class TripsPage implements OnInit {
  path = '';
  listTrips: Trip[] = [];
  constructor(
    public navCtrl: NavController,
    private dm: DataManagement,
    private config: ConfigService,
    private translate: TranslateService,
    private alertCtrl: AlertController
  ) {
    this.path = this.config.config().restUrlPrefixLocalhost;
    this.listYourTrips();
  }

  ngOnInit() {}

  ionViewWillEnter() {
    this.listYourTrips();
  }
  // view trip detail
  viewDetail(id) {
    this.navCtrl.navigateForward('/trip-detail/2');
  }

  goToCreate() {
    this.navCtrl.navigateForward('/create-trip');
  }

  public listYourTrips(): void {
    this.dm
      .listYourTrips()
      .then((data: any) => {
        this.listTrips = data;
      })
      .catch(error => {});
  }

  public goTo(destination: string, trip) {
    const path = destination + trip.id;
    this.navCtrl.navigateForward(path);
  }

  public applyForTrip(tripId: string) {
    this.dm.applyForTrip(tripId).then((_) => {
      this.presentAlert();
    }).catch((_) => {

    });
  }

  presentAlert() {
    const alert = this.alertCtrl.create(
      {
        message: 'hola',
      });
      alert.then((res) => {
        console.log(res);
      });
  }

}
