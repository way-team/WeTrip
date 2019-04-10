import { Component, OnInit } from '@angular/core';
import { NavController } from '@ionic/angular';
import { Router } from '@angular/router';


@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.page.html',
  styleUrls: ['./dashboard.page.scss']
})
export class DashboardPage implements OnInit {
  statsType = 'trips';
  constructor(public router: Router) { }

  ngOnInit() {}


  public onClickTripsByMonth() { 
    this.router.navigate(['/dashboard/tripsByMonth']);
  }

  public onClickPublicVsPrivate() { 
    this.router.navigate(['/dashboard/publicVsPrivate']);
  }

  public onClickApplicationsPerTrip() { 
    this.router.navigate(['/dashboard/applicationsPerTrip']);
  }

  public onClickVisitedCities() { 
    this.router.navigate(['/dashboard/visitedCities']);
  }

  public onClickUsersByGender() { 
    this.router.navigate(['/dashboard/usersByGender']);
  }

  public onClickPremiumUsers() { 
    this.router.navigate(['/dashboard/premiumUsers']);
  }

  public onClickActiveVsInactive() { 
    this.router.navigate(['/dashboard/activeVsInactive']);
  }

  public onClickUsersMetrics() { 
    this.router.navigate(['/dashboard/usersMetrics']);
  }
}
