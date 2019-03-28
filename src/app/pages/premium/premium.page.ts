import { Component, OnInit } from '@angular/core';
import { NavController, LoadingController, ToastController } from '@ionic/angular';

@Component({
  selector: 'app-premium',
  templateUrl: './premium.page.html',
  styleUrls: ['./premium.page.scss'],
})
export class PremiumPage implements OnInit {

  constructor(
   public toastCtrl: ToastController,
   public navCtrl: NavController,
   public loadingCtrl: LoadingController) { }

  ngOnInit() {
  }
  async payment() {
    const loader = await this.loadingCtrl.create({
      duration: 2000
    });

    loader.present();
    loader.onWillDismiss().then(async l => {
      const toast = await this.toastCtrl.create({
        showCloseButton: true,
        cssClass: 'bg-profile',
        message: 'This feature is not implemented yet!',
        duration: 3000,
         position: 'bottom'
      });

      toast.present();
      this.navCtrl.navigateForward('/discover');
    });
  }

}