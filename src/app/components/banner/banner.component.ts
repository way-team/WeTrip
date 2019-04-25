import { Component, OnInit } from '@angular/core';
import { DataManagement } from 'src/app/services/dataManagement';
import { CookieService } from 'ngx-cookie-service';
import { ModalController } from '@ionic/angular';
import { ImagePage } from 'src/app/pages/modal/image/image.page';

@Component({
  selector: 'app-banner',
  templateUrl: './banner.component.html',
  styleUrls: ['./banner.component.scss']
})
export class BannerComponent implements OnInit {
  isPremium: boolean;

  bannerPath: string;
  bannerSrc: string;

  constructor(
    public dM: DataManagement,
    public cookieService: CookieService,
    public modalCtrl: ModalController
  ) {
    this.getUserPremium();
    this.aleatorio(1, 5);
  }

  ngOnInit() {}
  aleatorio(a, b) {
    const imagenId = Math.round(Math.random() * (b - a) + parseInt(a));
    const urls = [
      'https://www.vueling.com/es',
      'https://www.booking.com/index.es.html',
      'https://www.skyscanner.es/',
      'https://www.trivago.es/',
      'https://www.expedia.es/'
    ];
    this.bannerSrc = 'assets/img/banner/' + imagenId + '.jpg';
    this.bannerPath = urls[imagenId - 1];
  }

  private getUserPremium(): void {
    let token: String;
    token = this.cookieService.get('token');
    this.dM
      .getUserLogged(token)
      .then((data: any) => {
        this.isPremium = data.isPremium;
      })
      .catch(error => {});
  }
  async presentImage(image: any) {
    const modal = await this.modalCtrl.create({
      component: ImagePage,
      componentProps: { value: image }
    });
    return await modal.present();
  }
}
