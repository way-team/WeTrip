import { EditProfilePage } from '../../pages/edit-profile/edit-profile.page';
import {
  NavController,
  AlertController,
  MenuController,
  ToastController,
  PopoverController,
  ModalController,
  LoadingController
} from '@ionic/angular';

// Modals
import { SearchFilterPage } from '../../pages/modal/search-filter/search-filter.page';
import { ImagePage } from './../modal/image/image.page';
// Call notifications test by Popover and Custom Component.
import { NotificationsComponent } from './../../components/notifications/notifications.component';
import { TranslateService } from '@ngx-translate/core';
import { User, UserProfile } from '../../app.data.model';
import { DataManagement } from '../../services/dataManagement';
import { CookieService } from 'ngx-cookie-service';
import { Component, ViewChild } from '@angular/core';
import { IonInfiniteScroll } from '@ionic/angular';
@Component({
  selector: 'app-discover',
  templateUrl: './discover.page.html',
  styleUrls: ['./discover.page.scss']
})
export class DiscoverPage {
  offsetString = '';
  limitString = '';
  searchKey = '';
  yourLocation = '123 Test Street';
  themeCover = 'assets/img/ionic4-Start-Theme-cover.jpg';
  discover: UserProfile[] = [];
  newData: UserProfile[] = [];
  @ViewChild(IonInfiniteScroll) infiniteScroll: IonInfiniteScroll;
  @ViewChild('content') private content: any;
  constructor(
    public navCtrl: NavController,
    public menuCtrl: MenuController,
    public popoverCtrl: PopoverController,
    public alertCtrl: AlertController,
    public modalCtrl: ModalController,
    public toastCtrl: ToastController,
    private _translate: TranslateService,
    public dM: DataManagement,
    public cookieService: CookieService,
    public loadingCtrl: LoadingController
  ) {
    this.getInit(12, 0);
    this.getData(12, 12);
  }

  scrollToTop() {
    this.content.scrollToTop(300);
  }
  loadData(event) {
    setTimeout(() => {
      console.log('Done');

      this.getData(12, this.discover.length + 12);

      this.newData.forEach(x => this.discover.push(x));

      event.target.complete();
      // App logic to determine if all data is loaded
      // and disable the infinite scroll
      if (this.discover.length == 200) {
        event.target.disabled = true;
      }
    }, 500);
  }
  getData(offset: Number, limit: Number) {
    this.offsetString = '' + offset;
    this.limitString = '' + limit;
    this.dM
      .getData(this.offsetString, this.limitString)
      .then((data: UserProfile[]) => {
        this.newData = data;
      })
      .catch(error => {});
  }

  getInit(offset: Number, limit: Number) {
    this.offsetString = '' + offset;
    this.limitString = '' + limit;
    this.dM
      .getData(this.offsetString, this.limitString)
      .then((data: any) => {
        this.discover = data;
      })
      .catch(error => {});
  }

  ionViewWillEnter() {
    this.menuCtrl.enable(true);
  }
  contact(id) {
    this.navCtrl.navigateForward('/');
  }

  cambiaIdioma(idioma: string) {
    console.log(`Traduzco a: ${idioma}`);
    this._translate.use(idioma);
  }

  private listDiscover(): void {
    this.dM
      .listDiscover()
      .then((data: any) => {
        this.discover = data;
      })
      .catch(error => {});
  }

  settings() {
    this.navCtrl.navigateForward('settings');
  }

  async alertLocation() {
    const changeLocation = await this.alertCtrl.create({
      header: 'Change Location',
      message: 'Type your Address.',
      inputs: [
        {
          name: 'location',
          placeholder: 'Enter your new Location',
          type: 'text'
        }
      ],
      buttons: [
        {
          text: 'Cancel',
          handler: data => {
            console.log('Cancel clicked');
          }
        },
        {
          text: 'Change',
          handler: async data => {
            console.log('Change clicked', data);
            this.yourLocation = data.location;
            const toast = await this.toastCtrl.create({
              message: 'Location was change successfully',
              duration: 3000,
              position: 'top',
              closeButtonText: 'OK',
              showCloseButton: true
            });

            toast.present();
          }
        }
      ]
    });
    changeLocation.present();
  }

  async searchFilter() {
    const modal = await this.modalCtrl.create({
      component: SearchFilterPage
    });
    return await modal.present();
  }

  async presentImage(image: any) {
    const modal = await this.modalCtrl.create({
      component: ImagePage,
      componentProps: { value: image }
    });
    return await modal.present();
  }

  async notifications(ev: any) {
    const popover = await this.popoverCtrl.create({
      component: NotificationsComponent,
      event: ev,
      animated: true,
      showBackdrop: true
    });
    return await popover.present();
  }

  async sendData(username: string) {
    const translation1: string = this._translate.instant(
      'DISCOVER.ALERT_MESSAGE'
    );
    const translation3: string = this._translate.instant(
      'DISCOVER.ALERT_TITLE'
    );
    this.dM
      .sendFriendInvitation(username)
      .then(res => {
        this.showLoading();
        setTimeout(() => {
          this.alertCtrl
            .create({
              header: translation3,
              message: translation1,
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
        }, 1500);
        this.getInit(12, 0);
      })
      .catch(err => {
        this.getInit(12, 0);
      });
  }

  showLoading() {
    const translation2: string = this._translate.instant('DISCOVER.WAIT');
    this.loadingCtrl
      .create({
        message: translation2,
        showBackdrop: true,
        duration: 1000
      })
      .then(loadingEl => {
        loadingEl.present();
      });
  }
}
