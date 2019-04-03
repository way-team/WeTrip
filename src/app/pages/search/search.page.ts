import { Component, OnInit } from '@angular/core';
import { Trip } from '../../app.data.model';
import { NavController } from '@ionic/angular';
import { DataManagement } from '../../services/dataManagement';
import { ConfigService } from 'src/config/configService';

@Component({
  selector: 'app-search',
  templateUrl: './search.page.html',
  styleUrls: ['./search.page.scss']
})
export class SearchPage implements OnInit {
  path = '';
  listSearch: Trip[] = [];
  constructor(
    public navCtrl: NavController,
    private dm: DataManagement,
    private config: ConfigService
  ) {
    this.path = this.config.config().restUrlPrefixLocalhost;
    this.listSearchTrips();
  }

  ngOnInit() {}

  ionViewWillEnter() {
    this.listSearchTrips();
  }

  goToMyTrips() {
    this.navCtrl.navigateForward('/trips');
  }

  public listSearchTrips(): void {
    this.dm
      .listSearchTrips()
      .then((data: any) => {
        this.listSearch = data;
      })
      .catch(error => {});
  }
}
