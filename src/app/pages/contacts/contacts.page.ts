import { Component, OnInit } from '@angular/core';
import { NavController } from '@ionic/angular';
import { User } from '../../app.data.model';
import { DataManagement } from '../../services/dataManagement';
@Component({
  selector: 'app-contacts',
  templateUrl: './contacts.page.html',
  styleUrls: ['./contacts.page.scss']
})
export class ContactsPage implements OnInit {
  friends: User[] = [];
  meetYou: User[] = [];
  constructor(public navCtrl: NavController, public dM: DataManagement) {
    this.listFriends();
    this.listMeetYou();
  }

  ngOnInit() {}

  chat(id) {
    this.navCtrl.navigateForward('/chat/1');
  }
  editProfile(id) {
    this.navCtrl.navigateForward('/edit-profile/2');
  }

  private listFriends(): void {
    this.dM
      .listFriends()
      .then((data: any) => {
        this.friends = data;
      })
      .catch(error => {});
  }

  private listMeetYou(): void {
    this.dM
      .listMeetYou()
      .then((data: any) => {
        this.meetYou = data;
      })
      .catch(error => {});
  }
}
