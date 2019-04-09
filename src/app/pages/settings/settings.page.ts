import { Component, OnInit } from '@angular/core';
import { NavController } from '@ionic/angular';
import { CookieService } from 'ngx-cookie-service';
import { DataManagement } from 'src/app/services/dataManagement';
import { TranslateService } from '@ngx-translate/core';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.page.html',
  styleUrls: ['./settings.page.scss']
})
export class SettingsPage implements OnInit {
  lang: any;
  enableNotifications: any;
  paymentMethod: any;
  currency: any;
  enablePromo: any;
  enableHistory: any;

  languages: any = ['English', 'Spanish'];
  paymentMethods: any = ['Paypal', 'Credit Card'];
  currencies: any = ['USD', 'BRL', 'EUR'];
  public userLogged;

  constructor(
    public navCtrl: NavController,
    private cookieService: CookieService,
    public dm: DataManagement,
    private translateService: TranslateService
  ) {
    const token = this.cookieService.get('token');
    this.dm.getUserLogged(token).then(res => {
      this.userLogged = res;
    });
  }

  ngOnInit() {}

  editProfile() {
    this.navCtrl.navigateForward('edit-profile');
  }

  logout() {
    this.cookieService.delete('token');
    this.navCtrl.navigateRoot('/');
  }

  goTo(destination: string) {
    this.navCtrl.navigateForward(destination);
  }

  changeLanguage(selectedValue: { detail: { value: string; }; }){
    
    this.cookieService.set('lang', selectedValue.detail.value);
    this.translateService.use(selectedValue.detail.value);
  }

}
