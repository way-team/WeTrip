import { Injectable } from '@angular/core';
import {
  CanActivate,
  ActivatedRouteSnapshot,
  RouterStateSnapshot,
  CanLoad,
  Route,
  UrlSegment
} from '@angular/router';
import { Observable } from 'rxjs';
import { CookieService } from 'ngx-cookie-service';
import { AlertController } from '@ionic/angular';
import { DataManagement } from 'src/app/services/dataManagement';


@Injectable({
  providedIn: 'root'
})
export class AdminGuard implements CanLoad {
  constructor(
    private cookieService: CookieService,
    public alertCtrl: AlertController,
    private dm: DataManagement
  ) {}
  canLoad(
    route: Route,
    segments: UrlSegment[]
  ): Observable<boolean> | Promise<boolean> | boolean {
    const check = this.cookieService.check('token');
    const token = this.cookieService.get('token');
    const isAdmin = this.dm.getUserLogged(token).then((data)=> {
      return data.user.is_staff;
    });
    if (!check || !isAdmin) {
      this.alertCtrl
        .create({
          header: 'Unathenticated!',
          message: 'You are not allowed to access to this resource',
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
    return check && isAdmin;
  }
}
