import { Component } from '@angular/core';

import { Platform, NavController } from '@ionic/angular';
import { SplashScreen } from '@ionic-native/splash-screen/ngx';
import { StatusBar } from '@ionic-native/status-bar/ngx';

import { Pages } from './interfaces/pages';
import { TranslateService } from '@ngx-translate/core';
import { CookieService } from 'ngx-cookie-service';
import { DataManagement } from './services/dataManagement';
import { Events } from '@ionic/angular';

@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  public appPages: Array<Pages>;
  public userLogged;

  constructor(
    private platform: Platform,
    private splashScreen: SplashScreen,
    private statusBar: StatusBar,
    public navCtrl: NavController,
    private _translate: TranslateService,
    private cookieService: CookieService,
    public dm: DataManagement,
    public events: Events
  ) {
    events.subscribe('user:logged', user => {
      this.userLogged = user;
    });
    if (!this.cookieService.check('token')) {
      this.userLogged = null;
    } else {
      const token = this.cookieService.get('token');
      this.dm.getUserLogged(token).then(res => {
        this.userLogged = res;
      });
    }
    /*this.userLogged = this.cookieService.check('token')
      ? this.dm.getUserLogged(this.cookieService.get('token'))
      : null;*/
    this.appPages = [
      {
        title: 'Discover',
        url: '/discover',
        direct: 'root',
        icon: 'compass'
      },
      {
        title: 'Contacts',
        url: '/contacts',
        direct: 'forward',
        icon: 'contact'
      },

      {
        title: 'Premium',
        url: '/premium',
        direct: 'forward',
        icon: 'trophy'
      },
      {
        title: 'About',
        url: '/about',
        direct: 'forward',
        icon: 'information-circle-outline'
      },

      {
        title: 'App Settings',
        url: '/settings',
        direct: 'forward',
        icon: 'cog'
      }
    ];

    this.initializeApp();
    let userLang = navigator.language.split('-')[0];
    userLang = /(en|de|it|fr|es|be)/gi.test(userLang) ? userLang : 'en';
    this._translate.use(userLang);
  }

  initializeApp() {
    this.platform
      .ready()
      .then(() => {
        this.statusBar.styleDefault();
        this.splashScreen.hide();

        if (this.cookieService.check('token')) {
          this.navCtrl.navigateForward('discover');
        }
      })
      .catch(() => {});
  }

  goToEditProgile() {
    this.navCtrl.navigateForward('edit-profile');
  }

  logout() {
    this.cookieService.delete('token');
    this.navCtrl.navigateRoot('/');
  }

  goTo(destination: string) {
    this.navCtrl.navigateForward('user-profile');
  }
}
