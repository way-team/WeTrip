import {  Component, OnInit } from '@angular/core';
import {
  NavController,
} from '@ionic/angular';
@Component({
  selector: 'app-contacts',
  templateUrl: './contacts.page.html',
  styleUrls: ['./contacts.page.scss'],
})
export class ContactsPage implements OnInit {

  constructor( public navCtrl: NavController) {

       }

  ngOnInit() {
  }
  chat(id) {
    this.navCtrl.navigateForward('/chat/1');
  }
      editProfile(id) {
    this.navCtrl.navigateForward('/display-profile/2');
  }
}
