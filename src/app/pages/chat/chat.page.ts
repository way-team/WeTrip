import { Component, OnInit } from '@angular/core';
import { AlertController } from '@ionic/angular';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.page.html',
  styleUrls: ['./chat.page.scss']
})
export class ChatPage implements OnInit {
  constructor(public alertCtrl: AlertController) {
    this.alertCtrl
      .create({
        header: 'Future feature',
        message: 'The chat is coming next week.',
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
  }

  ngOnInit() {}
}
