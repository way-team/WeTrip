import { Component, OnInit } from '@angular/core';
import {
  NavController,
  LoadingController,
  ToastController,
  AlertController
} from '@ionic/angular';
import { ActivatedRoute } from '@angular/router';
import { UserProfile } from 'src/app/app.data.model';
import { DataManagement } from 'src/app/services/dataManagement';
import { CookieService } from 'ngx-cookie-service';

@Component({
  selector: 'app-rating',
  templateUrl: './rating.page.html',
  styleUrls: ['./rating.page.scss']
})
export class RatingPage implements OnInit {
  public user: UserProfile;
  private username: string;
  public ratingActual: Number;
  public rating: Number;
  public voted: string;

  constructor(
    private dm: DataManagement,
    private cookieService: CookieService,
    private activatedRoute: ActivatedRoute,
     public alertCtrl: AlertController
  ) {
    this.username = this.activatedRoute.snapshot.paramMap.get('username');
    this.getUser(this.username);

  }

  ngOnInit() {}

  private getUser(username: string) {
    const token = this.cookieService.get('token');
    this.dm
      .getUserBy(username, token)
      .then((res: UserProfile) => {
        this.user = res;
        this.ratingActual=res.avarageRate;
        this.voted=this.username;
      })
      .catch(error => {
        console.log(error);
      });
  }
   public rate() {
    this.dm
      .rate(
        this.voted,
        this.rating
      )
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
}
