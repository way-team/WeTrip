import { Component, OnInit } from '@angular/core';
import {
  NavController,
  MenuController,
  ToastController,
  AlertController,
  LoadingController,
  Events
} from '@ionic/angular';

@Component({
  selector: 'app-gdpr2',
  templateUrl: './gdpr2.page.html',
  styleUrls: ['./gdpr2.page.scss'],
})
export class Gdpr2Page implements OnInit {

  constructor( public menuCtrl: MenuController,
  public navCtrl: NavController) {

   }

  ngOnInit() {


 this.menuCtrl.enable(true); // or true
  }
  logout() {

    this.navCtrl.navigateRoot('/');
  }
}
