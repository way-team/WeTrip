import { Component, OnInit ,AfterViewInit} from '@angular/core';
import { NavController, LoadingController, ToastController } from '@ionic/angular';
import * as $ from "jquery";

declare let paypal: any;

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
        onAuthorize: function(data, actions) {
          return actions.payment.execute().then(function(payment) {
            // TODO

          })
        }
      }, '#paypal-button');
    });
  }

  }
