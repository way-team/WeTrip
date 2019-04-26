import { Component, OnInit } from '@angular/core';
import { NavController,AlertController } from '@ionic/angular';
import { User, UserProfile } from '../../app.data.model';
import { DataManagement } from '../../services/dataManagement';
import { CookieService } from 'ngx-cookie-service';
import { TranslateService } from '@ngx-translate/core';

@Component({
  selector: 'app-contacts',
  templateUrl: './contacts.page.html',
  styleUrls: ['./contacts.page.scss']
})
export class ContactsPage implements OnInit {
  friends: UserProfile[] = [];
  meetYou: UserProfile[] = [];
  youWantToMeet: UserProfile[] = [];
  logged: UserProfile;

  constructor(
    public navCtrl: NavController,
    public dM: DataManagement,
    private cookieService: CookieService,
     public alertCtrl: AlertController,
       private translate: TranslateService
  ) {
    const token = this.cookieService.get('token');
    this.dM
      .getUserLogged(token)
      .then(res => {
        this.logged = res;
      })
      .catch(err => {
        console.log('Error: ' + err);
      });
    this.listFriends();
    this.listMeetYou();

  }

  ngOnInit() {}

  chat(otherUsername) {
    this.navCtrl.navigateForward(
      '/chat/' + this.logged.user.username + '/' + otherUsername
    );
  }

  editProfile(id) {
    this.navCtrl.navigateForward('/edit-profile/2');
  }

  private listFriends(): void {
    this.dM.listFriends().then((data: any) => {
        this.friends = data;
      }).catch(error => {

      });
  }

  private listMeetYou(): void {
    this.dM.listMeetYou().then((data: any) => {
      this.meetYou = data;
    }).catch(error => {

    });
  }

 private listYouWantToMeet(): void {
    this.dM.listYouWantToMeet().then((data: any) => {
      this.youWantToMeet = data;
    }).catch(error => {

    });
  }

  accept(username: string) {
    this.dM.resolveFriendRequest('accept', username).then((_) => {
      this.listMeetYou();
      this.listFriends();
    });
  }

  reject(username: string) {
    this.dM.resolveFriendRequest('reject', username).then((_) => {
      this.listMeetYou();
      this.listFriends();
    });
  }
}
