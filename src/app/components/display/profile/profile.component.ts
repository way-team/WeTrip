import { Component, OnInit, Input } from '@angular/core';
import { UserProfile } from 'src/app/app.data.model';
import { NavController, IonDatetime } from '@ionic/angular';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss'],
})
export class ProfileComponent implements OnInit {

  @Input()
  public user: UserProfile;

  public myProfile: Boolean = true;
  public interests: string[];
  public today: Date;

  constructor(
    private navCtrl: NavController,
  ) { }

  ngOnInit() {}

  goTo(destination: string, username: string) {
    const dest: string = destination + username;
    this.navCtrl.navigateForward(dest);
  }

}
