import { Component, OnInit } from '@angular/core';
import { NavController } from '@ionic/angular';
import { DataManagement } from '../../services/dataManagement';
import { Trip } from '../../app.data.model';
@Component({
  selector: 'app-trips',
  templateUrl: './trips.page.html',
  styleUrls: ['./trips.page.scss']
})
export class TripsPage implements OnInit {
  listTrips: Trip[] = [];
  constructor(public navCtrl: NavController, private dm: DataManagement) {
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
}
