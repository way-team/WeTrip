import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';
import { Ng2OdometerModule } from 'ng2-odometer';

import { IonicModule } from '@ionic/angular';
import { TranslateModule, TranslateLoader } from '@ngx-translate/core';
import { DashboardDetailPage } from './dashboard-detail.page';

const routes: Routes = [
  {
    path: '',
    component: DashboardDetailPage
  }
];

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    TranslateModule,
    RouterModule.forChild(routes),
    Ng2OdometerModule.forRoot()
  ],
  declarations: [DashboardDetailPage]
})
export class DashboardDetailPageModule {}
