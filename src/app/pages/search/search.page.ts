import { Component, OnInit } from '@angular/core';
import { Trip } from '../../app.data.model';
import { NavController, ModalController, AlertController } from '@ionic/angular';
import { DataManagement } from '../../services/dataManagement';
import { ConfigService } from 'src/config/configService';
import { SearchFilterPage } from '../../pages/modal/search-filter/search-filter.page';
import { ImagePage } from './../modal/image/image.page';
import { TranslateService } from '@ngx-translate/core';

@Component({
  selector: 'app-search',
  templateUrl: './search.page.html',
  styleUrls: ['./search.page.scss']
})
export class SearchPage implements OnInit {
  searchKey = '';
  path = '';
  listSearch: Trip[] = [];
  constructor(
    public navCtrl: NavController,
    public alertCtrl: AlertController,
    private dm: DataManagement,
    private config: ConfigService,
    private translate: TranslateService,
    public modalCtrl: ModalController
  ) {
    this.path = this.config.config().restUrlPrefixLocalhost;
    this.listSearchTrips();
  }

  ngOnInit() {}

  ionViewWillEnter() {
    this.list();
  }

  private list(){
    if(this.searchKey ==''){
    this.listSearchTrips()
    }
    else{
    this.search()
    }

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
  
  public goTo(destination: string, id) {
    const path = destination + id;
    console.log(path);
    this.navCtrl.navigateForward(path);
  }


    public search() {
    let translation:string = this.translate.instant('TRIPS.ERROR');
    this.dm
      .search(
        this.searchKey
      )
       .then((data: any) => {
        this.listSearch = data;
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
}
