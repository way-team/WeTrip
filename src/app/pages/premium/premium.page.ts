import { Component, OnInit ,AfterViewInit} from '@angular/core';
import { NavController, LoadingController, ToastController , AlertController} from '@ionic/angular';
import * as $ from "jquery";
import { User, UserProfile } from '../../app.data.model';
import { DataManagement } from '../../services/dataManagement';
import { CookieService } from 'ngx-cookie-service';
import { Location } from '@angular/common';

declare let paypal: any;

@Component({
  selector: 'app-premium',
  templateUrl: './premium.page.html',
  styleUrls: ['./premium.page.scss'],
})
export class PremiumPage implements OnInit {
   public premium: boolean;
   public logged: UserProfile;
   private username: string;



  constructor(
       public toastCtrl: ToastController,
       public navCtrl: NavController,
       public loadingCtrl: LoadingController,
        public dM: DataManagement,
        private cookieService: CookieService,
        public alertCtrl: AlertController,
        private location: Location
     ) {

     const token = this.cookieService.get('token');
     this.dM
      .getUserLogged(token)
      .then(res => {
        this.logged = res;
        this.premium=res.isPremium;
        this.username=res.user.username;
      })
      .catch(err => {
        console.log('Error: ' + err);
      }); }

  ngOnInit() {

    }
    paid() {
    this.dM
      .paid()
      .then(data => {
      })
      .catch(error => {
        this.alertCtrl
          .create({
            header: 'Error',
            message: 'Something went wrong.',
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

  async payment() {
    const loader = await this.loadingCtrl.create({
      duration: 2000
    });}

   loadExternalScript(scriptUrl: string) {
    return new Promise((resolve, reject) => {
      const scriptElement = document.createElement('script')
      scriptElement.src = scriptUrl
      scriptElement.onload = resolve
      document.body.appendChild(scriptElement)
  });}
ngAfterViewInit(): void {
    this.loadExternalScript("https://www.paypalobjects.com/api/checkout.js").then(() => {
      paypal.Button.render({
        env: 'sandbox',
        client: {
          production: '',
          sandbox: 'AddLPh79rdzGB5QdmTWhN0coPnuTCg9_1hEkeyKv6rZtoK-m4MIaq3syIe5sCRmndpu9WAt-gpwLWBs9'
        },
        commit: true,
        payment: function (data, actions) {
          return actions.payment.create({
            payment: {
              transactions: [
                {
                  amount: { total: '10.00', currency: 'EUR' }
                }
              ]
            }
          })
        },
        onAuthorize: (data, actions) => {
          return actions.payment.execute().then( (payment) => {

             this.paid();
             this.ngOnInit();
          })
        }
      }, '#paypal-button');
    });
  }

  }
