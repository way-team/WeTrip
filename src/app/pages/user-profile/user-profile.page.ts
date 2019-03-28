import { Component, OnInit } from '@angular/core';
import { UserProfile } from 'src/app/app.data.model';
import { DataManagement } from 'src/app/services/dataManagement';
import { CookieService } from 'ngx-cookie-service';

@Component({
  selector: 'app-user-profile',
  templateUrl: './user-profile.page.html',
  styleUrls: ['./user-profile.page.scss'],
})
export class UserProfilePage implements OnInit {

  public userLogged: UserProfile;

  constructor(
    private dm: DataManagement,
    private coockieService: CookieService
  ) {
    this.getUserLogged();
  }

  ngOnInit() {
  }

  private getUserLogged() {
    const token = this.coockieService.get('token');
    this.dm.getUserLogged(token).then((res: UserProfile) => {
      this.userLogged = res;
    }).catch(error => {
      console.log(error);
    });

    // return null;
  }

}
