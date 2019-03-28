import { Component, OnInit } from '@angular/core';
import { NavController } from '@ionic/angular';
@Component({
  selector: 'app-trips',
  templateUrl: './trips.page.html',
  styleUrls: ['./trips.page.scss']
})
export class TripsPage implements OnInit {
  constructor(public navCtrl: NavController) {}

  ngOnInit() {}
  // view trip detail
  viewDetail(id) {
    this.navCtrl.navigateForward('/trip-detail/2');
  }

  goToCreate() {
    this.navCtrl.navigateForward('/create-trip');
  }
}
