import { Component } from '@angular/core';
import { EditProfilePage } from '../../pages/edit-profile/edit-profile.page';
import {
  NavController,
  AlertController,
  MenuController,
  ToastController,
  PopoverController,
  ModalController
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

@Component({
  selector: 'app-discover',
  templateUrl: './discover.page.html',
  styleUrls: ['./discover.page.scss']
})
export class DiscoverPage {
  searchKey = '';
  yourLocation = '123 Test Street';
  themeCover = 'assets/img/ionic4-Start-Theme-cover.jpg';
  discover: UserProfile[] = [];
  isPremium: boolean;

  constructor(
    public navCtrl: NavController,
    public menuCtrl: MenuController,
    public popoverCtrl: PopoverController,
    public alertCtrl: AlertController,
    public modalCtrl: ModalController,
    public toastCtrl: ToastController,
    private _translate: TranslateService,
    public dM: DataManagement,
    public cookieService: CookieService
  ) {
    this.listDiscover();
    this.getUserPremium();
  }

  contact(id) {
    this.navCtrl.navigateForward('/');
  }

  cambiaIdioma(idioma: string) {
    console.log(`Traduzco a: ${idioma}`);
    this._translate.use(idioma);
  }


  private getUserPremium(): void {
    user: UserProfile;
    let token: String;
    token = this.cookieService.get('token');
    this.dM.getUserLogged(token).then((data: any) => {
      this.isPremium = data.isPremium;
    }).catch(error => { });

  }

  private listDiscover(): void {
    this.dM
      .listDiscover()
      .then((data: any) => {
        this.discover = data;
      })
      .catch(error => { });
  }
  ionViewWillEnter() {
    this.menuCtrl.enable(true);
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
    this.dM.sendFriendInvitation(username).then((res) => {
      console.log('Hola');
      this.listDiscover();
    }).catch((err) => {
      this.listDiscover();
    });
  }
}
