import { Component, OnInit, Input } from '@angular/core';
import { UserProfile } from 'src/app/app.data.model';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss'],
})
export class ProfileComponent implements OnInit {

  @Input()
  public userLogged: UserProfile;

  constructor() { }

  ngOnInit() {}

}
