import { Component, OnInit, Input } from '@angular/core';
import { UserProfile, User } from 'src/app/app.data.model';
import { NavController, IonDatetime, LoadingController, AlertController } from '@ionic/angular';
import { TranslateService } from '@ngx-translate/core';
import { CookieService } from 'ngx-cookie-service';
import { DataManagement } from '../../../services/dataManagement';
import { ConditionalExpr } from '@angular/compiler';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss'],
})
export class ProfileComponent implements OnInit {

  @Input()
  public user: UserProfile;

  public myProfile: Boolean;
  public interests: string[];
  public today: Date;

  private userLogged: UserProfile;
  private userProfile: UserProfile;

  constructor(
    private navCtrl: NavController,
    public alertCtrl: AlertController,
    private translate: TranslateService,
    private cookieService: CookieService,
    public dm: DataManagement,
    public loadingCtrl: LoadingController,
  ) {}

  ngOnInit() {
    this.isMyProfile(); 
  }

  goTo(destination: string, username: string) {
    let translationAlert:string = this.translate.instant('PROFILE.SORRY');
    let translationDelete1:string = this.translate.instant('PROFILE.ELIMINATED');
    const dest: string = destination + username;

    this.dm.getUserBy(username, this.cookieService.get('token')).then(userProfile => {
      this.userProfile = userProfile;
      if(this.userProfile.status=='D'){
        this.alertCtrl
          .create({
            header: translationAlert,
            subHeader: translationDelete1,
            buttons: [
              {
                text: 'OK',
                role: 'ok',
              }
            ]
          })
          .then(alertEl => {
            alertEl.present();
          });
      } else {
        this.navCtrl.navigateForward(dest);
      }
    });

  }

  delete() {
    let translationAlert:string = this.translate.instant('PROFILE.ALERT');
    let translationDelete1:string = this.translate.instant('PROFILE.DELETE_USER_1');
    let translationDelete2:string = this.translate.instant('PROFILE.DELETE_USER_2');
    let translationDelete3:string = this.translate.instant('PROFILE.DELETE_USER_3');
    let translationYes:string = this.translate.instant('PROFILE.YES');

    setTimeout(() => {
      this.alertCtrl
        .create({
          header: translationAlert,
          subHeader: translationDelete1,
          message:
            translationDelete2+"<br \><br \><strong>"+translationDelete3+"</strong>",
          buttons: [
            {
              text: translationYes,
              role: 'yes',
              handler: () => {
                this.deleteUser();
              }
            },
            {
              text: "NO"
            }
          ]
        })
        .then(alertEl => {
          alertEl.present();
        });
    }, 100);
  }

  deleteUser(){
    let translationError1:string = this.translate.instant('PROFILE.DELETE_ERROR_1');
    let translationError2:string = this.translate.instant('PROFILE.DELETE_ERROR_2');
    this.dm
      .deleteUser()
      .then(data => {
        this.deleteToken();
      }).catch(error => {
          this.showLoading();
          setTimeout(() => {
            this.alertCtrl
              .create({
                header: 'Error',
                message: translationError1+"<br \><br \>"+translationError2,
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
          }, 1500);
        });
  }

  deleteToken(){
    this.cookieService.delete('token');
    this.navCtrl.navigateRoot('/');
  }

  
  showLoading() {
    let translation2:string = this.translate.instant('LOGIN.WAIT');
    this.loadingCtrl
      .create({
        message: translation2,
        showBackdrop: true,
        duration: 1000
      })
      .then(loadingEl => {
        loadingEl.present();
      });
  }

  isMyProfile(){
    this.dm.getUserLogged(this.cookieService.get('token')).then(userProfile => {
      this.userLogged = userProfile;
      if(this.user){
        this.myProfile = this.userLogged.user.id==this.user.user.id;
      } else {
        this.myProfile = false;
      }
    });
  }
}
