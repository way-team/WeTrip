import { Component, OnInit } from '@angular/core';
import {
  NavController,
  AlertController,
  LoadingController
} from '@ionic/angular';
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
    private translate: TranslateService,
    public loadingCtrl: LoadingController
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
    this.listYouWantToMeet();
  }

  ngOnInit() {}

  chat(otherUsername) {
    this.navCtrl.navigateForward(
      '/chat/' + this.logged.user.username + '/' + otherUsername
    );
  }

  block(userToBlock) {
    const translationHeader: string = this.translate.instant(
      'CONTACTS.ALERT_MESSAGE_HEADER'
    );
    const translationMessage: string = this.translate.instant(
      'CONTACTS.ALERT_MESSAGE_MESSAGE'
    );
    const translationConfirm: string = this.translate.instant(
      'CONTACTS.ALERT_MESSAGE_CONFIRM'
    );
    const translationCancel: string = this.translate.instant(
      'CONTACTS.ALERT_MESSAGE_CANCEL'
    );
    const translationSuccessMessage: string = this.translate.instant(
      'CONTACTS.ALERT_MESSAGE_SUCCESS'
    );
    this.alertCtrl
      .create({
        header: translationHeader,
        message: translationMessage,
        buttons: [
          {
            text: translationConfirm,
            handler: () => {
              this.dM.block(userToBlock).then(res => {
                this.showLoading();
                setTimeout(() => {
                  this.alertCtrl
                    .create({
                      header: translationHeader,
                      message: translationSuccessMessage,
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
                }, 750);
                this.listFriends();
              });
            }
          },
          {
            text: translationCancel,
            role: 'Cancel'
          }
        ]
      })
      .then(alertEl => {
        alertEl.present();
      });
  }
  showLoading() {
    const translation2: string = this.translate.instant('DISCOVER.WAIT');
    this.loadingCtrl
      .create({
        message: translation2,
        showBackdrop: true,
        duration: 500
      })
      .then(loadingEl => {
        loadingEl.present();
      });
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

  private listYouWantToMeet(): void {
    this.dM
      .listYouWantToMeet()
      .then((data: any) => {
        this.youWantToMeet = data;
      })
      .catch(error => {});
  }

  accept(username: string) {
    this.dM.resolveFriendRequest('accept', username).then(_ => {
      this.listMeetYou();
      this.listFriends();
    });
  }

  reject(username: string) {
    this.dM.resolveFriendRequest('reject', username).then(_ => {
      this.listMeetYou();
      this.listFriends();
    });
  }
}
