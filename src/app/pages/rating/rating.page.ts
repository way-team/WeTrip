import { Component, OnInit } from '@angular/core';
import { NavController, LoadingController, ToastController } from '@ionic/angular';
import { ActivatedRoute  } from '@angular/router';
import { UserProfile } from 'src/app/app.data.model';
import { DataManagement } from 'src/app/services/dataManagement';
import { CookieService } from 'ngx-cookie-service';

@Component({
  selector: 'app-rating',
  templateUrl: './rating.page.html',
  styleUrls: ['./rating.page.scss'],
})
export class RatingPage implements OnInit {

  public user: UserProfile;
  private username: string;
  public ratingActual: integer;


  constructor(
      private dm: DataManagement,
    private cookieService: CookieService,
    private activatedRoute: ActivatedRoute
  ) {
    this.username = this.activatedRoute.snapshot.paramMap.get('username');
   this.getUser(this.username);
   this.ratingActual=3;
  }

  ngOnInit() {

  }
    private getUser(username: string) {
    const token = this.cookieService.get('token');
    this.dm.getUserBy(username, token).then((res: UserProfile) => {
      this.user = res;
    }).catch(error => {
      console.log(error);
    });
  }

}
